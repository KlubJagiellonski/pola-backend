import React from 'react';
import styled from 'styled-components';
import { margin } from '../../styles/theme';
import Tag from './Tag';

const Wrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: ${margin.small};
`;

const Title = styled.p`
  font-weight: bold;
`;

interface ITagsList {
  tag?: string[];
  activeTags?: string[];
}

const TagsList: React.FC<ITagsList> = ({ tag, activeTags }) => {
  return (
    <div>
      <Title>kategorie</Title>
      <Wrapper>
        {tag && tag.map((el, id) => <Tag key={`tag_${id}`} label={el} active={activeTags?.includes(el)} />)}
      </Wrapper>
    </div>
  );
};

export default TagsList;
