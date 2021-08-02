import React, { useState, useEffect } from 'react'

import { ButtonColor } from '../../styles/button-theme'
import { fontSize } from '../../styles/theme'
import { TagButton } from '../buttons/TagButton'
import { ArrayParam, useQueryParams, withDefault } from 'use-query-params';
import { tagUrl } from './url-service';
import { Link } from 'gatsby';

interface ITag {
  label?: string;
  active?: boolean
}

interface IQuery {
  tags: string[],
}

const Tag: React.FC<ITag> = ({ label, active }) => {
  const [query] = useQueryParams<IQuery>({ tags: withDefault(ArrayParam, []) });
  const [url, setUrl] = useState("");

  useEffect(() => {
    if (label) {
      setUrl(tagUrl(label, query))
    }
  }, [label]);

  return (
    <Link to={url}>
      <TagButton
        label={label}
        color={active ? ButtonColor.Gray : ButtonColor.LightGray}
        fontSize={fontSize.small}
      />
    </Link>
  )
}

export default Tag;