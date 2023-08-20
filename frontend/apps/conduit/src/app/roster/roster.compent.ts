import { Component, OnInit } from '@angular/core';
import { RosterService } from './roster.service';

interface AuthorRoster {
  username: string;           // The user name
  profileLink: string;        // The profile link
  totalArticles: number;      // The total number of articles authored
  totalLikes: number;         // The total number of likes received on their articles
  firstArticleDate: string | null; // The date of their first articles, or null if no post was made yet
}
    
@Component({
  selector: 'app-roster',
  templateUrl: './roster.component.html',
})
export class RosterComponent implements OnInit {
  authorsRoster: AuthorRoster[] = [];

  constructor(private readonly rosterService: RosterService) {}

  ngOnInit() {
    this.rosterService.getAuthorsRoster().subscribe((data: any) => { // Use 'any' type or specific type
      this.authorsRoster = data;
    });
  }
}