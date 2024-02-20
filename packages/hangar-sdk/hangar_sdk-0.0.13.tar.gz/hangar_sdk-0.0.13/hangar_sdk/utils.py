from rich.tree import Tree


def print_status(resource, status):
    if status is None:
        return Tree(resource + " : " + "Pending"), None, None
    # print(status)
    items = list(
        map(
            lambda x: {
                "resource_id": x["resource_id"],
                "resource_type": x["resource_type"],
                "status": x["status"],
            },
            list(status["resources"].values()),
        )
    )
    items = sorted(items, key=lambda x: x["resource_type"])
    errors = list(
        map(
            lambda x: {"error_type": "InternalHangarError", "message": x}
            if isinstance(x, str)
            else {
                "resource_id": x["resource_type"],
                "resource_type": x["resource_id"],
                "message": x["message"].split("\n")[0],
            },
            list(status["errors"].values()),
        )
    )
    # print(errors)

    tree = Tree(resource)
    for v in items:
        rendered_status = (
            v["resource_type"] + " - " + v["resource_id"] + " " + v["status"]
        )
        matches = [
            x
            for x in errors
            if (
                "resource_type" in x
                and (
                    v["resource_type"] == x["resource_type"]
                    and v["resource_id"] == x["resource_id"]
                )
            )
            or "error_type" in x
        ]
        # print(matches)

        if len(matches) != 0:
            rendered_status += " error: " + matches[0]["message"]

        tree.add(rendered_status)

    return tree, items, errors
