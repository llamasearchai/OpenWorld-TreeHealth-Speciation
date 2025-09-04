from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class SensorPlugin(ABC):
    name: str

    @abstractmethod
    def ingest(self, source: str, **kwargs: Any) -> dict:
        """
        Ingest data from source and return a standard dict containing:
        - 'type': 'pointcloud' | 'raster' | 'field'
        - 'data': in-memory representation
        - 'metadata': dict
        """
        raise NotImplementedError


