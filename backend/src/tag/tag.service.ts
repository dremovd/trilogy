import { Injectable } from '@nestjs/common';
import { EntityRepository } from '@mikro-orm/core';
import { InjectRepository } from '@mikro-orm/nestjs';
import { Tag } from './tag.entity';
import { ITagsRO } from './tag.interface';

@Injectable()
export class TagService {
  constructor(
    @InjectRepository(Tag)
    private readonly tagRepository: EntityRepository<Tag>,
  ) {}

  async findAll(): Promise<ITagsRO> {
    const tags = await this.tagRepository.findAll();
    return { tags: tags.map((tag) => tag.tag) };
  }

  async handleTags(tagListStr: string): Promise<Tag[]> {
    const tags = tagListStr.split(',').map((tag) => tag.trim());
    const handledTags: Tag[] = [];
    for (const tagStr of tags) {
      let tagEntity = await this.tagRepository.findOne({ tag: tagStr });
      if (!tagEntity) {
        // Create a new Tag entity and save it
        tagEntity = new Tag();
        tagEntity.tag = tagStr;
        await this.tagRepository.persistAndFlush(tagEntity);
      }
      handledTags.push(tagEntity);
    }
    return handledTags;
  }
}
