import { createFileRoute } from "@tanstack/react-router";
import { HomeLayout } from "fumadocs-ui/layouts/home";
import { PlanetaryAtlasLanding } from "@/components/landing/planetary-atlas";
import {
  installCommand,
  planets,
  sdkCommand,
} from "@/components/landing/landing-data";
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
