import { navigate } from 'gatsby';

/**
 * Redirects to website page
 * @param url Object representing address of the page
 */
export const navigateTo = (url: string) => {
  if (window && typeof window !== 'undefined') {
    navigate(url);
  }
};

/**
 * Open external website in a new browser's tab
 * @param url Object representing address of the page
 */
export const openNewTab = (url: URL) => {
  if (window && typeof window !== 'undefined') {
    window.open(url.href, '_blank');
  }
};
