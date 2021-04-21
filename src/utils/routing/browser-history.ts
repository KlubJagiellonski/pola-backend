import { BrowserHistory } from 'history';

export class BrowserHistoryInstance {
  public static history: BrowserHistory<object>;

  /**
   * Creates or returns existing object to manage browser history
   * @param history optional parameter, just to set once
   */
  public static setHistory(history: BrowserHistory<object>): void {
    BrowserHistoryInstance.history = history;
  }
}

export const redirectTo = (url: string) => {
  if (BrowserHistoryInstance.history) {
    BrowserHistoryInstance.history.push(url);
  }
};
