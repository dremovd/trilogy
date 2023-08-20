import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthorRoster } from './roster.types';

@Injectable()
export class RosterService {
  constructor(private readonly httpClient: HttpClient) {}

  getRoster(): Observable<AuthorRoster[]> {
    return this.httpClient.get<AuthorRoster[]>('/api/roster');
  }
}
