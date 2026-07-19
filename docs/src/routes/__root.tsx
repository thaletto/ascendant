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
        title: 'Ascendant — Vedic astrology, expressed as code',
      },
      {
        name: 'description',
        content: 'Typed Vedic astrology calculations for Python and installable workflows for AI coding agents.',
      },
      {
        property: 'og:title',
        content: 'Ascendant — Vedic astrology, expressed as code',
      },
      {
        property: 'og:description',
        content: 'Typed Vedic astrology calculations for Python and installable workflows for AI coding agents.',
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
