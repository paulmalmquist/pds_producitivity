import { EventEmitter, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable, forkJoin } from 'rxjs';

export type Intent = 'knowledge' | 'analytics' | 'tasks' | 'mixed';
export type Source = 'knowledge' | 'analytics' | 'tasks';

@Injectable({ providedIn: 'root' })
export class RouterService {
  private readonly baseUrl = '/api';
  private readonly activeSources = new Set<Source>();
  readonly activeSourcesChanged = new EventEmitter<Source[]>();

  constructor(private readonly http: HttpClient) {}

  classifyIntent(prompt: string): Intent {
    const lowered = prompt.toLowerCase();
    const matches = new Set<Source>();

    if (/chart|sql|trend|genie|visual/i.test(prompt)) {
      matches.add('analytics');
    }
    if (/jira|task|standup|ticket|email/i.test(lowered)) {
      matches.add('tasks');
    }
    if (/explain|what|who|rag|knowledge|policy/i.test(lowered)) {
      matches.add('knowledge');
    }

    if (matches.size === 0) {
      return 'knowledge';
    }

    if (matches.size > 1) {
      return 'mixed';
    }

    return Array.from(matches)[0];
  }

  endpointForIntent(intent: Intent): string | null {
    switch (intent) {
      case 'knowledge':
        return `${this.baseUrl}/rag/ask`;
      case 'analytics':
        return `${this.baseUrl}/stream/chat`;
      case 'tasks':
        return `${this.baseUrl}/jira/standup-digest`;
      default:
        return null;
    }
  }

  routeMixed(prompt: string): Observable<{ source: Source; payload: unknown }[]> {
    const knowledge$ = this.http
      .post(`${this.baseUrl}/rag/ask`, { prompt })
      .pipe(map((payload) => ({ source: 'knowledge' as const, payload })));
    const analytics$ = this.http
      .post(`${this.baseUrl}/genie/ask`, { prompt })
      .pipe(map((payload) => ({ source: 'analytics' as const, payload })));
    const tasks$ = this.http
      .get(`${this.baseUrl}/jira/standup-digest`)
      .pipe(map((payload) => ({ source: 'tasks' as const, payload })));

    return forkJoin([knowledge$, analytics$, tasks$]);
  }

  notifySource(source?: Source): void {
    if (!source) {
      return;
    }
    this.activeSources.add(source);
    this.activeSourcesChanged.emit(Array.from(this.activeSources));
  }

  activeSourcesSignal(): Source[] {
    return Array.from(this.activeSources);
  }
}
