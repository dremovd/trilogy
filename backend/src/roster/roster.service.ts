import { Injectable } from '@nestjs/common';
import { UserRepository } from '../user/user.repository';
import { AuthorRoster } from './roster.types';

@Injectable()
export class RosterService {
  constructor(private readonly userRepository: UserRepository) {}

  async getAuthorsRoster(): Promise<AuthorRoster[]> {
    return this.userRepository.getAuthorsRoster();
  }
}
