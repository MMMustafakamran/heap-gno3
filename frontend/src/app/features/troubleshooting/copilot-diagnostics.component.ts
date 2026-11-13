// https://docs.copilotkit.ai/angular/agno/guides/troubleshooting  (verbatim: src/app/copilot-diagnostics.component.ts)
import { Component, inject } from "@angular/core";
import { CopilotKit } from "@copilotkit/angular";

@Component({
  selector: "app-copilot-diagnostics",
  standalone: true,
  template: `
    <p>Runtime: {{ copilotKit.runtimeConnectionStatus() }}</p>
    <p>Agents: {{ agentIds().join(", ") || "none" }}</p>
  `,
})
export class CopilotDiagnosticsComponent {
  protected readonly copilotKit = inject(CopilotKit);
  protected readonly agentIds = () =>
    Object.keys(this.copilotKit.agents());
}
