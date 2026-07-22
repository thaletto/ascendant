import { createFileRoute } from "@tanstack/react-router";
import { HomeLayout } from "fumadocs-ui/layouts/home";
import { PlanetaryAtlasLanding } from "@/components/landing-prototype/variant-b";
import {
  installCommand,
  planets,
  sdkCommand,
} from "@/components/landing-prototype/landing-data";
import { baseOptions } from "@/lib/layout.shared";
import { ASCENDANT_VERSION } from "@/lib/shared";

export const Route = createFileRoute("/")({
  component: Home,
});

const landingProps = {
  version: ASCENDANT_VERSION,
  installCommand,
  sdkCommand,
  planets,
};

function Home() {
  return (
    <HomeLayout {...baseOptions()}>
      <PlanetaryAtlasLanding {...landingProps} />
    </HomeLayout>
  );
}
