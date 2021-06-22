import { Link } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { PageType } from '../../domain/generic';
import { color } from '../../styles/theme';

interface INavItem {
  label: string;
  to: string;
  type: PageType;
  activePage: PageType;
}

const Item = styled.div<{ selected: boolean }>`
  font-weight: bolder;
  cursor: pointer;

  &.selected {
    color: ${color.text.red};
  }

  a {
    color: black;
    text-decoration: none;
  }
`;

export const NavItem: React.FC<INavItem> = ({ label, to, type, activePage }) => {
  const selected = type === activePage;
  return (
    <Item className={type} selected={selected}>
      <Link to={to}>{label}</Link>
    </Item>
  );
};
