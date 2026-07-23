import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import wordmark from '../../assets/ascendant-wordmark.svg';
import { gitConfig } from './shared';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: <img src={wordmark} alt="Ascendant" className="h-5 w-auto dark:brightness-0 dark:invert" />,
    },
    githubUrl: `https://github.com/${gitConfig.user}/${gitConfig.repo}`,
  };
}
