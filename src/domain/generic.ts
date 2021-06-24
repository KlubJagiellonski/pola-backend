/**
 * Represents period in seconds
 */
export type seconds = number;

/**
 * Represents period in miliseconds
 */
export type miliseconds = number;

export enum PageType {
  HOME = 'home',
  NEWS = 'news',
  ABOUT = 'about',
  SUPPORT = 'support',
  FRIENDS = 'friends',
  TEAM = 'team',
  FAQ = 'faq',
  CONTACT = 'contact',
  PRODUCTS = 'products',
  ERROR_404 = '404',
}

export interface PageLinkData {
  type: PageType;
  label: string;
  url: string;
}
