import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class EmailService {
  constructor(private readonly http: HttpClient) {}

  search(keyword: string) {
    return this.http.get('/api/email/search', { params: { q: keyword } });
  }
}
