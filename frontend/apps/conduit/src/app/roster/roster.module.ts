// roster.module.ts

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { RosterComponent } from './roster.component';
import { RosterService } from './roster.service';
  
@NgModule({
  declarations: [
    RosterComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild([
      {
        path: '',
        component: RosterComponent
      }
    ])
  ],
  providers: [
    RosterService
  ]
})
export class RosterModule { }