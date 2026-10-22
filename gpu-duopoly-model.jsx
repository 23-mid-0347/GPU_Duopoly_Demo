import React, { useState, useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, LineChart, Line
} from "recharts";
import { Cpu, Factory, GitBranch, SlidersHorizontal, ArrowDown } from "lucide-react";

// ---------- palette / tokens ----------
const COLORS = {
  bg: "#181B19",
  panel: "#20241F",
  panelAlt: "#262B25",
  line: "#3A413A",
  text: "#ECE8DE",
  mute: "#8F9A8C",
  gold: "#C79A56",
  teal: "#5FA8A0",
  warn: "#C2694F",
};

const FONT_IMPORT = `
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
`;

// ---------- illustrative calibration data (placeholder — swap for your team's sourced figures) ----------
const HIST = [
  { gen: "RTX 4080 / RX 7900XTX", nvPrice: 1199, amdPrice: 999, nvShare: 82, c1: 620, c2: 470 },
  { gen: "RTX 4070 / RX 7800XT", nvPrice: 599, amdPrice: 499, nvShare: 80, c1: 480, c2: 380 },
  { gen: "RTX 5080 / RX 9070XT", nvPrice: 999, amdPrice: 599, nvShare: 84, c1: 560, c2: 400 },
  { gen: "RTX 5070 / RX 9060XT", nvPrice: 549, amdPrice: 349, nvShare: 85, c1: 440, c2: 340 },
];
// c1/c2 above are illustrative die-size/wafer-cost proxies per generation — replace with your
// data lead's actual SemiAnalysis-style cost estimates once sourced.

// ---------- model math ----------
// Inverse demand: p1 = A - B*q1 - D*q2 ,  p2 = A - B*q2 - D*q1
// D/B is the substitutability index: 0 = independent monopolies, ->B = near-homogeneous goods

function cournot(A, B, D, c1, c2) {
  const k = D / (2 * B);
  const denom = 2 * B * (1 - k * k);
  const q1 = ((A - c1) - k * (A - c2)) / denom;
  const q2 = ((A - c2) - k * (A - c1)) / denom;
  const p1 = A - B * q1 - D * q2;
  const p2 = A - B * q2 - D * q1;
  return { q1, q2, p1, p2, m1: p1 - c1, m2: p2 - c2, pi1: (p1 - c1) * q1, pi2: (p2 - c2) * q2 };
}

function bertrand(A, B, D, c1, c2) {
  const m = D / (2 * B);
  const base1 = ((B - D) * A + B * c1) / (2 * B);
  const base2 = ((B - D) * A + B * c2) / (2 * B);
  const denom = 1 - m * m;
  const p1 = (base1 + m * base2) / denom;
  const p2 = (base2 + m * base1) / denom;
  const bsq = B * B - D * D;
  const q1 = ((B - D) * A - B * p1 + D * p2) / bsq;
  const q2 = ((B - D) * A - B * p2 + D * p1) / bsq;
  return { q1, q2, p1, p2, m1: p1 - c1, m2: p2 - c2, pi1: (p1 - c1) * q1, pi2: (p2 - c2) * q2 };
}

function capacityConstrainedCournot(A, B, D, c1, c2, q1cap) {
  const k = D / (2 * B);
  const q2 = (A - c2) / (2 * B) - k * q1cap;
  const p1 = A - B * q1cap - D * q2;
  const p2 = A - B * q2 - D * q1cap;
  return { q1: q1cap, q2, p1, p2, m1: p1 - c1, m2: p2 - c2, pi1: (p1 - c1) * q1cap, pi2: (p2 - c2) * q2 };
}

const fmt = (n) => n.toFixed(0);

// ---------- reusable bits ----------
function SectionLabel({ n, label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 18 }}>
      <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 13, color: COLORS.gold, letterSpacing: 1 }}>{n}</span>
      <span style={{ height: 1, width: 32, background: COLORS.line }} />
      <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 12, color: COLORS.mute, textTransform: "uppercase", letterSpacing: 2 }}>{label}</span>
    </div>
  );
}

function EqCard({ title, children, accent }) {
  return (
    <div style={{
      background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, borderRadius: 4,
      padding: "20px 22px", flex: 1, minWidth: 260
    }}>
      <div style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 600, fontSize: 16, color: accent, marginBottom: 12 }}>{title}</div>
      <div style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 13, color: COLORS.text, lineHeight: 1.9 }}>{children}</div>
    </div>
  );
}

function Slider({ label, value, min, max, step, onChange, unit = "", accent = COLORS.gold }) {
  return (
    <div style={{ marginBottom: 22 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontFamily: "'IBM Plex Mono', monospace", fontSize: 12.5, color: COLORS.mute, marginBottom: 8 }}>
        <span>{label}</span>
        <span style={{ color: accent }}>{value}{unit}</span>
      </div>
      <input
        type="range" min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ width: "100%", accentColor: accent, height: 4 }}
      />
    </div>
  );
}

export default function GPUDuopolyModel() {
  const A = 1400, B = 2.5;
  const [D, setD] = useState(1.2);
  const [c1, setC1] = useState(550); // NVIDIA marginal cost proxy
  const [c2, setC2] = useState(420); // AMD marginal cost proxy
  const [capOn, setCapOn] = useState(false);
  const [q1cap, setQ1cap] = useState(120);
  const [metric, setMetric] = useState("price");

  const cn = useMemo(() => cournot(A, B, D, c1, c2), [D, c1, c2]);
  const bt = useMemo(() => bertrand(A, B, D, c1, c2), [D, c1, c2]);
  const cap = useMemo(() => capacityConstrainedCournot(A, B, D, c1, c2, q1cap), [D, c1, c2, q1cap]);

  const metricKey = { price: ["p1", "p2"], quantity: ["q1", "q2"], margin: ["m1", "m2"] }[metric];
  const chartData = [
    { name: "NVIDIA", Cournot: cn[metricKey[0]], Bertrand: bt[metricKey[0]] },
    { name: "AMD", Cournot: cn[metricKey[1]], Bertrand: bt[metricKey[1]] },
  ];

  const substitutability = (D / B).toFixed(2);
  const marginGapCournot = (cn.m1 - cn.m2).toFixed(0);
  const marginGapBertrand = (bt.m1 - bt.m2).toFixed(0);

  // validation: run each historical generation's own cost proxies through the SAME
  // Cournot/Bertrand solutions, using the live substitutability slider, and compare to actual MSRP
  const validation = useMemo(() => HIST.map((h) => {
    const c = cournot(A, B, D, h.c1, h.c2);
    const b = bertrand(A, B, D, h.c1, h.c2);
    return {
      gen: h.gen.split(" / ")[0],
      Actual: h.nvPrice,
      Cournot: Math.round(c.p1),
      Bertrand: Math.round(b.p1),
    };
  }), [D]);

  const mae = (key) => (validation.reduce((s, r) => s + Math.abs(r.Actual - r[key]), 0) / validation.length).toFixed(0);
  const maeCournot = mae("Cournot");
  const maeBertrand = mae("Bertrand");
  const betterFit = maeCournot < maeBertrand ? "Cournot" : "Bertrand";

  return (
    <div style={{ background: COLORS.bg, color: COLORS.text, fontFamily: "'IBM Plex Sans', sans-serif", minHeight: "100%" }}>
      <style>{FONT_IMPORT}{`
        input[type=range] { -webkit-appearance: none; background: ${COLORS.line}; border-radius: 2px; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 14px; height: 14px; border-radius: 50%; background: currentColor; cursor: pointer; }
        .toggle-btn { font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; padding: 7px 14px; border-radius: 3px; border: 1px solid ${COLORS.line}; background: transparent; color: ${COLORS.mute}; cursor: pointer; transition: all .15s; }
        .toggle-btn.active { background: ${COLORS.gold}; color: #181B19; border-color: ${COLORS.gold}; font-weight: 600; }
      `}</style>

      {/* HERO */}
      <div style={{ minHeight: 420, display: "flex", flexDirection: "column", justifyContent: "center", padding: "80px 8vw 60px", borderBottom: `1px solid ${COLORS.line}` }}>
        <div style={{ fontFamily: "'IBM Plex Mono', monospace", color: COLORS.gold, fontSize: 13, letterSpacing: 2, marginBottom: 18 }}>
          GAME THEORY · DISCRETE GPU DUOPOLY
        </div>
        <h1 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: "clamp(32px, 5vw, 58px)", fontWeight: 700, lineHeight: 1.08, margin: 0, maxWidth: 780 }}>
          One wafer supply.<br />Two pricing strategies.
        </h1>
        <p style={{ color: COLORS.mute, fontSize: 16, maxWidth: 560, marginTop: 22, lineHeight: 1.6 }}>
          NVIDIA and AMD sell substitutable, not identical, GPUs. We model both as a Cournot
          (quantity) game and a Bertrand (price) game over the same demand system, calibrate it
          against real launch data, and let you re-solve the equilibrium live.
        </p>
        <div style={{ display: "flex", gap: 40, marginTop: 40, fontFamily: "'IBM Plex Mono', monospace" }}>
          <div>
            <div style={{ fontSize: 28, fontWeight: 600, color: COLORS.gold }}>${fmt(cn.p1)}</div>
            <div style={{ fontSize: 11.5, color: COLORS.mute, marginTop: 4 }}>NVIDIA price · Cournot, current params</div>
          </div>
          <div>
            <div style={{ fontSize: 28, fontWeight: 600, color: COLORS.teal }}>${fmt(bt.p1)}</div>
            <div style={{ fontSize: 11.5, color: COLORS.mute, marginTop: 4 }}>NVIDIA price · Bertrand, current params</div>
          </div>
        </div>
        <div style={{ marginTop: 46, display: "flex", alignItems: "center", gap: 8, color: COLORS.mute, fontSize: 12.5 }}>
          <ArrowDown size={14} /> scroll — the model below is live
        </div>
      </div>

      {/* SETUP */}
      <div style={{ padding: "70px 8vw", borderBottom: `1px solid ${COLORS.line}` }}>
        <SectionLabel n="01" label="the setup" />
        <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 26, fontWeight: 600, maxWidth: 640, marginTop: 0 }}>
          Differentiated demand, not homogeneous goods
        </h2>
        <p style={{ color: COLORS.mute, maxWidth: 640, lineHeight: 1.7, fontSize: 15 }}>
          Plain Bertrand assumes identical products — whoever's cheaper takes the whole market.
          That's obviously false here (AMD offers more VRAM per dollar and still holds under 20%
          share), so we use one linear demand system with a cross-price term <em>D</em> that both
          games share. <span style={{ color: COLORS.text }}>D / B</span> is the substitutability index:
          0 means the two firms behave like independent monopolies, and values approaching B mean
          the goods are almost interchangeable.
        </p>
        <div style={{ display: "flex", gap: 20, flexWrap: "wrap", marginTop: 30 }}>
          <EqCard title="Inverse demand" accent={COLORS.gold}>
            p₁ = A − B·q₁ − D·q₂<br />
            p₂ = A − B·q₂ − D·q₁
          </EqCard>
          <EqCard title="Cournot reaction" accent={COLORS.teal}>
            firms choose q₁, q₂ simultaneously<br />
            FOC: A − 2B·qᵢ − D·qⱼ − cᵢ = 0
          </EqCard>
          <EqCard title="Bertrand reaction" accent={COLORS.warn}>
            firms choose p₁, p₂ simultaneously<br />
            solved off the direct-demand inverse of the system above
          </EqCard>
        </div>
      </div>

      {/* CALIBRATION DATA */}
      <div style={{ padding: "70px 8vw", borderBottom: `1px solid ${COLORS.line}` }}>
        <SectionLabel n="02" label="calibration data" />
        <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 26, fontWeight: 600, marginTop: 0 }}>
          Launch-window prices, illustrative
        </h2>
        <p style={{ color: COLORS.mute, fontSize: 14, maxWidth: 620, marginBottom: 26 }}>
          Placeholder numbers — swap in your team's JPR share data and 10-K segment revenue, then
          regress quantity on own-price and rival-price per generation to get real B and D instead
          of the toy values used below.
        </p>
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={HIST}>
            <CartesianGrid stroke={COLORS.line} strokeDasharray="3 3" />
            <XAxis dataKey="gen" stroke={COLORS.mute} tick={{ fontSize: 11, fontFamily: "IBM Plex Mono" }} />
            <YAxis stroke={COLORS.mute} tick={{ fontSize: 11, fontFamily: "IBM Plex Mono" }} />
            <Tooltip contentStyle={{ background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, fontFamily: "IBM Plex Mono", fontSize: 12 }} />
            <Legend wrapperStyle={{ fontFamily: "IBM Plex Mono", fontSize: 12 }} />
            <Line type="monotone" dataKey="nvPrice" name="NVIDIA MSRP" stroke={COLORS.gold} strokeWidth={2} dot={{ r: 4 }} />
            <Line type="monotone" dataKey="amdPrice" name="AMD MSRP" stroke={COLORS.teal} strokeWidth={2} dot={{ r: 4 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* LIVE MODEL — interactive */}
      <div style={{ padding: "70px 8vw" }}>
        <SectionLabel n="03" label="live equilibrium — drag anything" />
        <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 26, fontWeight: 600, marginTop: 0 }}>
          What if the market were more — or less — competitive?
        </h2>
        <p style={{ color: COLORS.mute, fontSize: 14, maxWidth: 620, marginBottom: 30 }}>
          Move the sliders. Every value below — including the chart and the headline sentence — is
          recomputed from the closed-form Cournot and Bertrand solutions, not looked up from a table.
        </p>

        <div style={{ display: "flex", gap: 40, flexWrap: "wrap" }}>
          {/* controls */}
          <div style={{ flex: "1 1 300px", background: COLORS.panel, border: `1px solid ${COLORS.line}`, borderRadius: 4, padding: "24px 26px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20, color: COLORS.mute, fontSize: 12.5, fontFamily: "'IBM Plex Mono', monospace", textTransform: "uppercase", letterSpacing: 1.5 }}>
              <SlidersHorizontal size={14} /> parameters
            </div>
            <Slider label="Substitutability (D/B)" value={substitutability} min={0} max={2.3} step={0.05}
              onChange={setD} accent={COLORS.gold} />
            {/* note: slider drives D directly but label shows D/B for readability */}
            <input type="range" min={0} max={2.3} step={0.05} value={D} onChange={(e) => setD(parseFloat(e.target.value))} style={{ display: "none" }} />
            <Slider label="NVIDIA marginal cost proxy" value={c1} min={300} max={800} step={10} unit="" onChange={setC1} accent={COLORS.gold} />
            <Slider label="AMD marginal cost proxy" value={c2} min={300} max={800} step={10} unit="" onChange={setC2} accent={COLORS.teal} />

            <div style={{ height: 1, background: COLORS.line, margin: "22px 0" }} />

            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14, color: COLORS.mute, fontSize: 12.5, fontFamily: "'IBM Plex Mono', monospace", textTransform: "uppercase", letterSpacing: 1.5 }}>
              <Factory size={14} /> supply constraint
            </div>
            <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
              <button className={`toggle-btn ${!capOn ? "active" : ""}`} onClick={() => setCapOn(false)}>Unconstrained</button>
              <button className={`toggle-btn ${capOn ? "active" : ""}`} onClick={() => setCapOn(true)}>TSMC-capped</button>
            </div>
            {capOn && (
              <Slider label="NVIDIA fab allocation cap (units)" value={q1cap} min={20} max={220} step={5}
                onChange={setQ1cap} accent={COLORS.warn} />
            )}
          </div>

          {/* results */}
          <div style={{ flex: "2 1 420px" }}>
            <div style={{ display: "flex", gap: 8, marginBottom: 18 }}>
              {["price", "quantity", "margin"].map((m) => (
                <button key={m} className={`toggle-btn ${metric === m ? "active" : ""}`} onClick={() => setMetric(m)} style={{ textTransform: "capitalize" }}>
                  {m}
                </button>
              ))}
            </div>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={chartData}>
                <CartesianGrid stroke={COLORS.line} strokeDasharray="3 3" />
                <XAxis dataKey="name" stroke={COLORS.mute} tick={{ fontSize: 12, fontFamily: "IBM Plex Mono" }} />
                <YAxis stroke={COLORS.mute} tick={{ fontSize: 11, fontFamily: "IBM Plex Mono" }} />
                <Tooltip contentStyle={{ background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, fontFamily: "IBM Plex Mono", fontSize: 12 }} />
                <Legend wrapperStyle={{ fontFamily: "IBM Plex Mono", fontSize: 12 }} />
                <Bar dataKey="Cournot" fill={COLORS.gold} radius={[3, 3, 0, 0]} />
                <Bar dataKey="Bertrand" fill={COLORS.teal} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>

            <div style={{
              marginTop: 24, background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, borderRadius: 4,
              padding: "18px 22px", fontFamily: "'IBM Plex Mono', monospace", fontSize: 13.5, lineHeight: 1.8
            }}>
              At <span style={{ color: COLORS.gold }}>D/B = {substitutability}</span>, Cournot predicts a
              margin gap of <span style={{ color: COLORS.gold }}>${marginGapCournot}</span> (NVIDIA over AMD),
              while Bertrand predicts a gap of <span style={{ color: COLORS.teal }}>${marginGapBertrand}</span>.
              {capOn && (
                <> Capping NVIDIA's output at <span style={{ color: COLORS.warn }}>{q1cap} units</span> pushes
                  its equilibrium price to <span style={{ color: COLORS.warn }}>${fmt(cap.p1)}</span> and
                  AMD's to <span style={{ color: COLORS.warn }}>${fmt(cap.p2)}</span> — a real fab-allocation
                  constraint acts like a pre-committed Cournot quantity, which is the closest real-world
                  analogue to why NVIDIA doesn't just flood the market.</>
              )}
            </div>
          </div>
        </div>

      </div>

      {/* VALIDATION — predicted vs actual */}
      <div style={{ padding: "70px 8vw", borderTop: `1px solid ${COLORS.line}` }}>
        <SectionLabel n="04" label="predicted vs. actual" />
        <h2 style={{ fontFamily: "'Space Grotesk', sans-serif", fontSize: 26, fontWeight: 600, marginTop: 0 }}>
          Which model actually fits history?
        </h2>
        <p style={{ color: COLORS.mute, fontSize: 14, maxWidth: 640, marginBottom: 10 }}>
          Same equations, same substitutability slider from above — now run against each generation's
          own cost proxy instead of a single hypothetical firm. NVIDIA's actual launch MSRP is plotted
          against what Cournot and Bertrand would each have predicted at that D/B.
        </p>
        <p style={{ color: COLORS.mute, fontSize: 13, maxWidth: 640, marginBottom: 30, fontStyle: "italic" }}>
          Try dragging the substitutability slider in section 03 — this chart re-fits live.
        </p>

        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={validation}>
            <CartesianGrid stroke={COLORS.line} strokeDasharray="3 3" />
            <XAxis dataKey="gen" stroke={COLORS.mute} tick={{ fontSize: 11, fontFamily: "IBM Plex Mono" }} />
            <YAxis stroke={COLORS.mute} tick={{ fontSize: 11, fontFamily: "IBM Plex Mono" }} />
            <Tooltip contentStyle={{ background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, fontFamily: "IBM Plex Mono", fontSize: 12 }} />
            <Legend wrapperStyle={{ fontFamily: "IBM Plex Mono", fontSize: 12 }} />
            <Bar dataKey="Actual" fill={COLORS.text} radius={[3, 3, 0, 0]} />
            <Bar dataKey="Cournot" fill={COLORS.gold} radius={[3, 3, 0, 0]} />
            <Bar dataKey="Bertrand" fill={COLORS.teal} radius={[3, 3, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>

        <div style={{
          marginTop: 24, display: "flex", gap: 20, flexWrap: "wrap"
        }}>
          <div style={{ background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, borderRadius: 4, padding: "16px 20px", flex: 1, minWidth: 220 }}>
            <div style={{ fontSize: 11.5, color: COLORS.mute, fontFamily: "'IBM Plex Mono', monospace", textTransform: "uppercase", letterSpacing: 1 }}>Mean abs. error — Cournot</div>
            <div style={{ fontSize: 24, fontWeight: 600, color: COLORS.gold, fontFamily: "'Space Grotesk', sans-serif", marginTop: 6 }}>${maeCournot}</div>
          </div>
          <div style={{ background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, borderRadius: 4, padding: "16px 20px", flex: 1, minWidth: 220 }}>
            <div style={{ fontSize: 11.5, color: COLORS.mute, fontFamily: "'IBM Plex Mono', monospace", textTransform: "uppercase", letterSpacing: 1 }}>Mean abs. error — Bertrand</div>
            <div style={{ fontSize: 24, fontWeight: 600, color: COLORS.teal, fontFamily: "'Space Grotesk', sans-serif", marginTop: 6 }}>${maeBertrand}</div>
          </div>
          <div style={{ background: COLORS.panelAlt, border: `1px solid ${COLORS.line}`, borderRadius: 4, padding: "16px 20px", flex: 1, minWidth: 220 }}>
            <div style={{ fontSize: 11.5, color: COLORS.mute, fontFamily: "'IBM Plex Mono', monospace", textTransform: "uppercase", letterSpacing: 1 }}>Better fit at current D/B</div>
            <div style={{ fontSize: 24, fontWeight: 600, color: COLORS.warn, fontFamily: "'Space Grotesk', sans-serif", marginTop: 6 }}>{betterFit}</div>
          </div>
        </div>

        <p style={{ color: COLORS.mute, fontSize: 13, maxWidth: 640, marginTop: 22, lineHeight: 1.7 }}>
          If Cournot fits noticeably better across most of the D/B range, that's your quantitative
          case for the "wafer allocation constrains behavior more than price competition does" story —
          worth stating explicitly in the writeup rather than leaving it implicit in the chart.
        </p>

        <div style={{ marginTop: 50, padding: "18px 22px", border: `1px dashed ${COLORS.line}`, borderRadius: 4, color: COLORS.mute, fontSize: 13, display: "flex", gap: 10, alignItems: "flex-start" }}>
          <GitBranch size={15} style={{ marginTop: 2, flexShrink: 0 }} />
          <span>
            This is a structural prototype, not the final deliverable: A, B and every cost proxy here
            are placeholders. Replace them with your calibration lead's regression output and this page
            becomes the actual predicted-vs-actual and counterfactual engine for the writeup.
          </span>
        </div>
      </div>
    </div>
  );
}
