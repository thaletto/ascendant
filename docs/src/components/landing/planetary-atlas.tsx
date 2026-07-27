import { useEffect, useState } from "react";
import { ArrowDown } from "lucide-react";
import { DitheredPlanet } from "./dithered-planet";
import { landingCopy, workflowSteps, type LandingVariantProps } from "./landing-data";
import { InstallCommand } from "./install-command";
import { AtlasScroller } from "./atlas-scroller";
import {
  FinalCta,
  LandingActions,
  LandingFooter,
  ProofStrip,
} from "./shared";

export function PlanetaryAtlasLanding({ installCommand, sdkCommand, planets }: LandingVariantProps) {
  const saturn = planets.at(-1)!;
  const [showScrollCue, setShowScrollCue] = useState(true);

  useEffect(() => {
    let frameId = 0;

    const updateScrollCue = () => {
      const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
      const nextVisibility = scrollableHeight <= 0 || window.scrollY / scrollableHeight < 0.05;
      setShowScrollCue((isVisible) => (isVisible === nextVisibility ? isVisible : nextVisibility));
    };

    const requestUpdate = () => {
      cancelAnimationFrame(frameId);
      frameId = requestAnimationFrame(updateScrollCue);
    };

    updateScrollCue();
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener("scroll", requestUpdate);
      window.removeEventListener("resize", requestUpdate);
    };
  }, []);

  return (
    <main className="lp-page bg-background text-foreground">
      <section className="lp-hero relative min-h-[calc(100svh-4rem)] overflow-hidden">
        <DitheredPlanet
          src={saturn.src}
          alt="Saturn rendered as a dithered celestial atlas plate"
          className="lp-hero-planet absolute inset-0 size-full rounded-none"
          imageClassName="object-center"
          palette="cosmos"
          priority
          size={2.6}
        />
        <div className="lp-atlas-veil absolute inset-0" aria-hidden="true" />
        <div className="relative z-10 mx-auto flex min-h-[calc(100svh-4rem)] max-w-360 flex-col px-5 py-6 sm:px-8 lg:px-12">
          <div className="mt-auto pb-12 pt-28">
            <div>
              <h1 className="max-w-[12ch] text-[clamp(3.2rem,7vw,7.75rem)] font-medium leading-[0.9] tracking-[-0.075em] text-balance text-(--hero-foreground)">
                {landingCopy.headline}
              </h1>
              <p className="mt-7 max-w-[62ch] text-base leading-7 text-pretty text-(--hero-muted) sm:text-lg sm:leading-8">
                {landingCopy.subheadline}
              </p>
              <div className="mt-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                <LandingActions />
                <div className="w-full lg:ms-auto lg:w-md lg:self-end lg:translate-y-4.5">
                  <InstallCommand agentCommand={installCommand} sdkCommand={sdkCommand} />
                </div>
              </div>
            </div>
          </div>
          <a
            href="#atlas"
            className={`lp-hero-scroll inline-flex size-12 items-center justify-center self-end rounded-full transition-[opacity,transform] duration-200 ease-(--lp-ease-out) motion-reduce:transition-none active:scale-[0.96] ${
              showScrollCue ? "opacity-100" : "pointer-events-none translate-y-2 opacity-0"
            }`}
            aria-label="Explore the planetary atlas"
            aria-hidden={!showScrollCue}
            tabIndex={showScrollCue ? 0 : -1}
          >
            <ArrowDown aria-hidden="true" />
          </a>
        </div>
      </section>

      <ProofStrip className="mx-auto max-w-360 border-y border-border/70" />

      <section id="atlas" className="overflow-clip py-20 lg:py-28" aria-labelledby="atlas-title">
        <div className="px-5 sm:px-8 lg:px-12">
          <div className="mx-auto flex max-w-7xl flex-col gap-7 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <h2 id="atlas-title" className="max-w-[13ch] text-4xl font-medium leading-[1.02] tracking-[-0.055em] text-balance sm:text-6xl">
                Seven planets. Distinct roles.
              </h2>
            </div>
            <p className="max-w-[52ch] text-base leading-7 text-muted-foreground text-pretty">
              See how each planet shapes a different kind of astrological insight.
            </p>
          </div>
        </div>

        <AtlasScroller planets={planets} />
      </section>

      <section className="lp-method px-5 py-20 sm:px-8 lg:px-12 lg:py-28" aria-labelledby="atlas-method-title">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-10 lg:grid-cols-[0.75fr_1.25fr] lg:items-center">
            <div>
              <h2 id="atlas-method-title" className="max-w-[12ch] text-4xl font-medium leading-[1.02] tracking-[-0.055em] text-balance sm:text-6xl">
                Evidence moves in a clear sequence.
              </h2>
            </div>
            <div>
              {workflowSteps.map((step) => (
                <article key={step.number} className="grid gap-4 border-t border-(--method-rule) py-7 sm:grid-cols-[4rem_1fr]">
                  <span className="font-mono text-xs text-(--method-accent) tabular-nums">{step.number}</span>
                  <div>
                    <h3 className="text-xl font-medium tracking-[-0.035em]">{step.title}</h3>
                    <p className="mt-2 max-w-[58ch] text-sm leading-6 text-(--method-muted) text-pretty">{step.text}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <FinalCta />
      <LandingFooter />
    </main>
  );
}
