import { Link } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { PageLinkData, PageType } from '../../domain/generic';
import { color } from '../../styles/theme';

const Item = styled.div<{ selected: boolean }>`
  font-weight: bolder;
  cursor: pointer;

  a {
    color: ${(props) => (props.selected ? color.text.red : color.text.primary)};
    text-decoration: none;
  }
`;

interface INavItem {
  data: PageLinkData;
  activePage: PageType;
  onClick: (type: PageType) => void;
}

export const NavItem: React.FC<INavItem> = ({ data, activePage, onClick }) => {
  const selected = data.type === activePage;
  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    onClick(data.type);
  };

  return (
    <Item className={data.type} selected={selected} onClick={handleClick}>
      <Link to={data.url}>{data.label}</Link>
    </Item>
  );
};
