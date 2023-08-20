import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { RosterService } from './roster.service';
import { AuthorRoster } from './roster.types';

@Injectable({
  providedIn: 'root',
})
export class RosterResolver implements Resolve<AuthorRoster[]> {
  constructor(private rosterService: RosterService) {}

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<AuthorRoster[]> {
    return this.rosterService.getAuthorsRoster();
  }
}
