import { Link } from 'gatsby';
import { AnchorLink } from 'gatsby-plugin-anchor-links';
import React from 'react';
import styled from 'styled-components';
import { classNames } from '../class-names';

const Anchor = styled.a`
  text-decoration: none;
`;

interface IExternalLink {
  url: URL;
  newTab?: boolean;
  children: React.ReactNode | React.ReactNode[];
}

export const ExternalLink: React.FC<IExternalLink> = ({ url, newTab = true, children }) => (
  <Anchor href={url.href} target={newTab ? '__blank' : undefined}>
    {children}
  </Anchor>
);

interface ITextLink {
  label: string;
  href: string;
  anchor?: boolean;
  hideMobile?: boolean;
}

export const TextLink: React.FC<ITextLink> = ({ label, href, anchor = false, hideMobile = false }) =>
  anchor ? (
    <AnchorLink className="link" to={href}>
      <p className={classNames('text', ['hide-mobile', hideMobile])}>{label}</p>
    </AnchorLink>
  ) : (
    <Link className="link" to={href}>
      <p className={classNames('text', ['hide-mobile', hideMobile])}>{label}</p>
    </Link>
  );

interface ITextExternalLink {
  label: string;
  url: URL;
  hideMobile?: boolean;
}

export const TextExternalLink: React.FC<ITextExternalLink> = ({ label, url, hideMobile = false }) => (
  <ExternalLink url={url}>
    <p className={classNames('text', ['hide-mobile', hideMobile])}>{label}</p>
  </ExternalLink>
);
