import { useEffect, useRef, useState } from "react";
import { Stepper, useAutoPlay } from "pasito/react";
import "pasito/styles.css";
import type { PlanetAsset } from "./landing-data";
import { DitheredPlanet } from "./dithered-planet";

interface AtlasScrollerProps {
  planets: PlanetAsset[];
}

export function AtlasScroller({ planets }: AtlasScrollerProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [isPillFilling, setIsPillFilling] = useState(false);
  const hasStartedAutoplay = useRef(false);
  const activePlanet = planets[activeIndex];
  const { playing, toggle, filling, fillDuration } = useAutoPlay({
    count: planets.length,
    active: activeIndex,
    onStepChange: setActiveIndex,
    stepDuration: 5_000,
    loop: true,
    enabled: true,
  });

  useEffect(() => {
    if (!hasStartedAutoplay.current && !playing) {
      hasStartedAutoplay.current = true;
      toggle();
    }
  }, [playing, toggle]);

  useEffect(() => {
    if (!filling) {
      setIsPillFilling(false);
      return;
    }

    setIsPillFilling(false);
    const frame = requestAnimationFrame(() => setIsPillFilling(true));
    return () => cancelAnimationFrame(frame);
  }, [activeIndex, filling]);

  return (
    <div className="mt-12">
      <article className="mx-auto grid max-w-7xl gap-8 px-5 pb-6 sm:px-8 lg:grid-cols-[minmax(0,0.95fr)_minmax(20rem,0.65fr)] lg:items-start lg:gap-16 lg:px-12">
        <div>
          <DitheredPlanet
            src={activePlanet.src}
            alt={`${activePlanet.name} rendered as a dithered atlas plate`}
            className="aspect-square rounded-[1.5rem]"
            palette="signal"
            size={2.4}
            scale={1.08}
            priority={activeIndex === 0}
          />
          <div className="mt-4 flex justify-center">
            <Stepper
              count={planets.length}
              active={activeIndex}
              onStepClick={setActiveIndex}
              transitionDuration={240}
              easing="cubic-bezier(0.22, 1, 0.36, 1)"
              filling={filling && isPillFilling}
              fillDuration={fillDuration}
              className="lp-atlas-stepper"
            />
          </div>
        </div>
        <div aria-live="polite">
          <p className="font-mono text-lg font-medium uppercase tracking-[0.08em] text-celestial">
            {activePlanet.name}
          </p>
          <h3 className="mt-4 text-3xl font-medium leading-none tracking-tighter sm:text-5xl">{activePlanet.workflow}</h3>
          <p className="mt-4 text-base leading-7 text-muted-foreground text-pretty">{activePlanet.description}</p>
          <ul className="mt-6 flex flex-wrap gap-2" aria-label={`${activePlanet.name} themes`}>
            {activePlanet.themes.map((theme) => (
              <li key={theme} className="rounded-full bg-muted px-3 py-1.5 font-mono text-[0.65rem] uppercase tracking-widest text-muted-foreground">
                {theme}
              </li>
            ))}
          </ul>
        </div>
      </article>
    </div>
  );
}
