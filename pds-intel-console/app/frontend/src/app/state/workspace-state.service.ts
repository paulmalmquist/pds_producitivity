import { Injectable } from '@angular/core';

type WorkspaceType = 'project' | 'vendor' | 'person';

interface WorkspaceState {
  type: WorkspaceType;
  key: string;
  chats: { role: string; content: string }[];
  pinnedCards: unknown[];
  chartConfigs: Record<string, unknown>;
}

interface SettingsState {
  jllGptEndpoint?: string;
  jllGptApiKey?: string;
  genieEndpoint?: string;
  jiraUrl?: string;
}

const STORAGE_KEY = 'pds-intel-console-state';

@Injectable({ providedIn: 'root' })
export class WorkspaceStateService {
  private state: WorkspaceState[] = [];
  private settingsState: SettingsState = {};

  constructor() {
    const persisted = typeof localStorage !== 'undefined' ? localStorage.getItem(STORAGE_KEY) : null;
    if (persisted) {
      const parsed = JSON.parse(persisted);
      this.state = parsed.workspaces ?? [];
      this.settingsState = parsed.settings ?? {};
    } else {
      this.state = [
        {
          type: 'project',
          key: 'Northwind',
          chats: [
            { role: 'user', content: 'Show me cost trends for Northwind.' },
            { role: 'assistant', content: 'Capital spend increased 10% MoM.' }
          ],
          pinnedCards: [
            {
              type: 'chart',
              title: 'Northwind Spend Trend',
              description: 'Auto-pinned insight from Genie',
              chartConfig: null
            }
          ],
          chartConfigs: {}
        }
      ];
    }
  }

  lastChats() {
    return this.state.flatMap((workspace) => workspace.chats).slice(-10);
  }

  pinnedCards() {
    return this.state.flatMap((workspace) => workspace.pinnedCards);
  }

  updateWorkspace(workspace: WorkspaceState) {
    const existingIndex = this.state.findIndex(
      (item) => item.type === workspace.type && item.key === workspace.key
    );

    if (existingIndex >= 0) {
      this.state[existingIndex] = workspace;
    } else {
      this.state.push(workspace);
    }

    this.persist();
  }

  settings(): SettingsState {
    return { ...this.settingsState };
  }

  updateSettings(settings: SettingsState): void {
    this.settingsState = { ...settings };
    this.persist();
  }

  private persist(): void {
    if (typeof localStorage === 'undefined') {
      return;
    }
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        workspaces: this.state.slice(-3),
        settings: this.settingsState
      })
    );
  }
}
