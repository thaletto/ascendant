import { createFileRoute, Link } from '@tanstack/react-router';
import { HomeLayout } from 'fumadocs-ui/layouts/home';
import { ArrowRight, ChartPie, Clock3, List } from 'lucide-react';
import SideRays from '@/components/side-rays';
import { buttonVariants } from '@/components/ui/button';
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { baseOptions } from '@/lib/layout.shared';
import moonImage from '../../assets/moon.png';

export const Route = createFileRoute('/')({
  component: Home,
});

function Home() {
  return (
    <HomeLayout {...baseOptions()}>
      <main className="asc-home">
        <SideRays
          className="asc-side-rays"
          speed={0.35}
          rayColor1="#ffffff"
          rayColor2="#ffffff"
          darkRayColor1="#ffffff"
          darkRayColor2="#ffffff"
          intensity={2.2}
          spread={1.65}
          origin="top-right"
          tilt={-5}
          saturation={0}
          blend={0.48}
          falloff={1.5}
          opacity={0.85}
        />
        <section className="asc-hero">
          <div className="asc-hero-copy">
            <h1>
              Read the sky.
              <span>Write the logic.</span>
            </h1>
            <p className="asc-lede">
              Precise charts, planetary periods, and classical yogas.
            </p>
            <div className="asc-actions">
              <Link
                to="/docs/$"
                params={{ _splat: '' }}
                className={buttonVariants({ size: 'lg' })}
              >
                Read the docs
                <ArrowRight data-icon="inline-end" aria-hidden="true" />
              </Link>
              <a
                href="https://github.com/thaletto/ascendant"
                className={buttonVariants({ variant: 'outline', size: 'lg' })}
              >
                View on GitHub
              </a>
            </div>
          </div>

          <div className="asc-lunar-stage" aria-hidden="true">
            <div className="asc-lunar-halo" />
            <img className="asc-moon" src={moonImage} alt="" />
            <div className="asc-lunar-axis asc-lunar-axis-horizontal" />
            <div className="asc-lunar-axis asc-lunar-axis-vertical" />
            <span className="asc-lunar-glyph asc-lunar-glyph-moon">☽</span>
            <span className="asc-lunar-glyph asc-lunar-glyph-node">☊</span>
            <span className="asc-coordinate asc-coordinate-top">MOON · 18° 42′</span>
            <span className="asc-coordinate asc-coordinate-bottom">NAKSHATRA · ROHINI</span>
          </div>
        </section>

        <Separator className="asc-section-separator" />

        <section className="asc-capabilities" aria-labelledby="capabilities-heading">
          <div className="asc-section-heading">
            <span>One birth moment</span>
            <h2 id="capabilities-heading">A complete computational foundation.</h2>
          </div>
          <div className="asc-card-grid">
            <Link to="/docs/$" params={{ _splat: 'charts' }} className="asc-card-link">
              <Card className="asc-card">
                <CardHeader>
                  <ChartPie aria-hidden="true" />
                  <CardAction><ArrowRight aria-hidden="true" /></CardAction>
                </CardHeader>
                <CardContent>
                  <CardTitle>Divisional charts</CardTitle>
                  <CardDescription>Calculate sixteen Vargas, from the natal Rāśi to the Shastyamsa.</CardDescription>
                </CardContent>
              </Card>
            </Link>
            <Link to="/docs/$" params={{ _splat: 'dasha' }} className="asc-card-link">
              <Card className="asc-card">
                <CardHeader>
                  <Clock3 aria-hidden="true" />
                  <CardAction><ArrowRight aria-hidden="true" /></CardAction>
                </CardHeader>
                <CardContent>
                  <CardTitle>Vimshottari Dasha</CardTitle>
                  <CardDescription>Build full planetary timelines and inspect the period active at any date.</CardDescription>
                </CardContent>
              </Card>
            </Link>
            <Link to="/docs/$" params={{ _splat: 'yoga' }} className="asc-card-link">
              <Card className="asc-card">
                <CardHeader>
                  <List aria-hidden="true" />
                  <CardAction><ArrowRight aria-hidden="true" /></CardAction>
                </CardHeader>
                <CardContent>
                  <CardTitle>Classical yogas</CardTitle>
                  <CardDescription>Detect and describe meaningful planetary combinations with structured output.</CardDescription>
                </CardContent>
              </Card>
            </Link>
          </div>
        </section>
      </main>
    </HomeLayout>
  );
}
