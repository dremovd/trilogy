import { EntityManager, FindOneOptions } from '@mikro-orm/core';
import { User } from './user.entity';
import { Injectable } from '@nestjs/common';
import { AuthorRoster } from '../roster/roster.types';

@Injectable()
export class UserRepository {
  constructor(private readonly em: EntityManager) {}

  async getAuthorsRoster(): Promise<AuthorRoster[]> {
    const authors = await this.em.find(User, {});
    await this.em.populate(authors, ['articles']);
    return authors.map((author) => {
      const totalLikes = author.articles.getItems().reduce((sum, article) => sum + article.favoritesCount, 0);
      return {
        username: author.username,
        profileLink: `/profile/${author.username}`,
        totalArticles: author.articles.length,
        totalLikes: totalLikes,
        firstArticleDate: author.articles[0]?.createdAt?.toISOString() || null,
      };
    }).sort((a, b) => b.totalLikes - a.totalLikes); // Sorting by likes
  }
  async findAll(): Promise<User[]> {
    return this.em.find(User, {});
  }

  async findOne(condition: any, options?: { populate: string[] }): Promise<User | null> {
    // Handle the populate option as needed
    // ...
  
    return this.em.findOne(User, condition, /* other options */);
  }
  

  getReference(id: number): User {
    return this.em.getReference(User, id);
  }

  async count(condition: any): Promise<number> {
    return this.em.count(User, condition);
  }

  async nativeDelete(condition: any): Promise<number> {
    return this.em.nativeDelete(User, condition);
  }

  async findOneOrFail(condition: any): Promise<User> {
    return this.em.findOneOrFail(User, condition);
  }
}
