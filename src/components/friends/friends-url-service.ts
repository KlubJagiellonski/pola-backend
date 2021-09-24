import { encodeQueryParams, StringParam } from 'use-query-params';
import { urls } from '../../domain/website';
import { stringify } from 'query-string';

export function buildFriendUrl(slug: string, sectionId: string) {
  const encodedQuery = encodeQueryParams({ value: StringParam }, { value: slug });
  return `${urls.pola.friends}?${stringify(encodedQuery)}#${sectionId}`;
}
