import { createRootRoute, HeadContent, Outlet, Scripts } from '@tanstack/react-router';
import * as React from 'react';
import appCss from '@/styles/app.css?url';
import { RootProvider } from 'fumadocs-ui/provider/tanstack';
import moonImage from '../../assets/moon.png';

export const Route = createRootRoute({
  head: () => ({
    meta: [
      {
        charSet: 'utf-8',
      },
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1',
      },
      {
        title: 'Ascendant — An astrology engine your agent can explain',
      },
      {
        name: 'description',
        content: 'Guided astrology workflows for AI agents, backed by local typed Python calculations and inspectable evidence.',
      },
      {
        property: 'og:title',
        content: 'Ascendant — An astrology engine your agent can explain',
      },
      {
        property: 'og:description',
        content: 'Guided astrology workflows for AI agents, backed by local typed Python calculations and inspectable evidence.',
      },
      {
        property: 'og:image',
        content: '/og.png',
      },
      {
        name: 'twitter:card',
        content: 'summary_large_image',
      },
      {
        name: 'twitter:image',
        content: '/og.png',
      },
    ],
    links: [
      { rel: 'stylesheet', href: appCss },
      { rel: 'icon', type: 'image/png', href: moonImage },
    ],
  }),
  component: RootComponent,
});

function RootComponent() {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <HeadContent />
      </head>
      <body className="flex flex-col min-h-screen">
        <RootProvider>
          <Outlet />
        </RootProvider>
        <Scripts />
      </body>
    </html>
  );
}
