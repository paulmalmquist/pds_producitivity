import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PlaybookService {
  constructor(private readonly http: HttpClient) {}

  getPlaybooks() {
    return this.http.get<{ name: string; steps: string[] }[]>('/api/playbooks');
  }
}
