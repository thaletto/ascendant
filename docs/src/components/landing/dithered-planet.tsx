import { lazy, Suspense, useEffect, useRef, useState } from "react";
import type { ImageDitheringProps } from "@paper-design/shaders-react";
import { cn } from "@/lib/utils";

const LazyImageDithering = lazy(() =>
  import("@paper-design/shaders-react").then((module) => ({
    default: module.ImageDithering,
  })),
);

type DitherPalette = "paper" | "cosmos" | "signal";

export interface DitheredPlanetProps {
  src: string;
  alt: string;
  className?: string;
  imageClassName?: string;
  fit?: ImageDitheringProps["fit"];
  palette?: DitherPalette;
  size?: number;
  scale?: number;
  priority?: boolean;
}
const paletteTokens: Record<DitherPalette, [string, string, string]> = {
  paper: ["--dither-paper-back", "--dither-paper-front", "--dither-paper-highlight"],
  cosmos: ["--dither-cosmos-back", "--dither-cosmos-front", "--dither-cosmos-highlight"],
  signal: ["--dither-signal-back", "--dither-signal-front", "--dither-signal-highlight"],
};

function cssTokenToRgb(token: string) {
  const styles = getComputedStyle(document.documentElement);
  let value = styles.getPropertyValue(token).trim();
  const reference = value.match(/^var\((--[^,\s)]+)/)?.[1];
  if (reference) value = styles.getPropertyValue(reference).trim();
  const canvas = document.createElement("canvas");
  canvas.width = 1;
  canvas.height = 1;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  if (!context) return "rgb(0, 0, 0)";

  context.fillStyle = value;
  context.fillRect(0, 0, 1, 1);
  const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;
  return `rgb(${red}, ${green}, ${blue})`;
}

function resolvePalette(palette: DitherPalette) {
  const [back, front, highlight] = paletteTokens[palette];
  return {
    back: cssTokenToRgb(back),
    front: cssTokenToRgb(front),
    highlight: cssTokenToRgb(highlight),
  };
}

export function DitheredPlanet({
  src,
  alt,
  className,
  imageClassName,
  fit = "cover",
  palette = "paper",
  size = 2,
  scale = 1,
  priority = false,
}: DitheredPlanetProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isNearViewport, setIsNearViewport] = useState(false);
  const [colors, setColors] = useState<ReturnType<typeof resolvePalette> | null>(null);

  useEffect(() => {
    const element = containerRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => setIsNearViewport(entry.isIntersecting),
      { rootMargin: priority ? "320px" : "120px" },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, [priority]);

  useEffect(() => {
    const root = document.documentElement;
    const updateColors = () => setColors(resolvePalette(palette));
    const observer = new MutationObserver(updateColors);
    updateColors();
    observer.observe(root, { attributes: true, attributeFilter: ["class"] });
    return () => observer.disconnect();
  }, [palette]);

  const renderShader = isNearViewport && colors;

  return (
    <div
      ref={containerRef}
      className={cn("lp-dither-frame relative isolate overflow-hidden", className)}
    >
      <img
        src={src}
        alt={alt}
        className={cn("size-full object-cover", imageClassName)}
        loading={priority ? "eager" : "lazy"}
        fetchPriority={priority ? "high" : "auto"}
      />
      {renderShader ? (
        <Suspense fallback={null}>
          <LazyImageDithering
            aria-hidden="true"
            image={src}
            colorBack={colors.back}
            colorFront={colors.front}
            colorHighlight={colors.highlight}
            originalColors={false}
            inverted={false}
            type="8x8"
            size={size}
            colorSteps={3}
            fit={fit}
            scale={scale}
            maxPixelCount={1_200_000}
            className="absolute inset-0 size-full"
            style={{ width: "100%", height: "100%" }}
          />
        </Suspense>
      ) : null}
      <span className="lp-image-outline pointer-events-none absolute inset-0" aria-hidden="true" />
    </div>
  );
}
