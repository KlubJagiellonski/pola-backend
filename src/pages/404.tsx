import React from 'react';
import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';

const NotFoundPage = () => (
  <PageLayout>
    <SEO title="404: Not found" />
    <h1>NOT FOUND</h1>
    <p>You just hit a route that doesn&#39;t exist... the sadness.</p>
  </PageLayout>
);

export default NotFoundPage;
