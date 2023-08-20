import { Controller, Get } from '@nestjs/common';
import { RosterService } from './roster.service';
import { AuthorRoster } from './roster.types';

@Controller('roster')
export class RosterController {
  constructor(private readonly rosterService: RosterService) {}

  @Get()
  async getAuthorsRoster(): Promise<AuthorRoster[]> {
    return this.rosterService.getAuthorsRoster();
  }
}
