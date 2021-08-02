import { color } from './theme';

interface IButtonColor {
  background: string;
  hover: string;
  text: string;
}

export const getButtonColor = (buttonColor?: ButtonColor): IButtonColor => {
  switch (buttonColor) {
    case ButtonColor.Red:
      return {
        background: color.button.red,
        hover: color.button.redLight,
        text: color.text.light,
      };
    case ButtonColor.White:
      return {
        background: color.button.white,
        hover: color.button.white,
        text: color.text.primary,
      };
    case ButtonColor.LightGray:
      return {
        background: color.button.lightGray,
        hover: color.background.gray,
        text: color.text.primary,
      };
    case ButtonColor.Gray:
    default:
      return {
        background: color.button.gray,
        hover: color.button.disabled,
        text: color.text.primary,
      };
  }
};

export enum ButtonColor {
  Gray,
  LightGray,
  Red,
  White,
}
