from telco_oran.generation.simulation_factory import SimulationFactory

NUM_CELLS = 3
BANDS_PER_CELL = 2
RECORDS_PER_BAND = 4


def test_simulation_factory_generates_expected_structure():
    factory = SimulationFactory()
    metrics = factory.create(
        num_cells=NUM_CELLS,
        bands_per_cell=BANDS_PER_CELL,
        records_per_band=RECORDS_PER_BAND,
    )

    assert len(metrics) == NUM_CELLS * BANDS_PER_CELL

    for m in metrics:
        assert m.cell is not None
        assert m.band is not None
        assert len(m.records) == RECORDS_PER_BAND
        assert m.latest is not None
        assert len(m.history) == RECORDS_PER_BAND - 1


def test_all_records_belong_to_same_cell_and_band():
    factory = SimulationFactory()
    metrics = factory.create(
        num_cells=NUM_CELLS,
        bands_per_cell=BANDS_PER_CELL,
        records_per_band=RECORDS_PER_BAND,
    )

    for m in metrics:
        for record in m.records:
            assert record.cell is m.cell
            assert record.band == m.band


def test_total_number_of_records():
    factory = SimulationFactory()
    metrics = factory.create(
        num_cells=NUM_CELLS,
        bands_per_cell=BANDS_PER_CELL,
        records_per_band=RECORDS_PER_BAND,
    )

    total_records = sum(len(m.records) for m in metrics)
    assert total_records == NUM_CELLS * BANDS_PER_CELL * RECORDS_PER_BAND
