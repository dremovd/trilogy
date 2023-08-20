import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ROSTER_ROUTES } from './roster.routes';
import { RosterComponent } from './roster.component';
import { RosterService } from './roster.service';

@NgModule({
  imports: [
    RouterModule.forChild(ROSTER_ROUTES),
    CommonModule,
  ],
  declarations: [RosterComponent],
  providers: [
    RosterService, 
  ],
})
export class RosterFeatureRosterModule {}
