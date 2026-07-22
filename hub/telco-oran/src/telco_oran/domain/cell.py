from dataclasses import dataclass


@dataclass
class Cell:
    """A RAN cell site with static topology and configuration."""

    cell_id: int
    max_capacity: int
    lat: float
    lon: float
    bands: list[str]
    area_type: str
    city: str
    adjacent_cells: list[int]
