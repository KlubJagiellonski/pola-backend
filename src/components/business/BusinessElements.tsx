import React from 'react';
import styled from 'styled-components';
import SingleBusinessSlider from './SingleBusinessSlider';
import { SliderContainer } from '../SliderComponent';
import BusinessElement from './BusinessElement';
import { IBusinessTemplate } from '../../templates/BusinessTemplate';
import { useEffect } from 'react';
import { useQueryParams, StringParam } from 'use-query-params';

const H = styled.div`
  .slick-slider {
    .slick-list {
      .slick-track {
        display: flex;
        align-items: flex-end;
      }
    }
  }
`;

interface IBusinessElements {
  data: IBusinessTemplate;
}

const BusinessElements: React.FC<IBusinessElements> = ({ data }) => {
  const [query, setQuery] = useQueryParams<any>({
    value: StringParam,
  });

  useEffect(() => {
    if (!query.value && data.allMarkdownRemark.nodes.length > 0) {
      setQuery({ value: data.allMarkdownRemark.nodes[0].frontmatter.slug }, 'push');
    }
  }, [query, data]);

  return (
    <>
      <H>
        <SliderContainer rows={1}>
          {data.allMarkdownRemark.nodes?.map((el) => (
            <SingleBusinessSlider
              slug={el.frontmatter.slug}
              title={el.frontmatter.title}
              iconFluid={el.frontmatter.icon.childImageSharp.fluid}
            />
          ))}
        </SliderContainer>
      </H>
      {data.allMarkdownRemark.nodes
        ?.filter((el) => el.frontmatter.slug === query.value)
        .map((el) => (
          <BusinessElement html={el.html} imgFluid={el.frontmatter.cover?.childImageSharp?.fluid} />
        ))}
    </>
  );
};

export default BusinessElements;
