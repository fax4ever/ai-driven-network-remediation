import random as random_module
from datetime import datetime

from telco_oran.domain.cell import Cell
from telco_oran.domain.ran_kpi_record import RanKpiRecord

BAND_FREQUENCY_MAP: dict[str, str] = {
    "Band 29": "700",
    "Band 26": "850",
    "Band 71": "600",
    "Band 66": "1700-2100",
}

USAGE_PATTERNS: dict[str, dict[str, dict[str, tuple[float, float]]]] = {
    "industrial": {
        "weekdays": {"day": (0.7, 0.9), "night": (0.1, 0.3)},
        "weekends": {"day": (0.4, 0.6), "night": (0.1, 0.3)},
    },
    "commercial": {
        "weekdays": {"day": (0.3, 0.5), "night": (0.6, 0.9)},
        "weekends": {"day": (0.4, 0.6), "night": (0.7, 0.9)},
    },
    "rural": {
        "weekdays": {"day": (0.1, 0.2), "night": (0.1, 0.2)},
        "weekends": {"day": (0.1, 0.2), "night": (0.1, 0.2)},
    },
    "residential": {
        "weekdays": {"day": (0.3, 0.2), "night": (0.7, 0.9)},
        "weekends": {"day": (0.4, 0.6), "night": (0.5, 0.8)},
    },
}


class RanKpiRecordFactory:
    """Factory that generates RAN KPI measurements for a given cell."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random_module.Random(seed)

    def create_for_cell(self, cell: Cell) -> list[RanKpiRecord]:
        current_time = datetime.now()
        is_weekend = current_time.strftime("%A") in ("Saturday", "Sunday")
        is_day = 6 <= current_time.hour < 18

        time_key = "weekends" if is_weekend else "weekdays"
        period_key = "day" if is_day else "night"
        usage_range = USAGE_PATTERNS[cell.area_type][time_key][period_key]

        records = []
        for band in cell.bands:
            ues_usage = int(self._rng.uniform(*usage_range) * cell.max_capacity)

            record = RanKpiRecord(
                cell=cell,
                datetime=current_time,
                band=band,
                frequency=BAND_FREQUENCY_MAP.get(band, "Unknown"),
                ues_usage=ues_usage,
                rsrp=round(self._rng.uniform(-120, -80), 2),
                rsrq=round(self._rng.uniform(-20, -3), 2),
                sinr=round(self._rng.uniform(0, 30), 2),
                throughput_mbps=round(self._rng.uniform(10, 150), 2),
                latency_ms=round(self._rng.uniform(10, 100), 2),
            )
            records.append(record)

        return records
