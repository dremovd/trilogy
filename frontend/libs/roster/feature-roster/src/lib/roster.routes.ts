import { RosterComponent } from './roster.component';
import { RosterResolver } from './roster-resolver.service';

export const ROSTER_ROUTES = [
  { path: '', component: RosterComponent, resolve: { authors: RosterResolver } }
];
