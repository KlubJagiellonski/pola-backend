import { navigate } from 'gatsby';

declare let window: any;

export const isBrowserEnv = () => typeof window !== 'undefined';

/**
 * Redirects to website page
 * @param url Object representing address of the page
 */
export const navigateTo = (url: string) => {
  if (isBrowserEnv()) {
    navigate(url);
  }
};

/**
 * Open external website in a new browser's tab
 * @param url Object representing address of the page
 */
export const openNewTab = (url: URL) => {
  if (isBrowserEnv()) {
    window.open(url.href, '_blank');
  }
};
