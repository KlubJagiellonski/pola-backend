import React, { Component, FormEvent } from 'react';
import onClickOutside from 'react-onclickoutside';

export interface IClickOutsideComponentProps {
  clickOutsideHandler?: () => void;
}

class ClickOutsideComponent extends Component<IClickOutsideComponentProps> {
  handleClickOutside = (evt: FormEvent) => {
    this.props.clickOutsideHandler && this.props.clickOutsideHandler();
  };

  public render() {
    return <div className="click-outside">{this.props.children}</div>;
  }
}

export const ClickOutside = onClickOutside(ClickOutsideComponent);
