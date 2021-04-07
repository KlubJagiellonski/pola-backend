export type ClassNameValue = string | boolean | undefined;
export type ClassNameType = ClassNameValue | ReadonlyArray<ClassNameValue>;

export const classNames = (...args: ClassNameType[]) => {
  const names: string[] = args.reduce((prev: string[], curr) => {
    if (typeof curr === 'string') {
      return [...prev, curr];
    }
    if (Array.isArray(curr) && curr.length === 2 && curr[1]) {
      return [...prev, curr[0]];
    }
    return prev;
  }, [] as string[]) as string[];
  return names.join(' ');
};
