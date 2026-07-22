from telco_oran.domain.anomaly import Anomaly, LowRsrp, ThroughputDrop
from telco_oran.domain.anomaly_detector import AnomalyDetector
from telco_oran.generation.simulation_factory import SimulationFactory

SEED = 42


def test_detect_anomalies_on_generated_data():
    factory = SimulationFactory(seed=SEED)
    metrics_list = factory.create(num_cells=5, bands_per_cell=2, records_per_band=4)

    detector = AnomalyDetector()
    all_anomalies: list[Anomaly] = []

    for metrics in metrics_list:
        anomalies = detector.detect(metrics)

        for anomaly in anomalies:
            assert isinstance(anomaly, Anomaly)
            assert anomaly.record is metrics.latest
            assert anomaly.record.cell is metrics.cell
            assert anomaly.record.band == metrics.band
            assert str(anomaly)

        all_anomalies.extend(anomalies)

    assert len(all_anomalies) == 2

    throughput_drop = all_anomalies[0]
    assert isinstance(throughput_drop, ThroughputDrop)
    assert throughput_drop.record.cell.cell_id == 0
    assert throughput_drop.record.band == "Band 66"
    assert throughput_drop.throughput_mbps == 18.89
    assert round(throughput_drop.avg_prior_throughput_mbps, 2) == 54.75

    low_rsrp = all_anomalies[1]
    assert isinstance(low_rsrp, LowRsrp)
    assert low_rsrp.record.cell.cell_id == 1
    assert low_rsrp.record.band == "Band 29"
    assert low_rsrp.rsrp == -110.05
