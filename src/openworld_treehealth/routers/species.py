from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/species", tags=["species"])


class SpeciesRequest(BaseModel):
    leaf_shape: Literal["needle", "broad", "lobed", "compound"]
    bark_texture: Literal["smooth", "furrowed", "peeling"]
    seed_type: Literal["cone", "samara", "nut", "berry", "pod"]
    region: Literal["temperate", "tropical", "boreal", "arid"]


class SpeciesResponse(BaseModel):
    species: str = Field(..., description="Predicted species name")
    confidence: float = Field(..., ge=0.0, le=1.0)


@router.post("/classify", response_model=SpeciesResponse)
async def classify_species(payload: SpeciesRequest) -> SpeciesResponse:
    score = 0
    if payload.leaf_shape == "needle" and payload.seed_type == "cone":
        return SpeciesResponse(species="Pinus sylvestris", confidence=0.92)
    if payload.leaf_shape == "lobed" and payload.seed_type in {"nut", "samara"}:
        score += 0.5
    if payload.bark_texture == "furrowed":
        score += 0.2
    if payload.region == "temperate":
        score += 0.2
    if score >= 0.8:
        return SpeciesResponse(species="Quercus robur", confidence=min(score, 0.98))
    if payload.leaf_shape == "compound" and payload.seed_type == "berry":
        return SpeciesResponse(species="Sorbus aucuparia", confidence=0.75)
    return SpeciesResponse(species="Unknown", confidence=0.55)


