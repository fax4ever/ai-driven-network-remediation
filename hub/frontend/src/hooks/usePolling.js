import { useEffect, useRef, useState } from "react";

const POLL_INTERVAL = 10_000;

export function usePolling(baseUrl) {
  const [summary, setSummary] = useState({
    agent_status: "unknown",
    cluster: "hub",
    site: "edge-01",
    open_incidents: 0,
    servicenow: { mode: "unknown", reachable: false },
    timestamp: "",
  });

  const [integrations, setIntegrations] = useState({
    total: 0,
    up: 0,
    down: 0,
    timestamp: "",
    integrations: [],
    slo: {},
    incident_movie: [],
    business_impact: {},
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const activeRef = useRef(true);

  useEffect(() => {
    activeRef.current = true;

    async function fetchData() {
      try {
        const base = baseUrl || "";
        const [summaryRes, integrationsRes] = await Promise.all([
          fetch(`${base}/api/summary`),
          fetch(`${base}/api/integrations`),
        ]);

        if (!summaryRes.ok || !integrationsRes.ok) {
          throw new Error(
            `BFF responded with ${summaryRes.status} / ${integrationsRes.status}`
          );
        }

        const [summaryData, integrationsData] = await Promise.all([
          summaryRes.json(),
          integrationsRes.json(),
        ]);

        if (activeRef.current) {
          setSummary(summaryData);
          setIntegrations(integrationsData);
          setLastUpdated(new Date());
          setError(null);
        }
      } catch (err) {
        if (activeRef.current) {
          setError(err.message || "Failed to reach BFF");
        }
      } finally {
        if (activeRef.current) {
          setLoading(false);
        }
      }
    }

    fetchData();
    const id = setInterval(fetchData, POLL_INTERVAL);

    return () => {
      activeRef.current = false;
      clearInterval(id);
    };
  }, [baseUrl]);

  return { summary, integrations, loading, error, lastUpdated };
}
