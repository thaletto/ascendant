import type { ReactNode } from "react";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import { documentationLinks, landingCopy, proofPoints } from "./landing-data";

export function Eyebrow({ children, inverse = false }: { children: ReactNode; inverse?: boolean }) {
  return (
    <p className={cn("lp-eyebrow", inverse && "text-celestial-soft")}>{children}</p>
  );
}

export function LandingActions({ inverse = false }: { inverse?: boolean }) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      <Button
        render={<Link to="/docs/$" params={{ _splat: "agents" }} />}
        className={cn(
          "h-12 rounded-xl px-5 text-sm font-semibold shadow-[0_0.75rem_2rem_color-mix(in_oklch,var(--foreground)_16%,transparent)] active:scale-[0.96]",
          inverse && "bg-cosmos-foreground text-cosmos hover:bg-cosmos-foreground/90",
        )}
      >
        {landingCopy.primaryCta}
        <ArrowRight aria-hidden="true" />
      </Button>
      <Button
        render={<Link to="/docs/$" params={{ _splat: "" }} />}
        variant="outline"
        className={cn(
          "h-12 rounded-xl border-border/70 bg-transparent px-4 text-sm active:scale-[0.96]",
          inverse && "border-cosmos-foreground/30 text-cosmos-foreground hover:bg-white/10 hover:text-cosmos-foreground",
        )}
      >
        {landingCopy.secondaryCta}
        <ArrowUpRight aria-hidden="true" />
      </Button>
    </div>
  );
}

export function ProofStrip({ inverse = false, className }: { inverse?: boolean; className?: string }) {
  return (
    <div className={cn("grid grid-cols-2 lg:grid-cols-4", className)}>
      {proofPoints.map((point, index) => (
        <div
          key={point.label}
          className={cn(
            "px-5 py-6 sm:px-7",
            index % 2 !== 0 && "border-s border-border/70",
            index > 1 && "border-t border-border/70 lg:border-t-0",
            index > 0 && "lg:border-s lg:border-border/70",
            inverse && "border-white/12",
          )}
        >
          <strong className="block text-2xl font-medium tracking-[-0.045em] tabular-nums sm:text-3xl">
            {point.value}
          </strong>
          <span className={cn("mt-1 block text-sm text-muted-foreground", inverse && "text-cosmos-muted")}>{point.label}</span>
        </div>
      ))}
    </div>
  );
}

export function DocumentationCards({ inverse = false }: { inverse?: boolean }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {documentationLinks.map((item) => (
        <Card
          key={item.href}
          className={cn(
            "rounded-2xl py-0 transition-[transform,box-shadow] duration-200 ease-(--lp-ease-out) hover:-translate-y-0.5 hover:shadow-lg",
            inverse && "bg-white/5 text-cosmos-foreground ring-white/12",
          )}
        >
          <Link
            to="/docs/$"
            params={{ _splat: item.href }}
            className="flex min-h-48 flex-col p-6 no-underline active:scale-[0.98]"
          >
            <div className="flex items-center justify-between gap-4">
              <span className="font-mono text-xs text-celestial tabular-nums">{item.number}</span>
              <span className={cn("text-xs uppercase tracking-[0.12em] text-muted-foreground", inverse && "text-cosmos-muted")}>{item.meta}</span>
            </div>
            <div className="mt-auto pt-10">
              <h3 className="text-xl font-medium tracking-[-0.035em]">{item.title}</h3>
              <p className={cn("mt-2 max-w-[42ch] text-sm leading-6 text-muted-foreground text-pretty", inverse && "text-cosmos-muted")}>{item.description}</p>
            </div>
          </Link>
        </Card>
      ))}
    </div>
  );
}

export function FinalCta({ inverse = false }: { inverse?: boolean }) {
  return (
    <section className={cn("px-5 py-20 sm:px-8 lg:px-12 lg:py-28", inverse && "bg-cosmos text-cosmos-foreground")}>
      <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <h2 className="max-w-[15ch] text-4xl font-medium leading-[1.02] tracking-[-0.055em] text-balance sm:text-6xl">
            Build on reliable astrology intelligence.
          </h2>
        </div>
        <LandingActions inverse={inverse} />
      </div>
    </section>
  );
}

export function LandingFooter({ inverse = false }: { inverse?: boolean }) {
  return (
    <footer className={cn("px-5 py-10 sm:px-8 lg:px-12", inverse && "bg-cosmos text-cosmos-foreground")}>
      <Separator className={cn("mb-8", inverse && "bg-white/12")} />
      <div className="mx-auto flex max-w-7xl flex-col gap-8 sm:flex-row sm:items-end sm:justify-between">
        <p className={cn("max-w-xs text-sm leading-6 text-muted-foreground", inverse && "text-cosmos-muted")}>
          <span className="wordmark mb-2 block">Ascendant</span>
          Reliable astrology intelligence for agents.
        </p>
        <nav className="flex flex-wrap gap-x-5 gap-y-2 text-sm" aria-label="Footer">
          <Link to="/docs/$" params={{ _splat: "" }}>Documentation</Link>
          <a href="https://github.com/thaletto/ascendant">GitHub</a>
          <a href="https://pypi.org/project/astro-ascendant/">PyPI</a>
          <a href="https://github.com/thaletto/ascendant/blob/main/LICENSE">AGPL-3.0</a>
        </nav>
      </div>
    </footer>
  );
}
