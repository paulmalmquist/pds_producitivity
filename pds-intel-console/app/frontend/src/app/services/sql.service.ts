import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SqlService {
  constructor(private readonly http: HttpClient) {}

  run(sql: string) {
    return this.http.post<{ columns: string[]; rows: unknown[][] }>('/api/sql/run', { sql });
  }
}
