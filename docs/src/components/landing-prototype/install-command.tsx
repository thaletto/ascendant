import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface InstallCommandProps {
  agentCommand: string;
  sdkCommand: string;
  className?: string;
  inverse?: boolean;
}
export function InstallCommand({
  agentCommand,
  sdkCommand,
  className,
  inverse = false,
}: InstallCommandProps) {
  const [active, setActive] = useState<"agent" | "python">("agent");
  const [copied, setCopied] = useState(false);
  const command = active === "agent" ? agentCommand : sdkCommand;

  async function copyCommand() {
    await navigator.clipboard.writeText(command);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  return (
    <Card
      className={cn(
        "gap-0 rounded-2xl py-0 shadow-[0_1rem_3rem_color-mix(in_oklch,var(--foreground)_10%,transparent)]",
        inverse && "bg-cosmos text-cosmos-foreground ring-white/12",
        className,
      )}
    >
      <div className="flex items-center gap-1 border-b border-border/70 p-2" role="tablist" aria-label="Installation method">
        <Button
          type="button"
          role="tab"
          aria-selected={active === "agent"}
          variant={active === "agent" ? "secondary" : "ghost"}
          className="h-9 min-w-20 rounded-xl px-3 text-sm active:scale-[0.96]"
          onClick={() => setActive("agent")}
        >
          Agent
        </Button>
        <Button
          type="button"
          role="tab"
          aria-selected={active === "python"}
          variant={active === "python" ? "secondary" : "ghost"}
          className="h-9 min-w-20 rounded-xl px-3 text-sm active:scale-[0.96]"
          onClick={() => setActive("python")}
        >
          Python
        </Button>
      </div>
      <CardContent className="flex min-h-16 items-center gap-3 px-4 py-3">
        <span className="select-none font-mono text-muted-foreground" aria-hidden="true">$</span>
        <code className="min-w-0 flex-1 overflow-x-auto whitespace-nowrap font-mono text-[0.8125rem] text-foreground sm:text-sm">
          {command}
        </code>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="size-11 shrink-0 rounded-xl active:scale-[0.96]"
          onClick={copyCommand}
          aria-label={copied ? "Command copied" : "Copy command"}
        >
          {copied ? <Check aria-hidden="true" /> : <Copy aria-hidden="true" />}
        </Button>
      </CardContent>
    </Card>
  );
}
