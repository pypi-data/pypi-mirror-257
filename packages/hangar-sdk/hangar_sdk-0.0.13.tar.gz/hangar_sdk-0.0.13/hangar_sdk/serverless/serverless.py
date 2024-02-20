import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict
from attr import define

from hangar_sdk.constructs import S3, Asset, FilePath, LambdaFunction, LambdaLayer
from hangar_sdk.library import CompositeResource, HangarScope
from hangar_sdk.serverless.packager import (
    AppOnlyDeploymentPackager,
    LayerDeploymentPackager,
)
from hangar_sdk.serverless.utils import get_current_runtime

from hangar_sdk.config import Config
import boto3


@define(frozen=False, slots=False)
class HangarLambdaPackager(CompositeResource):
    dir_path: str
    runtime: str
    layer: str = ""
    only_app: str = ""

    def _resolve(self):
        from hangar_sdk.serverless.utils import UI, OSUtils

        from hangar_sdk.serverless.packager import DependencyBuilder

        dep_builder = DependencyBuilder(
            osutils=OSUtils(),
        )

        # packager = LambdaDeploymentPackager(
        #     osutils=OSUtils(),
        #     dependency_builder=dep_builder,
        #     ui=UI()
        # )

        layer_packager = LayerDeploymentPackager(
            osutils=OSUtils(), dependency_builder=dep_builder, ui=UI()
        )

        app_packager = AppOnlyDeploymentPackager(
            osutils=OSUtils(), dependency_builder=dep_builder, ui=UI()
        )

        # filename = packager.create_deployment_package(
        #     project_dir=self.dir_path,
        #     python_version=self.runtime
        # )

        layer = layer_packager.create_deployment_package(
            project_dir=self.dir_path, python_version=self.runtime
        )

        only_app = app_packager.create_deployment_package(
            project_dir=self.dir_path, python_version=self.runtime
        )

        # self.app = filename
        self.layer = layer
        self.only_app = only_app


class HangarServerlessFunction:
    def __init__(self, func, scope: HangarScope, secrets: Dict[str, str] = {}):
        self.func = func
        self.scope = scope
        self.secrets = secrets

    def __call__(self, event, context) -> Any:
        args = event.get("args", [])
        kwargs = event.get("kwargs", {})

        print("test")

        for key, value in self.secrets.items():
            print(boto3.client("ssm").get_parameter(Name=value, WithDecryption=True))
            value = boto3.client("ssm").get_parameter(Name=value, WithDecryption=True)[
                "Parameter"
            ]["Value"]
            os.environ[key] = value
            print(f"Setting {key} to {value}")

        return self.func(*args, **kwargs)

    def invoke(self, *args, **kwargs):
        payload = {"args": args, "kwargs": kwargs}

        client = self.scope.get_boto3_session().client("lambda")

        response = client.invoke(
            FunctionName="hangar_serverless_" + self.func.__name__,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload),
        )
        return json.loads(response["Payload"].read().decode("utf-8"))


class LocalHangarServerlessFunction:
    def __init__(self, func, scope) -> None:
        self.func = func
        self.scope = scope

    def __call__(self, *args, **kwargs) -> Any:
        if os.getenv("HANGAR_ENVIRONMENT") == "LOCAL":
            payload = {"args": args, "kwargs": kwargs}
            client = self.scope.get_boto3_session().client("lambda")

            response = client.invoke(
                FunctionName="hangar_serverless_" + self.func.__name__,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )
            return json.loads(response["Payload"].read().decode("utf-8"))

        else:
            raise Exception(
                "Cannot call remote function. Call within a local function."
            )

    def invoke(self, *args, **kwargs):
        return self(*args, **kwargs)


class Serverless:
    def __init__(self, name, path, scope: HangarScope, bucket: S3, role_arn: str):
        self.name = name
        self._functions = []
        self.file = path
        self.local_entrypoint = None
        self.scope = scope
        self.bucket = bucket
        self.role_arn = role_arn
        self.mode = Config.mode

    @property
    def env(self):
        return os.getenv("HANGAR_ENVIRONMENT")

    def Function(self, timeout=60, environment_variables={}, role=None, secrets={}):
        def function_decorator(func):
            if self.env == "REMOTE":
                print("Remote")
                return HangarServerlessFunction(func, self.scope, secrets=secrets)

            if self.env == "LOCAL":
                return HangarServerlessFunction(func, self.scope, secrets=secrets)
            else:
                functionPath = (
                    os.path.basename(self.file).split(".")[0] + "." + func.__name__
                )
                self._functions.append(
                    {
                        "path": functionPath,
                        "timeout": timeout,
                        "environment_variables": environment_variables,
                        "role": role,
                    }
                )
                return LocalHangarServerlessFunction(func, self.scope)

        return function_decorator

    def LocalEntrypoint(self, func):
        self.local_function = func
        return

    async def _resolve(self):
        if self.env == "REMOTE":
            return

        if self.mode == "invoke":
            if self.local_function:
                os.environ["HANGAR_ENVIRONMENT"] = "LOCAL"
                self.local_function()
                del os.environ["HANGAR_ENVIRONMENT"]

            return
        
        current_runtime = get_current_runtime()


        packager = HangarLambdaPackager(
            dir_path=os.path.dirname(self.file),
            runtime=current_runtime,
            name="hangar_serverless_packager",
            scope=self.scope,
        )

        packager._resolve()

        self._resources = []

        asset_bucket = self.bucket

        layer_asset = Asset(
            name=self.name + "-hangar_serverless_layer_asset",
            source=FilePath(
                name=os.path.basename(packager.layer),
                path=packager.layer,
                scope=self.scope,
            ),
            bucket=asset_bucket,
            scope=self.scope,
        )

        app_asset = Asset(
            name=self.name + "-hangar-serverless-app-asset",
            source=FilePath(
                name=os.path.basename(packager.only_app),
                path=packager.only_app,
                scope=self.scope,
            ),
            bucket=asset_bucket,
            scope=self.scope,
        )
        # app_asset.sync()


        layer = LambdaLayer(
            scope=self.scope,
            name=self.name + "-hangar_serverless_layer",
            asset=layer_asset,
            runtimes=[current_runtime],
        )   

        for func in self._functions:
            LambdaFunction(
                scope=self.scope,
                name="hangar_serverless_" + func["path"].split(".")[1],
                handler=func["path"],
                asset=app_asset,
                function_name=func["path"].split(".")[1],
                role=self.role_arn if func["role"] is None else func["role"],
                runtime=current_runtime,
                timeout=func["timeout"],
                environment={
                    "HANGAR_ENVIRONMENT": "REMOTE",
                    "HANGAR_API_KEY": self.scope.api_key,
                    **func["environment_variables"],
                },
                layers=[layer],
            )

        print("Deploying")

        await self.scope.deploy()

        return self._resources
