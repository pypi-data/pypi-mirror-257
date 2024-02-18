from datetime import datetime, timezone


def get_local_timezone() -> timezone:
    return datetime.now().astimezone().tzinfo  # pyright: ignore[reportReturnType]
