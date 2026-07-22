from telco_oran.domain.cell import Cell
from telco_oran.domain.ran_kpi_record import RanKpiRecord
from telco_oran.domain.ran_kpi_record_factory import RanKpiRecordFactory


def test_factory_generates_one_record_per_band():
    cell = Cell(
        cell_id=1,
        max_capacity=87,
        lat=33.029427,
        lon=-96.697085,
        bands=["Band 29", "Band 66"],
        area_type="industrial",
        city="Plano",
        adjacent_cells=[23, 45, 67],
    )

    factory = RanKpiRecordFactory()
    records = factory.create_for_cell(cell)

    assert len(records) == len(cell.bands)

    for record, band in zip(records, cell.bands):
        assert isinstance(record, RanKpiRecord)
        assert record.cell is cell
        assert record.datetime is not None
        assert record.band == band
        assert record.frequency is not None
        assert record.ues_usage >= 0
        assert record.rsrp is not None
        assert record.rsrq is not None
        assert record.sinr is not None
        assert record.throughput_mbps is not None
        assert record.latency_ms is not None
