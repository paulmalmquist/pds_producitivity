import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class JiraService {
  constructor(private readonly http: HttpClient) {}

  getStandupDigest() {
    return this.http.get('/api/jira/standup-digest');
  }

  createTask(payload: Record<string, unknown>) {
    return this.http.post('/api/jira/create', payload);
  }
}
