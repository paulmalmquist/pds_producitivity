import {
  ChangeDetectionStrategy,
  Component,
  OnDestroy,
  effect,
  signal
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterService } from '../../services/router.service';
import { ChartInlineComponent } from '../chart-inline/chart-inline.component';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  source?: 'knowledge' | 'analytics' | 'tasks';
  chartConfig?: unknown;
}

@Component({
  selector: 'app-ai-chat-pane',
  standalone: true,
  imports: [CommonModule, FormsModule, ChartInlineComponent],
  templateUrl: './ai-chat-pane.component.html',
  styleUrls: ['./ai-chat-pane.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AiChatPaneComponent implements OnDestroy {
  readonly prompt = signal('');
  readonly messages = signal<ChatMessage[]>([]);
  readonly commandPaletteVisible = signal(false);
  readonly suggestions = signal<string[]>([]);

  private eventSource?: EventSource;

  constructor(
    private readonly http: HttpClient,
    private readonly routerService: RouterService
  ) {
    effect(() => {
      const promptValue = this.prompt();
      if (promptValue.startsWith('/')) {
        this.commandPaletteVisible.set(true);
        this.suggestions.set(this.buildSuggestions(promptValue));
      } else {
        this.commandPaletteVisible.set(false);
      }
    });
  }

  ngOnDestroy(): void {
    this.eventSource?.close();
  }

  sendPrompt(): void {
    const text = this.prompt().trim();
    if (!text) {
      return;
    }

    this.pushMessage({ role: 'user', content: text });
    this.prompt.set('');

    const intent = this.routerService.classifyIntent(text);
    const endpoint = this.routerService.endpointForIntent(intent);

    if (intent === 'mixed') {
      this.routerService.routeMixed(text).subscribe((payloads) => {
        payloads.forEach((entry) => {
          this.pushMessage({
            role: 'assistant',
            content: JSON.stringify(entry.payload, null, 2),
            source: entry.source
          });
        });
      });
      return;
    }

    if (!endpoint) {
      this.pushMessage({
        role: 'assistant',
        content: 'Unable to determine route. Please try refining your request.'
      });
      return;
    }

    if (intent === 'analytics') {
      this.fetchWithSse(endpoint, text, 'analytics');
    } else {
      this.http
        .post<{ answer?: string; narrative?: string }>(endpoint, { prompt: text })
        .subscribe((response) => {
          const content = response.answer ?? response.narrative ?? 'No response received.';
          this.pushMessage({ role: 'assistant', content, source: intent });
        });
    }
  }

  private fetchWithSse(endpoint: string, prompt: string, source: ChatMessage['source']): void {
    this.eventSource?.close();

    this.eventSource = new EventSource(`${endpoint}?prompt=${encodeURIComponent(prompt)}`);
    let aggregated = '';

    this.eventSource.onmessage = (event) => {
      aggregated += event.data;
      this.updateStreamingMessage(aggregated, source);
    };

    this.eventSource.onerror = () => {
      this.eventSource?.close();
    };
  }

  private updateStreamingMessage(content: string, source: ChatMessage['source']): void {
    const currentMessages = this.messages();
    const last = currentMessages[currentMessages.length - 1];
    if (last && last.role === 'assistant' && last.source === source) {
      this.messages.set([
        ...currentMessages.slice(0, -1),
        { ...last, content }
      ]);
    } else {
      this.pushMessage({ role: 'assistant', content, source });
    }
  }

  private pushMessage(message: ChatMessage): void {
    this.messages.set([...this.messages(), message]);
    this.routerService.notifySource(message.source);
  }

  private buildSuggestions(input: string): string[] {
    const [command, ...rest] = input.slice(1).split(' ');
    const value = rest.join(' ');
    const commands = [
      '/chart <query>',
      '/tableau <keyword>',
      '/project <code>',
      '/vendor <name>',
      '/person <name>',
      '/jira <jql>',
      '/playbook <name>'
    ];

    return commands.filter((item) => item.startsWith(`/${command}`) || !command).map((item) => {
      if (value) {
        return `${item.split(' ')[0]} ${value}`;
      }
      return item;
    });
  }
}
