# telco-oran

ORAN/Telco domain model with RAN KPI simulation and anomaly detection.

## Domain Model

- **Cell** — static RAN cell-site topology (location, bands, capacity)
- **RanKpiRecord** — single KPI measurement snapshot (RSRP, RSRQ, SINR, throughput, latency)
- **CellBandMetrics** — aggregate of KPI records for a specific cell on a specific band
- **Anomaly** — hierarchy of detected anomalies (Low RSRP, SINR Degradation, Throughput Drop, High PRB Utilization, UEs Spike/Drop, Cell Outage)
- **AnomalyDetector** — service that detects anomalies from a `CellBandMetrics` aggregate

## Simulation

- **RanKpiRecordFactory** — generates KPI records for a cell using area-type and time-of-day usage patterns
- **SimulationFactory** — generates a full dataset of cells with band metrics and KPI history

## Usage

```bash
cd hub/telco-oran
uv sync --group dev
uv run pytest
```
