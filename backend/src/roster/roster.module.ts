import { Module } from '@nestjs/common';
import { RosterController } from './roster.controller';
import { RosterService } from './roster.service';
import { UserModule } from '../user/user.module'; // Import the module containing UserRepository

@Module({
  imports: [
    UserModule, // Include the UserModule (or the module containing UserRepository) in the imports array
  ],
  controllers: [RosterController],
  providers: [RosterService],
})
export class RosterModule {}
