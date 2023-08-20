import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthorRoster } from './roster.types';

@Injectable()
export class RosterService {
  private readonly apiUrl = '/api/roster';

  constructor(private readonly httpClient: HttpClient) {}

  getRoster(): Observable<AuthorRoster[]> { // Use AuthorRoster type here
    return this.httpClient.get<AuthorRoster[]>(this.apiUrl);
  }
}
