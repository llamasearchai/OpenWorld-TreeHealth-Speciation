from __future__ import annotations
from importlib.metadata import entry_points
from typing import Type
from .plugins.base import SensorPlugin


def load_plugins() -> list[SensorPlugin]:
    plugins: list[SensorPlugin] = []
    try:
        eps = entry_points(group="openworld_tshm.plugins")  # type: ignore[arg-type]
    except TypeError:  # pragma: no cover - legacy importlib.metadata API
        eps = entry_points().get("openworld_tshm.plugins", [])  # type: ignore[call-arg]
    for ep in eps or []:  # type: ignore[assignment]
        try:
            plugin_cls: Type[SensorPlugin] = ep.load()
            plugins.append(plugin_cls())
        except Exception:  # pragma: no cover - skip bad entry point
            continue

    if not plugins:
        # Fallback to builtin plugins so CLI works without installed entry points
        from .plugins.lidar_laspy import LidarLaspyPlugin
        from .plugins.multispectral_rasterio import MultispectralRasterioPlugin
        from .plugins.field_csv import FieldCSVPlugin

        plugins = [LidarLaspyPlugin(), MultispectralRasterioPlugin(), FieldCSVPlugin()]
    return plugins


def get_plugin_by_name(name: str) -> SensorPlugin | None:
    for p in load_plugins():
        if p.name == name:
            return p
    return None


