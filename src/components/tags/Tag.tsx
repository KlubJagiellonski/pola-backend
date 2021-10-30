import React, { useState, useEffect } from 'react';

import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';
import { fontSize } from '../../styles/theme';
import { TagButton } from '../buttons/TagButton';
import { ArrayParam, useQueryParams, withDefault } from 'use-query-params';
import { tagUrl } from './url-service';
import { Link } from 'gatsby';

interface ITag {
  label?: string;
  active?: boolean;
}

interface IQuery {
  tags: string[];
}

const Tag: React.FC<ITag> = ({ label, active }) => {
  const [query] = useQueryParams<IQuery>({ tags: withDefault(ArrayParam, []) });
  const [url, setUrl] = useState('');

  useEffect(() => {
    if (label) {
      setUrl(tagUrl(label, query));
    }
  }, [label]);

  const flavor = active ? ButtonFlavor.GRAY : ButtonFlavor.LIGHT_GRAY;
  const styles = ButtonThemes[flavor];

  return (
    <Link to={url}>
      <TagButton label={label} styles={styles} />
    </Link>
  );
};

export default Tag;
