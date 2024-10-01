const express = require("express");
const path = require("path");

const app = express();
app.use(express.json());

// ===== Sub-service URLs =====
const FLOW_URL = process.env.FLOW_URL || "http://localhost:5678";
const ANALYTICS_URL = process.env.ANALYTICS_URL || "http://localhost:3030";
const CRM_URL = process.env.CRM_URL || "http://localhost:3000";
const DOCUSEAL_URL = process.env.DOCUSEAL_URL || "http://localhost:3004";
const HYPERSWITCH_API_URL = process.env.HYPERSWITCH_API_URL || "http://localhost:8180";
const GROWTHBOOK_URL = process.env.GROWTHBOOK_URL || "http://localhost:3100";
const MIROTALK_URL = process.env.MIROTALK_URL || "http://localhost:3400";
const DOCFORGE_URL = process.env.DOCFORGE_URL || "http://localhost:3002";
const MAILRADAR_URL = process.env.MAILRADAR_URL || "http://localhost:3003";
const MARKETHUB_URL = process.env.MARKETHUB_URL || "http://localhost:8080";

// ===== Health check for all services =====
app.get("/api/status", async (_req, res) => {
  const services = [
    { id: "flow", name: "FlowEngine", url: `${FLOW_URL}/healthz`, port: 81 },
    { id: "analytics", name: "Analytics", url: `${ANALYTICS_URL}/api/health`, port: 82 },
    { id: "crm", name: "CRM", url: `${CRM_URL}/api`, port: 83 },
    { id: "docuseal", name: "DocuSeal", url: `${DOCUSEAL_URL}/`, port: 84 },
    { id: "payments", name: "Payments", url: `${HYPERSWITCH_API_URL}/health`, port: 85 },
    { id: "experiments", name: "GrowthBook", url: `${GROWTHBOOK_URL}/`, port: 86 },
    { id: "voip", name: "MiroTalk", url: `${MIROTALK_URL}/`, port: 87 },
    { id: "docforge", name: "DocForge", url: `${DOCFORGE_URL}/`, port: 3002 },
    { id: "mailradar", name: "MailRadar", url: `${MAILRADAR_URL}/`, port: 3003 },
    { id: "markethub", name: "MarketHub", url: `${MARKETHUB_URL}/`, port: 8080 },
  ];
  const results = await Promise.all(
    services.map(async (svc) => {
      try {
        const ctrl = new AbortController();
        const t = setTimeout(() => ctrl.abort(), 3000);
        const r = await fetch(svc.url, { signal: ctrl.signal });
        clearTimeout(t);
        return { ...svc, status: r.ok ? "running" : "error" };
      } catch {
        return { ...svc, status: "offline" };
      }
    })
  );
  res.json(results);
});

// ===== Redirect old login route to home =====
app.get("/login", (_req, res) => res.redirect("/"));
app.get("/login.html", (_req, res) => res.redirect("/"));

// ===== Static files =====
app.use(express.static(path.join(__dirname, "public")));

// ===== SPA fallback: serve index.html for unmatched routes =====
app.get("*", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const PORT = process.env.PORT || 9090;
app.listen(PORT, () => console.log(`cx330o Sales Platform: http://localhost:${PORT}`));
