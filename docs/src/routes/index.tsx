import { createFileRoute } from "@tanstack/react-router";
import { HomeLayout } from "fumadocs-ui/layouts/home";
import { PlanetaryAtlasLanding } from "@/components/landing-prototype/variant-b";
import {
  installCommand,
  planets,
  sdkCommand,
} from "@/components/landing-prototype/landing-data";
import { baseOptions } from "@/lib/layout.shared";

export const Route = createFileRoute("/")({
  component: Home,
});

const landingProps = {
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
