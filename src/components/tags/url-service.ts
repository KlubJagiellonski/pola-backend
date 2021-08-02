import { withDefault, encodeQueryParams, ArrayParam } from 'use-query-params';
import { urls } from '../../domain/website';
import { stringify } from 'query-string';

export function tagUrl(label: string, query: any) {
  let tags = query.tags.slice();
  const isTag = tags.find((tag: string) => tag === label);
  if (!isTag) {
    tags.push(label);
  } else {
    tags = tags.filter((tag: string) => tag !== label);
  }
  const encodedQuery = encodeQueryParams({ tags: withDefault(ArrayParam, []) }, { tags });
  return `${urls.pola.news}?${stringify(encodedQuery)}`;
}
