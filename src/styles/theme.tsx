export const color = {
  primary: '#E5E5E5',
  dark: '#C4C4C4',
  border: '#A0A0A0',
  text: '#6C6C6C',
  black: '#000000',
  white: '#ffffff',
  red: '#D8152F',
  redLight: '#DF1F3F',
};

export const mobileHeaderHeight = '40px';
export const desktopHeaderHeight = '96px';

const width = 1272;
export const pageWidth = width + 'px';
export const padding = {
  tiny: '4px',
  small: '8px',
  normal: '20px',
  big: '40px',
};

export const Device: { [key: string]: string } = {
  mobile: `(max-width: ${width - 1}px)`,
  desktop: `(min-width: ${pageWidth})`,
};
