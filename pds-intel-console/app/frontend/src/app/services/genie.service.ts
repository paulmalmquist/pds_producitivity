import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

export interface GenieResponse {
  narrative: string;
  sql: string;
  columns: string[];
  rows: unknown[][];
  viz_hints?: {
    chartType?: string;
    x?: string;
    y?: string;
    series?: string;
    isTimeSeries?: boolean;
    percentLike?: boolean;
  };
}

@Injectable({ providedIn: 'root' })
export class GenieService {
  constructor(private readonly http: HttpClient) {}

  ask(prompt: string, context?: Record<string, unknown>) {
    return this.http.post<GenieResponse>('/api/genie/ask', { prompt, context });
  }
}
