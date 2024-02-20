from pathlib import Path

RESOURCE_PATH = Path(__file__).parent.resolve()


def resolve_resource_path(path):
    path = path.split(":")
    return Path(RESOURCE_PATH / "{}s/{}".format(*path)).resolve()
