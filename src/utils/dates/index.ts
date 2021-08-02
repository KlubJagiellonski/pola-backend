export function getDate(date: string) {
  const dateObj = new Date(date);
  const month = Object.values(Month);
  const dateToShow = `${dateObj.getDate()} ${month[dateObj.getMonth()]} ${dateObj.getFullYear()}`;

  return dateToShow;
}

enum Month {
  JANUARY = 'stycznia',
  FEBRUARY = 'lutego',
  MARCH = 'marca',
  APRIL = 'kwietnia',
  MAY = 'maja',
  JUNE = 'czerwca',
  JULY = 'lipca',
  AUGUST = 'sierpnia',
  SEPTEMBER = 'września',
  OCTOBER = 'października',
  NOVEMBER = 'listopada',
  DECEMBER = 'grudnia',
}
