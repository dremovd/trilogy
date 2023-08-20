import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ROSTER_ROUTES } from './roster.routes';
import { RosterComponent } from './roster.component';

@NgModule({
  imports: [RouterModule.forChild(ROSTER_ROUTES)],
  declarations: [RosterComponent],
})
export class RosterFeatureRosterModule {}
