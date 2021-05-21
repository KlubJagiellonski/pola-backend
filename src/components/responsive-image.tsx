import React from 'react';
import Img from 'gatsby-image';
import { StaticQuery, graphql } from 'gatsby';

function renderImage(file: any) {
  return <Img fluid={file.node.childImageSharp.fluid} />;
}

interface IResponsiveImage {
  imageSrc: string;
}

export const ResponsiveImage = function(props: IResponsiveImage) {
  return (
    <StaticQuery
      query={graphql`
        query {
          images: allFile(filter: { sourceInstanceName: { eq: "images" } }) {
            edges {
              node {
                extension
                relativePath
                childImageSharp {
                  fluid {
                    ...GatsbyImageSharpFluid
                  }
                }
              }
            }
          }
        }
      `}
      render={data => {
        const image = data.images.edges.find((image: any) => image.node.relativePath === props.imageSrc);
        return renderImage(image);
      }}
    />
  );
};
