import { DynamicCodeBlock } from "fumadocs-ui/components/dynamic-codeblock";
import { Tab, Tabs } from "fumadocs-ui/components/tabs";

interface InstallCommandProps {
  agentCommand: string;
  sdkCommand: string;
  className?: string;
}

export function InstallCommand({
  agentCommand,
  sdkCommand,
  className,
}: InstallCommandProps) {
  return (
    <Tabs items={["Agent", "Python"]} defaultIndex={0}>
      <Tab value="Agent">
        <DynamicCodeBlock code={agentCommand} lang="bash" />
      </Tab>
      <Tab value="Python">
        <DynamicCodeBlock code={sdkCommand} lang="bash" />
      </Tab>
    </Tabs>
  );
}
