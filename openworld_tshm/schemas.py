from __future__ import annotations
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, conint, confloat, ConfigDict


class TreeRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: conint(ge=0)
    height: confloat(ge=0)
    point_count: conint(ge=1)
    footprint: confloat(gt=0)
    p95_height: Optional[confloat(ge=0)] = None
    p50_height: Optional[confloat(ge=0)] = None
    density: Optional[confloat(ge=0)] = None
    centroid_x: float
    centroid_y: float


class Metrics(BaseModel):
    num_trees: conint(ge=0)
    avg_height: confloat(ge=0)
    species_breakdown: Dict[str, float] = Field(default_factory=dict)
    health_index_avg: confloat(ge=0)


class ProvenanceRecordModel(BaseModel):
    timestamp: float
    actor: str
    host: str
    step: str
    params: dict
    inputs: List[str]
    outputs: List[str]
    code_version: Optional[str]
    digest: str
    env: Optional[dict] = None

