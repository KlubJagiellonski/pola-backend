export const color = {
  background: {
    primary: '#C4C4C4',
    secondary: '#A0A0A0',
    dark: '#333333',
    black: '#000000',
    red: '#D8152F',
    white: '#ffffff',
  },
  text: {
    primary: '#333333',
    secondary: '#5B5B5B',
    light: '#ffffff',
    dark: '#000000',
    red: '#D8152F',
  },
  button: {
    white: '#ffffff',
    red: '#D8152F',
    redLight: '#DF1F3F',
    gray: '#C4C4C4',
    lightGray: '#C4C4C430',
    disabled: '#A0A0A0',
  },
  border: {
    grey: '#A0A0A0',
    white: '#ffffff',
  }
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
  veryBig: '80px',
  huge: '150px'
};
export const margin = {
  tiny: '4px',
  small: '8px',
  normal: '20px',
  big: '40px',
};

export const fontSize = {
  big: '24px',
  normal: '18px',
  small: '14px',
  tiny: '12px',
}

export const Device: { [key: string]: string } = {
  mobile: `(max-width: ${width - 1}px)`,
  desktop: `(min-width: ${pageWidth})`,
};
