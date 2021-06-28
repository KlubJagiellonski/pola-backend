import { graphql, useStaticQuery } from 'gatsby';

export interface IArticlesSuccess {
  results: IArticleData[];
}

export interface IArticlesError {
  error: unknown;
}

interface IArticleData {
  id: number;
  title: string;
  text: string;
  date: string;
  photo: string;
}

const articles: IArticleData[] = [
  {
    id: 1,
    title: 'ŚWIĄTECZNE ZAKUPY Z POLA APP DO 15% TANIEJ',
    text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
    date: '2020-12-12',
    photo: 'pexels-nadi-lindsay-3768323-1.png',
  },
  {
    id: 2,
    title: 'WIELKANOCNE ZAKUPY Z POLA APP DO 60% TANIEJ',
    text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
    date: '2021-03-17',
    photo: 'pexels-pixabay-33239-2.png',
  },
  {
    id: 3,
    title: 'MAJÓWKA Z POLA APP DO 45% TANIEJ',
    text: 'Sprawdź szczegóły promocji (wstęp artykułu) Lorem ipsum dolor sit amet enim. Etiam ullamcorper.',
    date: '2021-04-21',
    photo: 'pexels-polina-tankilevitch-3735657-1.png',
  },
];

export const ArticleService = {
  getArticles: async (): Promise<IArticlesSuccess> => {
    return {
      results: articles,
    };
  },
  getAll: () =>
    useStaticQuery(
      graphql`
        {
          allMarkdownRemark(filter: { fileAbsolutePath: { regex: "//posts//" } }, limit: 1000) {
            edges {
              node {
                id
                wordCount {
                  paragraphs
                  sentences
                  words
                }
                fields {
                  prefix
                  slug
                }
                frontmatter {
                  title
                  subTitle
                  category
                  cover {
                    extension
                    name
                    childImageSharp {
                      id
                      fixed {
                        src
                        originalName
                        width
                        height
                      }
                      fluid {
                        originalName
                        src
                        presentationWidth
                        presentationHeight
                        aspectRatio
                      }
                    }
                    relativePath
                  }
                }
              }
            }
          }
        }
      `
    ),
};

export interface IArticleEdge {
  node: IArticleNode;
}

export interface IArticleNode {
  id: string;
  wordCount: {
    paragraphs: number;
    sentences: number;
    words: number;
  };
  fields: {
    prefix: string;
    slug: string;
  };
  frontmatter: {
    title: string;
    subTitle: string;
    category: string;
    cover: {
      extension: string;
      name: string;
      childImageSharp: {
        id: string;
        fixed: {
          src: string;
          width: number;
          height: number;
        };
        fluid: {
          src: string;
          presentationWidth: number;
          presentationHeight: number;
          aspectRatio: number;
        };
      };
      relativePath: string;
    };
  };
}
