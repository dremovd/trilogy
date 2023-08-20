import { AuthorRoster } from './roster.types';
import { ApiService } from '@realworld/core/http-client';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RosterService {
  constructor(private readonly apiService: ApiService) {} // Use ApiService

  getRoster(): Observable<AuthorRoster[]> {
    return this.apiService.get<AuthorRoster[]>('/roster'); // Use the apiService to make the GET request
  }
}
