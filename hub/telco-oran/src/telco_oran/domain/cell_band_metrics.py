from dataclasses import dataclass, field

from telco_oran.domain.cell import Cell
from telco_oran.domain.ran_kpi_record import RanKpiRecord


@dataclass
class CellBandMetrics:
    """Aggregate of KPI measurements for a specific cell on a specific frequency band."""

    cell: Cell
    band: str
    records: list[RanKpiRecord] = field(default_factory=list)

    @property
    def latest(self) -> RanKpiRecord | None:
        return self.records[-1] if self.records else None

    @property
    def history(self) -> list[RanKpiRecord]:
        return self.records[:-1] if len(self.records) > 1 else []
