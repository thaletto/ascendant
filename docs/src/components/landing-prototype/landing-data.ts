import jupiter from "../../../assets/jupiter.png";
import mars from "../../../assets/mars.webp";
import mercury from "../../../assets/mercury.png";
import moon from "../../../assets/moon.png";
import saturn from "../../../assets/saturn.jpg";
import sun from "../../../assets/sun.jpg";
import venus from "../../../assets/venus.jpg";

export interface PlanetAsset {
  name: string;
  src: string;
  workflow: string;
  detail: string;
}

export interface LandingVariantProps {
  version: string;
  installCommand: string;
  sdkCommand: string;
  planets: PlanetAsset[];
}

export const landingCopy = {
  headline: "Give your agent an astrology engine it can explain.",
  subheadline:
    "Install guided workflows backed by local Python calculations, structured chart data, and explicit evidence boundaries—without relying on a hosted astrology API.",
  primaryCta: "Install agent skills",
  secondaryCta: "Explore the Python SDK",
};

export const installCommand = "npx skills add thaletto/ascendant";
export const sdkCommand = "pip install astro-ascendant";

export const proofPoints = [
  { value: "11", label: "agent skills" },
  { value: "16", label: "divisional charts" },
  { value: "7", label: "ayanamsas" },
  { value: "Local", label: "no hosted API" },
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
    text: "Career, finance, health, education, property, family, and relationship skills explain what the evidence supports—and where it stops.",
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
  { name: "Moon", src: moon, workflow: "Birth record", detail: "A reusable foundation" },
  { name: "Mercury", src: mercury, workflow: "Education", detail: "Learning and analysis" },
  { name: "Venus", src: venus, workflow: "Relationships", detail: "Compatibility evidence" },
  { name: "Sun", src: sun, workflow: "Career", detail: "Direction and authority" },
  { name: "Mars", src: mars, workflow: "Property", detail: "Action and fixed assets" },
  { name: "Jupiter", src: jupiter, workflow: "Finance", detail: "Promise before timing" },
  { name: "Saturn", src: saturn, workflow: "Daily transit", detail: "Dated planetary context" },
];
