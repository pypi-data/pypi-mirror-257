import os
import pathlib
import tarfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Union

from aiohttp import ClientError
from attr import define
from pydantic import BaseModel

from .base import HangarScope
from .library import CompositeResource, Deployable


class SourceInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, source):
        pass


@define(kw_only=True, slots=False)
class S3(CompositeResource, Deployable):
    @property
    def client(self):
        session = self.scope.get_boto3_session()
        return session.client("s3")

    def create_construct_definition(self) -> dict:
        return {
            "construct": "s3",
            "name": self.name,
        }


@define(kw_only=True, slots=False)
class GCS(CompositeResource, Deployable):
    location: str

    def create_construct_definition(self) -> dict:
        return {"construct": "gcs", "name": self.name, "location": self.location}


@define(kw_only=True, slots=False)
class Asset(CompositeResource, Deployable):
    source: SourceInterface
    bucket: S3

    def create_construct_definition(self) -> dict:
        return {
            "construct": "asset",
            "name": self.name,
            "source": {"!REF": True, "resourceId": self.source.name},
            "bucket": self.bucket._get_ref(),
        }

    def post_resolve(self):
        print("uploading asset")
        self.sync()

    def sync(self, token=None):
        if self.mode == "delete":
            return

        if isinstance(self.source, DirPath):
            fname = f"{self.source.name}.tar"

            ignorefile = (
                pathlib.Path(self.source.ignorefile) if self.source.ignorefile else None
            )

            if ignorefile and ignorefile.exists():
                with tarfile.open(fname, "w") as tar:
                    tar.add(
                        self.source.path,
                        arcname=os.path.basename(self.source.path),
                        filter=lambda x: x
                        if x.name not in ignorefile.read_text().split("\n")
                        else None,
                    )
            else:
                with tarfile.open(fname, "w") as tar:
                    tar.add(
                        self.source.path, arcname=os.path.basename(self.source.path)
                    )

            try:
                self.bucket.client.upload_file(
                    fname, self.bucket.name, f"{self.source.name}/{fname}"
                )
            except ClientError as e:
                print(e)

        elif isinstance(self.source, FilePath):
            try:
                self.bucket.client.upload_file(
                    self.source.path,
                    self.bucket.name,
                    self.source.name
                    if self.source.name
                    else os.path.basename(self.source.path),
                )
            except ClientError as e:
                print(e)

        elif isinstance(self.source, GitHubRepo):
            self.scope.execute_action(
                self.name, "sync", {"token": token} if token is not None else {}
            )


@define(kw_only=True, slots=False)
class DirPath(CompositeResource, SourceInterface, Deployable):
    path: str
    name: str
    ignorefile: Union[str, None] = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "dirpath",
            "name": self.name,
            "path": self.path,
        }


@define(kw_only=True, slots=False)
class FilePath(CompositeResource, SourceInterface, Deployable):
    path: str
    name: Optional[str]

    def create_construct_definition(self) -> dict:
        return {
            "construct": "filepath",
            "name": self.name,
            "path": self.path,
        }


@define(kw_only=True, slots=False)
class GitHubRepo(CompositeResource, SourceInterface, Deployable):
    repo: str
    branch: str

    def create_construct_definition(self) -> dict:
        return {
            "construct": "githubrepo",
            "name": self.name,
            "repository": self.repo,
            "branch": self.branch,
        }


class BuilderInterface(ABC):
    builderType: str

    @abstractmethod
    def __init__(self, builder):
        pass


@define(kw_only=True, slots=False)
class BuildkitBuilder(CompositeResource, BuilderInterface, Deployable):
    builder_type = "buildkit"

    def create_construct_definition(self) -> dict:
        return {"construct": "buildkit", "name": self.name}


class RegistryInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, builder):
        pass


@define(kw_only=True, slots=False)
class Registry(CompositeResource, RegistryInterface, Deployable):
    def create_construct_definition(self):
        return {"construct": "ecr"}


@define(kw_only=True, slots=False)
class ContainerBuilder(CompositeResource, Deployable):
    asset: Asset
    builder: BuilderInterface
    registry: RegistryInterface

    def create_construct_definition(self):
        return {
            "construct": "codebuild",
            "asset": self.asset._get_ref(),
            "builder": self.builder._get_ref(),
            "registry": self.registry._get_ref(),
        }

    def build(self, build_context=None, tag="latest"):
        if self.mode == "delete":
            return
        session = self.scope.get_boto3_session()
        client = session.client("codebuild")
        env_variables = [
            {
                "name": "BUILD_CONTEXT",
                "value": build_context,
                "type": "PLAINTEXT",
            },
            {
                "name": "TAG",
                "value": tag,
                "type": "PLAINTEXT",
            },
        ]
        # Start a build with environment variable overrides
        return client.start_build(
            projectName=self.name,
            environmentVariablesOverride=env_variables,
        )

        # return self.scope.execute_action(
        #     self.name,
        #     "build",
        #     {
        #         "build_context": build_context
        #         if build_context is not None
        #         else self.name,
        #         "tag": tag
        #     },
        # )

    def poll(self, build_id=None):
        if self.mode == "delete":
            return

        if build_id == None:
            print("no build passed, skipping polling")
            return

        session = self.scope.get_boto3_session()
        codebuild = session.client("codebuild")
        build = codebuild.batch_get_builds(ids=[build_id])
        return build["builds"][0]


class PortMappings(BaseModel):
    containerPort: int
    hostPort: int


@define(kw_only=True, slots=False)
class Container(CompositeResource, Deployable):
    source: Registry
    tag: str
    startCommand: str = None
    portMappings: List[PortMappings] = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "container",
            "registry": self.source._get_ref(),
            "tag": self.tag,
            "startCommand": self.startCommand.split(" ")
            if self.startCommand is not None
            else None,
            "portMappings": [mapping.model_dump() for mapping in self.portMappings]
            if self.portMappings is not None
            else None,
        }


@define(kw_only=True, slots=False)
class Service(CompositeResource):
    name: str
    container: Container
    environmentVariables: Union[Dict[str, str], None] = None


def env_vars_dict_to_str(env_vars: Dict[str, str]):
    return "\n".join([f"{k}={v}" for k, v in env_vars.items()])


@define(kw_only=True, slots=False)
class Cluster(CompositeResource, Deployable):
    name: str
    services: List[Service]

    def log(self, path=""):
        if self.mode == "delete":
            return
        return self.scope.get_logs(self.name, path)

    def create_construct_definition(self) -> dict:
        return {
            "construct": "cluster",
            "name": self.name,
            "services": [
                {
                    "name": s.name,
                    "container": s.container._get_ref(),
                    "environment_variables": env_vars_dict_to_str(
                        s.environmentVariables
                    )
                    if s.environmentVariables
                    else "",
                }
                for s in self.services
            ],
        }


class HostInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, builder):
        pass


class Ingress(BaseModel):
    fromPort: int
    toPort: int
    protocol: str
    cidrIp: List[str]


class Egress(BaseModel):
    fromPort: int
    toPort: int
    protocol: str
    cidrIp: List[str]


@define(kw_only=True, slots=False)
class SecurityGroup(CompositeResource, Deployable):
    name: str
    ingresses: List[Ingress] = None
    egresses: List[Egress] = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "securitygroup",
            "ingresses": [
                {
                    "fromPort": str(ingress.fromPort),
                    "toPort": str(ingress.toPort),
                    "protocol": ingress.protocol,
                    "cidrIp": ingress.cidrIp,
                }
                for ingress in self.ingresses
            ],
            "egresses": [
                {
                    "fromPort": str(egress.fromPort),
                    "toPort": str(egress.toPort),
                    "protocol": egress.protocol,
                    "cidrIp": egress.cidrIp,
                }
                for egress in self.egresses
            ],
        }


@define(kw_only=True, slots=False)
class Instance(CompositeResource, Deployable):
    name: str
    security_groups: List[SecurityGroup]
    instance_type: str
    path_to_key: Union[str, None] = None
    ssh: bool = True

    def pre_resolve(self):
        if self.ssh:
            works = False
            for sg in self.security_groups:
                if (
                    Ingress(
                        protocol="tcp",
                        fromPort=22,
                        toPort=22,
                        cidrIp=["0.0.0.0/0"],
                    )
                    in sg.ingresses
                ):
                    works = True
                    break
            if not works:
                self.security_groups[0].ingresses.append(
                    Ingress(
                        protocol="tcp",
                        fromPort=22,
                        toPort=22,
                        cidrIp=["0.0.0.0/0"],
                    )
                )

    def create_construct_definition(self) -> dict:
        return {
            "construct": "instance",
            "securityGroups": [sg._get_ref() for sg in self.security_groups],
            "instance_type": self.instance_type,
        }

    def run_command(self, command: str):
        if self.mode == "delete":
            return
        import os
        import sys

        import paramiko

        # Function to get default SSH key path based on the operating system
        def get_default_ssh_key_path():
            home = os.path.expanduser("~")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                # Default path for Linux and macOS
                return os.path.join(home, ".ssh", "id_rsa")
            elif sys.platform.startswith("win32"):
                # Default path for Windows
                return os.path.join(home, ".ssh", "id_rsa")
            else:
                raise ValueError("Unsupported operating system")

        INSTANCE_USER = "ubuntu"  # e.g., 'ec2-user' or 'ubuntu'

        if not self.path_to_key:
            # Prompt user for SSH key path or use default
            self.path_to_key = get_default_ssh_key_path()

        # Read your public key
        public_key_path = self.path_to_key + ".pub"
        with open(public_key_path, "r") as key_file:
            public_key = key_file.read().strip()

        try:
            self.scope.execute_action(
                self.name, "send_public_key", {"public_key": public_key}
            )
            print("Public key sent successfully.")
        except Exception as e:
            print(f"Failed to send public key: {e}")

        # Connect to the instance using Paramiko
        key = paramiko.RSAKey.from_private_key_file(self.path_to_key)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=self.state[self.name]["values"]["public_ip"],
                username=INSTANCE_USER,
                pkey=key,
            )
            print("SSH connection established.")

            _stdin, _stdout, _stderr = ssh_client.exec_command(command)
            _stdin.close()

        except Exception as e:
            print(self.state[self.name]["values"])
            print(f"SSH connection failed: {e}")
        finally:
            ssh_client.close()
            print("SSH connection closed.")

        # return command_results

        return {
            "command": command,
            "stdout": _stdout.read().decode(),
            "stderr": _stderr.read().decode(),
        }

    def run_commands(self, commands: List[str]):
        if self.mode == "delete":
            return

        import os
        import sys

        import paramiko

        # Function to get default SSH key path based on the operating system
        def get_default_ssh_key_path():
            home = os.path.expanduser("~")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                # Default path for Linux and macOS
                return os.path.join(home, ".ssh", "id_rsa")
            elif sys.platform.startswith("win32"):
                # Default path for Windows
                return os.path.join(home, ".ssh", "id_rsa")
            else:
                raise ValueError("Unsupported operating system")

        INSTANCE_USER = "ubuntu"  # e.g., 'ec2-user' or 'ubuntu'

        if not self.path_to_key:
            # Prompt user for SSH key path or use default
            self.path_to_key = get_default_ssh_key_path()

        # Read your public key
        public_key_path = self.path_to_key + ".pub"
        with open(public_key_path, "r") as key_file:
            public_key = key_file.read().strip()

        try:
            self.scope.execute_action(
                self.name, "send_public_key", {"public_key": public_key}
            )
            print("Public key sent successfully.")
        except Exception as e:
            print(f"Failed to send public key: {e}")

        # Connect to the instance using Paramiko
        key = paramiko.RSAKey.from_private_key_file(self.path_to_key)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=self.state[self.name]["values"]["public_ip"],
                username=INSTANCE_USER,
                pkey=key,
            )
            print("SSH connection established.")

            for command in commands:
                _stdin, _stdout, _stderr = ssh_client.exec_command(command)
                yield {
                    "command": command,
                    "stdout": _stdout.read().decode(),
                    "stderr": _stderr.read().decode(),
                }
                _stdin.close()

        except Exception as e:
            print(self.state[self.name]["values"])
            print(f"SSH connection failed: {e}")
        finally:
            ssh_client.close()
            print("SSH connection closed.")


class DockerEnvironment(CompositeResource):
    name: str
    host: Instance
    containers: List[Container]

    def post_resolve(self):
        self.host.run_commands(["sudo apt update", "sudo apt install -y docker.io"])
        self.ssh_host = self.host.state[self.host.name]["values"]["public_ip"]


@define(kw_only=True, slots=False)
class LambdaLayer(CompositeResource, Deployable):
    asset: Asset
    runtimes: Union[List[str], None] = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "lambda_layer",
            "name": self.name,
            "asset": self.asset._get_ref(),
            "runtimes": self.runtimes,
        }


@define(kw_only=True, slots=False)
class LambdaFunction(CompositeResource, Deployable):
    scope: HangarScope
    name: str
    function_name: str
    asset: Asset
    runtime: str
    handler: str
    timeout: int
    role: str
    environment: Union[Dict[str, str], None] = None
    layers: Union[List[LambdaLayer], None] = None


    def create_construct_definition(self):
        return {
            "construct": "lambda",
            "name": self.function_name,
            "asset": self.asset._get_ref(),
            "role": self.role,
            "runtime": self.runtime,
            "handler": self.handler,
            "timeout": self.timeout,
            "environment": self.environment,
            "layers": [layer._get_ref() for layer in self.layers]
            if self.layers
            else None,
        }


class Queue(CompositeResource, Deployable):
    name: str
    scope: HangarScope
    type: Union[Literal["fifo"], Literal["standard"]]

    def create_construct_definition(self) -> dict:
        return {
            "construct": "queue",
            "name": self.name,
            "config": {
                "type": self.type,
            },
        }

    def send_message(self, message: str):
        if self.mode == "delete":
            return
        self.scope.execute_action(self.name, "send_message", {"message": message})

    def receive_message(self):
        if self.mode == "delete":
            return
        return self.scope.execute_action(self.name, "receive_message", {})

    def delete_message(self, receipt_handle: str):
        if self.mode == "delete":
            return
        return self.scope.execute_action(
            self.name, "delete_message", {"receipt_handle": receipt_handle}
        )

    def purge_queue(self):
        if self.mode == "delete":
            return
        return self.scope.execute_action(self.name, "purge_queue", {})
