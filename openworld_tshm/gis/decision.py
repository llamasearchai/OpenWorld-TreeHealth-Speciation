from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Suggestion:
    harvest_years: int
    planting_density_per_acre: int
    regeneration_target_pct: float


# simplistic rotation ages and densities by species
ROTATION = {"pine": 30, "oak": 40, "spruce": 35}
DENSITY = {"pine": 600, "oak": 450, "spruce": 550}


def suggest(species: str, current_age: int, health_idx: float) -> Suggestion:
    rotation = ROTATION.get(species, 35)
    remaining = max(rotation - current_age, 0)
    # Adjust by health: poor health accelerates harvest
    adj = -5 if health_idx < 0.7 else 0
    harvest_years = max(remaining + adj, 0)
    planting_density = DENSITY.get(species, 500)
    regen_target = 0.9 if health_idx >= 0.8 else 0.8
    return Suggestion(harvest_years=int(harvest_years), planting_density_per_acre=planting_density, regeneration_target_pct=regen_target)


