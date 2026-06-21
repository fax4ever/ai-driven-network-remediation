function StatusCard({ title, value }) {
  return (
    <article className="card">
      <p>{title}</p>
      <strong>{value}</strong>
    </article>
  );
}

function formatServiceNow(sn) {
  if (!sn) return "unknown";
  if (typeof sn === "string") return sn;
  const mode = sn.mode || "unknown";
  const reachable = sn.reachable ? "reachable" : "unreachable";
  return `${mode} / ${reachable}`;
}

export function StatusCards({ summary, integrations }) {
  return (
    <section className="grid">
      <StatusCard title="Agent Runtime" value={summary.agent_status || "unknown"} />
      <StatusCard title="Edge Site" value={summary.site || "edge-01"} />
      <StatusCard title="Open Incidents" value={String(summary.open_incidents || 0)} />
      <StatusCard
        title="MCP Availability"
        value={`${integrations.up || 0}/${integrations.total || 0} up`}
      />
      <StatusCard title="ServiceNow" value={formatServiceNow(summary.servicenow)} />
      <StatusCard title="Hub Cluster" value={summary.cluster || "hub"} />
    </section>
  );
}
