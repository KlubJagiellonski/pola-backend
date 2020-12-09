import { createBrowserHistory, createMemoryHistory } from "history";

const isTest = process.env.NODE_ENV === "test";

export const history = isTest
  ? createMemoryHistory({ initialEntries: ['/'] })
  : createBrowserHistory();