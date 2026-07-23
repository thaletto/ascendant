import jupiter from "../../../assets/planets/jupiter.png";
import mars from "../../../assets/planets/mars.png";
import mercury from "../../../assets/planets/mercury.png";
import moon from "../../../assets/planets/moon.png";
import saturn from "../../../assets/planets/saturn.png";
import sun from "../../../assets/planets/sun.png";
import venus from "../../../assets/planets/venus.png";

export interface PlanetAsset {
  name: string;
  src: string;
  workflow: string;
  detail: string;
  description: string;
  themes: string[];
}

export interface LandingVariantProps {
  installCommand: string;
  sdkCommand: string;
  planets: PlanetAsset[];
}

export const landingCopy = {
  headline: "Astrology skills and tools your agent needs.",
  subheadline:
    "Astrology calculations your agent can trace and explain.",
  primaryCta: "Install agent skills",
  secondaryCta: "Explore the Python SDK",
};

export const installCommand = "npx skills add thaletto/ascendant";
export const sdkCommand = "pip install astro-ascendant";

export const proofPoints = [
  { value: "11", label: "agent skills" },
  { value: "16", label: "divisional charts" },
  { value: "7", label: "ayanamsas" },
  { value: "200+", label: "classical yogas" },
] as const;

export const workflowSteps = [
  {
    number: "01",
    title: "Record the source",
    text: "Capture birth time, timezone, and coordinates once, then keep the generated chart records available to every focused workflow.",
  },
  {
    number: "02",
    title: "Calculate before interpreting",
    text: "Typed Python results establish positions, houses, Vargas, dashas, yogas, transits, and Ashtakavarga evidence.",
  },
  {
    number: "03",
    title: "Apply a bounded skill",
    text: "Career, finance, health, education, property, family, and relationship skills explain what the evidence supports and where it stops.",
  },
] as const;

export const documentationLinks = [
  {
    number: "01",
    title: "Agent workflows",
    description: "Install the complete skill pack and create the first saved birth record.",
    href: "agents",
    meta: "11 skills",
  },
  {
    number: "02",
    title: "Divisional charts",
    description: "Generate Rāśi and fifteen Vargas through D60 as inspectable data.",
    href: "charts",
    meta: "16 charts",
  },
  {
    number: "03",
    title: "Vimshottari Dasha",
    description: "Resolve the planetary period active on a date or build the full timeline.",
    href: "dasha",
    meta: "120 years",
  },
  {
    number: "04",
    title: "Classical yogas",
    description: "Inspect named combinations, presence, strength, type, and rationale.",
    href: "yoga",
    meta: "structured",
  },
] as const;

export const planets: PlanetAsset[] = [
  { name: "Sun", src: sun, workflow: "Lead", detail: "Direction and authority", description: "Sun frames career questions through calculated houses, planets, Vargas, and dashas before the skill explains what those findings support.", themes: ["Soul", "Authority"] },
  { name: "Moon", src: moon, workflow: "Feel", detail: "A reusable foundation", description: "Moon anchors the stored birth record: time, place, timezone, and the calculated chart that every later skill can inspect.", themes: ["Mind", "Emotion"] },
  { name: "Mars", src: mars, workflow: "Act", detail: "Action and fixed assets", description: "Mars focuses the property workflow on fixed-assets evidence, so an agent can show the calculated basis before discussing timing or action.", themes: ["Energy", "Ambition"] },
  { name: "Mercury", src: mercury, workflow: "Think", detail: "Learning and analysis", description: "Mercury opens the education workflow, which narrows a complete chart into evidence about study, learning style, and analytical strengths.", themes: ["Intellect", "Communication"] },
  { name: "Venus", src: venus, workflow: "Relate", detail: "Compatibility evidence", description: "Venus leads relationship analysis with clear evidence boundaries, keeping chart themes separate from consent, intent, and lived behavior.", themes: ["Desire", "Harmony"] },
  { name: "Jupiter", src: jupiter, workflow: "Expand", detail: "Promise before timing", description: "Jupiter guides finance work from natal promise to periods and transits, keeping the rationale inspectable instead of reducing it to a prediction.", themes: ["Wisdom", "Expansion"] },
  { name: "Saturn", src: saturn, workflow: "Endure", detail: "Dated planetary context", description: "Saturn represents dated transit context: a local calculation gives an agent a precise snapshot to explain against the saved chart record.", themes: ["Discipline", "Destiny"] },
];
