import React from 'react';
import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';

const NotFoundPage = () => (
  <PageLayout>
    <SEOMetadata title="404: Not found" />
    <h1>NOT FOUND</h1>
    <p>You just hit a route that doesn&#39;t exist... the sadness.</p>
  </PageLayout>
);

export default NotFoundPage;
