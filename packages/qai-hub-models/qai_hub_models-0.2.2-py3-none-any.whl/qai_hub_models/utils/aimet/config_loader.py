from pathlib import Path


def get_default_aimet_config() -> str:
    path = Path(__file__).parent / "default_config.json"
    return str(path.resolve())


def get_per_channel_aimet_config() -> str:
    path = Path(__file__).parent / "default_config_per_channel.json"
    return str(path.resolve())
