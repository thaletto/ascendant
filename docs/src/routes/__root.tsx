import { createRootRoute, HeadContent, Outlet, Scripts } from '@tanstack/react-router';
import appCss from '@/styles/app.css?url';
import { RootProvider } from 'fumadocs-ui/provider/tanstack';
import moonImage from '../../assets/planets/moon.png';

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
        title: 'Ascendant',
      },
      {
        name: 'description',
        content: 'Guided astrology workflows for AI agents, backed by local typed Python calculations and inspectable evidence.',
      },
      {
        property: 'og:title',
        content: 'Ascendant - AI Skills and SDK for Astrology',
      },
      {
        property: 'og:description',
        content: 'Guided astrology workflows for AI agents, backed by local typed Python calculations and inspectable evidence.',
      },
      {
        name: 'twitter:card',
        content: 'summary_large_image',
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
