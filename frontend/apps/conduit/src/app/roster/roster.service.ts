import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class RosterService {
  constructor(private readonly http: HttpClient) {}

  getAuthorsRoster() {
    return this.http.get('/api/roster');
  }
}
