import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

export interface KnowledgeResponse {
  answer: string;
  sources: { title: string; url: string }[];
  entities: string[];
}

@Injectable({ providedIn: 'root' })
export class KnowledgeService {
  constructor(private readonly http: HttpClient) {}

  ask(prompt: string) {
    return this.http.post<KnowledgeResponse>('/api/rag/ask', { prompt });
  }
}
