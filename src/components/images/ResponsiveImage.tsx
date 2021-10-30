import React from 'react';
import Img from 'gatsby-image';
import { StaticQuery, graphql } from 'gatsby';

function renderImage(file: any) {
  return <Img fluid={file.node.childImageSharp.fluid} />;
}

interface IResponsiveImage {
  imageSrc: string;
}

export const ResponsiveImage: React.FC<IResponsiveImage> = function ({ imageSrc }) {
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
      render={(data) => {
        try {
          const image = data.images.edges.find((imageEdge: any) => imageEdge.node.relativePath === imageSrc);
          return renderImage(image);
        } catch {
          console.error(`Cannot load image "${imageSrc}"`);
          return;
        }
      }}
    />
  );
};
