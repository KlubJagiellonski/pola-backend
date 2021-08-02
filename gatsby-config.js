module.exports = {
  pathPrefix: (process.env.PUBLIC_URL && new URL(process.env.PUBLIC_URL).pathname) || null,
  siteMetadata: {
    title: `Pola Web`,
    description: `Strona aplikacji Pola`,
    author: `Klub Jagielloński`,
  },
  plugins: [
    'gatsby-plugin-use-query-params',
    `gatsby-plugin-styled-components`,
    `gatsby-plugin-react-helmet`,
    // generic images
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/assets/`,
      },
    },
    // images for articles
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/content/posts/`,
      },
    },
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `gatsby-starter-default`,
        short_name: `starter`,
        start_url: `/`,
        background_color: `#FFFFFF`,
        theme_color: `#D8152F`,
        display: `minimal-ui`,
        icon: `src/assets/logo/pola-color.svg`, // This path is relative to the root of the site.
      },
    },
    `gatsby-plugin-typescript`,
    {
      resolve: `gatsby-plugin-react-redux`,
      options: {
        pathToCreateStoreModule: './src/state/createStore',
        serialize: {
          space: 0,
          isJSON: true,
          unsafe: false,
        },
        cleanupOnClient: true,
        windowKey: '__PRELOADED_STATE__',
      },
    },
    // Markdown
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `posts`,
        path: `${__dirname}/content/posts`,
      },
    },
    {
      resolve: `gatsby-transformer-remark`,
      options: {
        // Footnotes mode (default: true)
        footnotes: true,
        // GitHub Flavored Markdown mode (default: true)
        gfm: true,
        // Plugins configs
        plugins: [
          `gatsby-plugin-sharp`,
          {
            resolve: `gatsby-remark-images`,
            options: {
              maxWidth: 800,
              backgroundColor: 'transparent',
            },
          },
          `gatsby-remark-copy-linked-files`,
          `gatsby-remark-smartypants`,
        ],
      },
    },
    // this (optional) plugin enables Progressive Web App + Offline functionality
    // To learn more, visit: https://gatsby.dev/offline
    // `gatsby-plugin-offline`,
  ],
};
