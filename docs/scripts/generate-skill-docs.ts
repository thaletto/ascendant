import { access, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const docsDirectory = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
);
const repositoryDirectory = path.resolve(docsDirectory, '..');
const skillsDirectory = path.join(
  repositoryDirectory,
  'plugins',
  'agent',
  'ascendant',
  'skills',
);
const outputDirectory = path.join(docsDirectory, 'content', 'skills');
const repositoryUrl = 'https://github.com/thaletto/ascendant';
const canonicalSkillsPath = 'plugins/agent/ascendant/skills';

type Skill = {
  description: string;
  markdown: string;
  name: string;
  title: string;
};

function parseSkill(source: string, directoryName: string): Skill {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(source);
  if (!match) {
    throw new Error(`${directoryName}/SKILL.md has no YAML frontmatter`);
  }

  const [, frontmatter, markdown] = match;
  const readField = (field: string): string => {
    const value = new RegExp(`^${field}:\\s*(.+)$`, 'm').exec(frontmatter)?.[1];
    if (!value) {
      throw new Error(`${directoryName}/SKILL.md has no ${field} field`);
    }
    return value.replace(/^(['"])(.*)\1$/, '$2');
  };

  const name = readField('name');
  if (name !== directoryName) {
    throw new Error(
      `${directoryName}/SKILL.md declares the unexpected name ${name}`,
    );
  }

  const heading = /^#\s+(.+)$/m.exec(markdown)?.[1];
  if (!heading) {
    throw new Error(`${directoryName}/SKILL.md has no level-one heading`);
  }

  return {
    description: readField('description'),
    markdown: markdown.replace(/^\s*#\s+.+\r?\n+/, ''),
    name,
    title: heading,
  };
}

function canonicalUrl(relativePath: string): string {
  return `${repositoryUrl}/blob/main/${relativePath}`;
}

function rewriteLinks(markdown: string, skillName: string): string {
  return markdown.replace(/\]\(([^)]+)\)/g, (fullMatch, target) => {
    if (
      target.startsWith('#') ||
      target.startsWith('/') ||
      /^[a-z]+:/i.test(target)
    ) {
      return fullMatch;
    }

    const repositoryPath = path.posix.normalize(
      path.posix.join(canonicalSkillsPath, skillName, target),
    );
    const otherSkill = new RegExp(
      `^${canonicalSkillsPath}/([^/]+)/SKILL\\.md$`,
    ).exec(repositoryPath)?.[1];

    if (otherSkill) {
      return `](/docs/skills/${otherSkill})`;
    }
    return `](${canonicalUrl(repositoryPath)})`;
  });
}

function pageFrontmatter(title: string, description: string): string {
  return [
    '---',
    `title: ${JSON.stringify(title)}`,
    `description: ${JSON.stringify(description)}`,
    '---',
  ].join('\n');
}

async function pathExists(filePath: string): Promise<boolean> {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function validateGeneratedSnapshot() {
  const metaPath = path.join(outputDirectory, 'meta.json');
  const meta: unknown = JSON.parse(await readFile(metaPath, 'utf8'));
  if (
    typeof meta !== 'object' ||
    meta === null ||
    !('pages' in meta) ||
    !Array.isArray(meta.pages)
  ) {
    throw new Error('The checked-in skill metadata has no pages array');
  }

  const skillPages = meta.pages.flatMap((page): string[] => {
    if (typeof page !== 'string') return [];
    const match = /^\[([^\]]+)]\(\/docs\/skills\/([^)]+)\)$/.exec(page);
    if (!match || match[1] !== match[2]) return [];
    return [match[1]];
  });

  if (skillPages.length === 0) {
    throw new Error('The checked-in skill documentation snapshot is empty');
  }

  await Promise.all(
    skillPages.map((skillName) =>
      access(path.join(outputDirectory, `${skillName}.md`)),
    ),
  );

  console.log(
    `Canonical skill sources are outside this deployment root; using ${skillPages.length} checked-in generated pages.`,
  );
}

if (!(await pathExists(skillsDirectory))) {
  await validateGeneratedSnapshot();
  process.exit(0);
}

await rm(outputDirectory, { recursive: true, force: true });
await mkdir(outputDirectory, { recursive: true });

const directoryEntries = await readdir(skillsDirectory, {
  withFileTypes: true,
});
const skills = [];

for (const entry of directoryEntries) {
  if (!entry.isDirectory()) continue;

  const skillPath = path.join(skillsDirectory, entry.name, 'SKILL.md');
  try {
    await access(skillPath);
  } catch {
    continue;
  }

  const source = await readFile(skillPath, 'utf8');
  const skill = parseSkill(source, entry.name);
  const sourceUrl = canonicalUrl(
    `${canonicalSkillsPath}/${skill.name}/SKILL.md`,
  );
  const output = [
    pageFrontmatter(skill.title, skill.description),
    '',
    `> Generated from the canonical [\`SKILL.md\`](${sourceUrl}). Edit the source specification, not this page.`,
    '',
    rewriteLinks(skill.markdown, skill.name).trim(),
    '',
  ].join('\n');

  await writeFile(
    path.join(outputDirectory, `${skill.name}.md`),
    output,
    'utf8',
  );
  skills.push(skill);
}

skills.sort((left, right) => left.name.localeCompare(right.name));

await writeFile(
  path.join(outputDirectory, 'meta.json'),
  `${JSON.stringify(
    {
      title: 'Skill specifications',
      description: 'Canonical Ascendant agent skill instructions.',
      pages: skills.map(
        (skill) => `[${skill.name}](/docs/skills/${skill.name})`,
      ),
    },
    null,
    2,
  )}\n`,
  'utf8',
);

console.log(`Generated ${skills.length} skill specification pages.`);
