import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import {
  ArrowRight,
  ArrowUpRight,
  Check,
  Clock3,
  Code2,
  Orbit,
  Sparkles,
} from "lucide-react";
import { HomeLayout } from "fumadocs-ui/layouts/home";
import { DynamicCodeBlock } from "fumadocs-ui/components/dynamic-codeblock";
import { Tabs, Tab } from "fumadocs-ui/components/tabs";
import { ImageDithering } from "@paper-design/shaders-react";
import { baseOptions } from "@/lib/layout.shared";
import { ASCENDANT_VERSION } from "@/lib/shared";


export const Route = createFileRoute("/")({
  component: Home,
});

const installCommand = "pip install astro-ascendant";
const skillsCommand = "npx skills add thaletto/ascendant";

const resultCode = `{
  "mahadasha": {
    "mahadasha": "Saturn",
    "start": "07-02-2024",
    "end": "03-02-2043",
    "antardashas": [...]
  },
  "antardasha": {
    "mahadasha": "Saturn",
    "antardasha": "Saturn",
    "start": "07-02-2024",
    "end": "10-02-2027"
  }
}`;

const referenceItems = [
  {
    number: "01",
    title: "Agent workflows",
    text: "Install eleven skills for saved birth records, transits, domain readings, and evidence-aware responses.",
    href: "agents",
    meta: "Skills CLI",
  },
  {
    number: "02",
    title: "Divisional charts",
    text: "Generate the Rāśi and fifteen Vargas through D60 as structured, inspectable data.",
    href: "charts",
    meta: "16 charts",
  },
  {
    number: "03",
    title: "Vimshottari Dasha",
    text: "Build the complete 120-year planetary sequence or resolve the period active on a date.",
    href: "dasha",
    meta: "9 grahas",
  },
  {
    number: "04",
    title: "Classical yogas",
    text: "Detect named combinations, then inspect their presence, strength, type, and rationale.",
    href: "yoga",
    meta: "structured results",
  },
  {
    number: "05",
    title: "Ashtakavarga",
    text: "Calculate Bhinna and Sarva scores, reductions, and Shodhya Pinda as typed results.",
    href: "ashtakavarga",
    meta: "typed matrix",
  },
];

function ClientImageDithering() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (!mounted)
    return <div style={{ background: "var(--background)", height: "100%" }} />;

  return (
    <ImageDithering
      image="/moon.png"
      colorBack="#000c38"
      colorFront="#94ffaf"
      colorHighlight="#eaff94"
      originalColors={false}
      inverted={false}
      type="8x8"
      size={2}
      colorSteps={2}
      fit="cover"
      scale={1}
      style={{ width: "100%", height: "100%" }}
    />
  );
}

function Home() {
  return (
    <HomeLayout {...baseOptions()}>
      <main className="manual-home">
        <div className="manual-grid" aria-hidden="true" />

        {/* Hero Section with 50/50 Grid */}
        <section className="manual-hero">
          <div className="manual-kicker-row">
            <p>{ASCENDANT_VERSION}</p>
          </div>
          <div className="manual-hero-grid">
            {/* Left Side: Content */}
            <div className="manual-hero-content">
              <div className="manual-intro">
                <h1>Vedic astrology for Python and AI agents.</h1>
                <p className="manual-lede">
                  Compute charts, dashas, yogas, and Ashtakavarga locally. Use the
                  typed Python API or install eleven guided workflows into your
                  agent.
                </p>

                <Tabs items={["agent", "python"]} defaultValue="agent">              
                  <Tab key="agent" value="agent">
                    <DynamicCodeBlock 
                      code={skillsCommand} 
                      lang="bash" 
                      codeblock={{ className: "text-left" }} 
                    />
                  </Tab>
                  
                  <Tab key="python" value="python">
                    <DynamicCodeBlock 
                      code={installCommand} 
                      lang="bash" 
                      codeblock={{ className: "text-left" }} 
                    />
                  </Tab>
                </Tabs>

                <div className="manual-actions">
                  <Link
                    to="/docs/$"
                    params={{ _splat: "agents" }}
                    className="manual-primary-action"
                  >
                    Set up an agent <ArrowRight />
                  </Link>
                </div>

                <ul className="manual-trust">
                  <li>
                    <Check /> Typed results
                  </li>
                  <li>
                    <Check /> 11 agent skills
                  </li>
                  <li>
                    <Check /> No API key
                  </li>
                </ul>
              </div>
            </div>

            {/* Right Side: Dithered Image */}
            <div className="manual-hero-image">
              <ClientImageDithering />
            </div>
          </div>
        </section>

        {/* Facts Section */}
        <section className="manual-facts" aria-label="Library facts">
          <div>
            <strong>16</strong>
            <span>divisional charts</span>
          </div>
          <div>
            <strong>11</strong>
            <span>agent skills</span>
          </div>
          <div>
            <strong>7</strong>
            <span>ayanamsas</span>
          </div>
        </section>

        {/* Workflow Section */}
        <section className="manual-workflow" aria-labelledby="workflow-title">
          <div className="manual-section-label">
            <span>Method / 01</span>
            <p>Data in. Evidence out.</p>
          </div>
          <div className="manual-workflow-content">
            <h2 id="workflow-title">
              A calculation layer your agent can inspect.
            </h2>
            <p className="manual-section-lede">
              Ascendant keeps calculation and interpretation separate. The
              engine returns reproducible data; each skill tells the agent what
              to inspect, how to explain it, and where to stop.
            </p>
            <div className="manual-steps">
              <article>
                <span>01</span>
                <div>
                  <h3>Save the source data</h3>
                  <p>
                    The <code>init-person</code> skill records the birth time,
                    timezone, and coordinates before generating reusable chart
                    records.
                  </p>
                </div>
              </article>
              <article>
                <span>02</span>
                <div>
                  <h3>Compute before interpreting</h3>
                  <p>
                    Typed positions flow into houses, Vargas, dashas, yogas,
                    transits, and Ashtakavarga evidence.
                  </p>
                </div>
              </article>
              <article>
                <span>03</span>
                <div>
                  <h3>Apply a focused skill</h3>
                  <p>
                    Career, finance, health, relationship, and other workflows
                    turn the stored evidence into bounded, reviewable guidance.
                  </p>
                </div>
              </article>
            </div>
          </div>
        </section>

        {/* Reference Section */}
        <section className="manual-reference" aria-labelledby="reference-title">
          <div className="manual-section-label manual-section-label-light">
            <span>Reference / 02</span>
            <p>Start with the workflow you need.</p>
          </div>
          <div className="manual-reference-content">
            <div className="manual-reference-heading">
              <h2 id="reference-title">
                For applications.
                <br />
                For agents.
              </h2>
              <Link to="/docs/$" params={{ _splat: "" }}>
                Browse all documentation <ArrowRight aria-hidden="true" />
              </Link>
            </div>
            <div className="manual-reference-list">
              {referenceItems.map((item) => (
                <Link
                  key={item.href}
                  to="/docs/$"
                  params={{ _splat: item.href }}
                  className="manual-reference-item"
                >
                  <span className="manual-reference-number">{item.number}</span>
                  <div>
                    <h3>{item.title}</h3>
                    <p>{item.text}</p>
                  </div>
                  <div className="manual-reference-meta">
                    <span>{item.meta}</span>
                    <ArrowUpRight aria-hidden="true" />
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* Output Section */}
        <section className="manual-output" aria-labelledby="output-title">
          <div className="manual-section-label">
            <span>Output / 03</span>
            <p>Useful after the function returns.</p>
          </div>
          <div className="manual-output-content">
            <div className="manual-output-copy">
              <h2 id="output-title">Results agents can inspect.</h2>
              <p>
                No screenshot parsing and no hidden astrology endpoint. Agents
                can read stable values, trace a conclusion to its chart factors,
                and say when required evidence is missing.
              </p>
              <ul>
                <li>
                  <Orbit aria-hidden="true" /> Sidereal planetary positions
                </li>
                <li>
                  <Clock3 aria-hidden="true" /> Date-aware dasha lookup
                </li>
                <li>
                  <Sparkles aria-hidden="true" /> Yoga presence and strength
                </li>
                <li>
                  <Code2 aria-hidden="true" /> Plain Python structures
                </li>
              </ul>
            </div>
            <DynamicCodeBlock
              codeblock={{ className: "text-left" }}
              code={resultCode}
              lang="json"
            />
          </div>
        </section>

        {/* Final CTA Section */}
        <section className="manual-final-cta" aria-labelledby="final-cta-title">
          <div>
            <span>Portable agent workflows</span>
            <h2 id="final-cta-title">Add a chart engine to your agent.</h2>
          </div>
          <div className="manual-final-actions">
            <Link
              to="/docs/$"
              params={{ _splat: "agents" }}
              className="manual-primary-action manual-primary-action-light"
            >
              Install agent skills
              <ArrowRight aria-hidden="true" />
            </Link>
            <p>Skills CLI + Codex.</p>
          </div>
        </section>

        {/* Footer */}
        <footer className="manual-footer">
          <div>
            <p>
              <strong>Ascendant</strong>
              <br />
              Vedic astrology, expressed as code.
            </p>
          </div>
          <div className="manual-footer-links">
            <Link to="/docs/$" params={{ _splat: "" }}>
              Documentation
            </Link>
            <a href="https://github.com/thaletto/ascendant">GitHub</a>
            <a href="https://pypi.org/project/astro-ascendant/">PyPI</a>
            <a href="https://github.com/thaletto/ascendant/blob/main/LICENSE">
              AGPL-3.0 license
            </a>
          </div>
        </footer>

        <Link
          to="/docs/$"
          params={{ _splat: "agents" }}
          className="manual-mobile-cta"
        >
          Set up an agent
          <ArrowRight aria-hidden="true" />
        </Link>
      </main>
    </HomeLayout>
  );
}