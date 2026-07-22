import { ArrowDown, ArrowRight } from "lucide-react";
import { Link } from "@tanstack/react-router";
import { Separator } from "@/components/ui/separator";
import { DitheredPlanet } from "./dithered-planet";
import { landingCopy, workflowSteps, type LandingVariantProps } from "./landing-data";
import { InstallCommand } from "./install-command";
import {
  DocumentationCards,
  Eyebrow,
  FinalCta,
  LandingActions,
  LandingFooter,
  MobileCta,
  ProofStrip,
} from "./shared";

export function PlanetaryAtlasLanding({ installCommand, sdkCommand, planets }: LandingVariantProps) {
  const saturn = planets.at(-1)!;

  return (
    <main className="lp-page bg-background text-foreground">
      <section className="relative min-h-[calc(100svh-4rem)] overflow-hidden bg-cosmos text-cosmos-foreground">
        <DitheredPlanet
          src={saturn.src}
          alt="Saturn rendered as a dithered celestial atlas plate"
          className="absolute inset-0 size-full rounded-none opacity-70"
          imageClassName="object-center"
          palette="cosmos"
          priority
          size={2.6}
          scale={1.14}
        />
        <div className="lp-atlas-veil absolute inset-0" aria-hidden="true" />
        <div className="relative z-10 mx-auto flex min-h-[calc(100svh-4rem)] max-w-[90rem] flex-col px-5 py-6 sm:px-8 lg:px-12">
          <div className="mt-auto grid gap-10 pb-12 pt-28 lg:grid-cols-[1fr_25rem] lg:items-end">
            <div>
              <Eyebrow inverse>Local calculations. Guided interpretation.</Eyebrow>
              <h1 className="mt-6 max-w-[12ch] text-[clamp(3.2rem,7vw,7.75rem)] font-medium leading-[0.9] tracking-[-0.075em] text-balance">
                {landingCopy.headline}
              </h1>
              <p className="mt-7 max-w-[62ch] text-base leading-7 text-cosmos-muted text-pretty sm:text-lg sm:leading-8">
                {landingCopy.subheadline}
              </p>
              <div className="mt-8">
                <LandingActions inverse />
              </div>
            </div>
            <InstallCommand agentCommand={installCommand} sdkCommand={sdkCommand} className="bg-background text-foreground" />
          </div>
          <a href="#atlas" className="inline-flex size-12 items-center justify-center self-end rounded-full bg-white/8 text-cosmos-foreground outline outline-1 outline-white/12 transition-transform duration-200 ease-[var(--lp-ease-out)] active:scale-[0.96]" aria-label="Explore the planetary atlas">
            <ArrowDown aria-hidden="true" />
          </a>
        </div>
      </section>

      <ProofStrip className="mx-auto max-w-[90rem] border-x border-b border-border/70" />

      <section id="atlas" className="overflow-hidden py-20 lg:py-28" aria-labelledby="atlas-title">
        <div className="px-5 sm:px-8 lg:px-12">
          <div className="mx-auto flex max-w-7xl flex-col gap-7 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <Eyebrow>Atlas / 01</Eyebrow>
              <h2 id="atlas-title" className="mt-5 max-w-[13ch] text-4xl font-medium leading-[1.02] tracking-[-0.055em] text-balance sm:text-6xl">
                One engine. Focused ways to read it.
              </h2>
            </div>
            <p className="max-w-[52ch] text-base leading-7 text-muted-foreground text-pretty">
              Every workflow starts from the same calculated record, then narrows the evidence to the question at hand.
            </p>
          </div>
        </div>

        <div className="lp-atlas-scroll mt-12 flex snap-x snap-mandatory gap-4 overflow-x-auto px-[max(1.25rem,calc((100vw-80rem)/2))] pb-6 sm:gap-6">
          {planets.map((planet, index) => (
            <article key={planet.name} className="w-[82vw] max-w-[30rem] shrink-0 snap-center">
              <DitheredPlanet
                src={planet.src}
                alt={`${planet.name} rendered as a dithered atlas plate`}
                className="aspect-[4/5] rounded-[1.5rem]"
                palette={index % 2 === 0 ? "paper" : "signal"}
                size={2.4}
                scale={1.08}
              />
              <div className="grid grid-cols-[2.5rem_1fr_auto] items-start gap-3 px-1 pt-5">
                <span className="font-mono text-xs text-celestial tabular-nums">{String(index + 1).padStart(2, "0")}</span>
                <div>
                  <h3 className="text-xl font-medium tracking-[-0.035em]">{planet.workflow}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{planet.detail}</p>
                </div>
                <span className="font-mono text-xs uppercase tracking-[0.12em] text-muted-foreground">{planet.name}</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="bg-cosmos px-5 py-20 text-cosmos-foreground sm:px-8 lg:px-12 lg:py-28" aria-labelledby="atlas-method-title">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr]">
            <div>
              <Eyebrow inverse>Orbit / 02</Eyebrow>
              <h2 id="atlas-method-title" className="mt-5 max-w-[12ch] text-4xl font-medium leading-[1.02] tracking-[-0.055em] text-balance sm:text-6xl">
                Evidence moves in a clear sequence.
              </h2>
            </div>
            <div>
              {workflowSteps.map((step) => (
                <article key={step.number} className="grid gap-4 border-t border-white/12 py-7 sm:grid-cols-[4rem_1fr]">
                  <span className="font-mono text-xs text-celestial-soft tabular-nums">{step.number}</span>
                  <div>
                    <h3 className="text-xl font-medium tracking-[-0.035em]">{step.title}</h3>
                    <p className="mt-2 max-w-[58ch] text-sm leading-6 text-cosmos-muted text-pretty">{step.text}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="px-5 py-20 sm:px-8 lg:px-12 lg:py-28" aria-labelledby="atlas-reference-title">
        <div className="mx-auto max-w-7xl">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <Eyebrow>Charts / 03</Eyebrow>
              <h2 id="atlas-reference-title" className="mt-5 text-4xl font-medium tracking-[-0.055em] sm:text-6xl">Choose a starting point.</h2>
            </div>
            <Link to="/docs/$" params={{ _splat: "" }} className="inline-flex min-h-11 items-center gap-2 text-sm underline decoration-from-font underline-offset-4">
              Browse all documentation <ArrowRight className="size-4" aria-hidden="true" />
            </Link>
          </div>
          <Separator className="my-10" />
          <DocumentationCards />
        </div>
      </section>

      <FinalCta />
      <LandingFooter />
      <MobileCta />
    </main>
  );
}
