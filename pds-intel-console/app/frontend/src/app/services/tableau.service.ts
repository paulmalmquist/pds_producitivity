import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class TableauService {
  constructor(private readonly http: HttpClient) {}

  listViews() {
    return this.http.get('/api/tableau/views');
  }

  snapshot(viewId: string) {
    return this.http.post('/api/tableau/snapshot', { viewId });
  }
}
