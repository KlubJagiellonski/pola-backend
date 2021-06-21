module.exports = {
  pathPrefix: (process.env.PUBLIC_URL && new URL(process.env.PUBLIC_URL).pathname) || null,
  siteMetadata: {
    title: `Pola Web`,
    description: `Strona aplikacji Pola`,
    author: `Klub Jagielloński`,
  },
  plugins: [
    `gatsby-plugin-react-helmet`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: `${__dirname}/src/assets`,
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
    // this (optional) plugin enables Progressive Web App + Offline functionality
    // To learn more, visit: https://gatsby.dev/offline
    // `gatsby-plugin-offline`,
  ],
};
