// roster.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthorRoster } from './roster.types';

@Component({
  selector: 'app-roster',
  templateUrl: './roster.component.html',
  styleUrls: ['./roster.component.css'],
})
export class RosterComponent implements OnInit {
  authorsRoster: AuthorRoster[] = [];

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.authorsRoster = this.route.snapshot.data['authors'];
  }
}
