import { Component, OnInit } from '@angular/core';
import { RosterService } from './roster.service';
import { AuthorRoster } from './roster.types';
    
@Component({
  selector: 'app-roster',
  templateUrl: './roster.component.html',
})
export class RosterComponent implements OnInit {
  authorsRoster: AuthorRoster[] = [];

  constructor(private readonly rosterService: RosterService) {}

  ngOnInit(): void {
    this.rosterService.getRoster().subscribe((data: AuthorRoster[]) => {
      this.authorsRoster = data;
    });
  }
}