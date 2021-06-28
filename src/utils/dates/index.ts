export function getDate(date: string) {
  const dateObj = new Date(date).toUTCString();
  const dateToShow = dateObj.split(' ').slice(0, 4).join(' ');

  return dateToShow;
}
