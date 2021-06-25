import React from 'react';
import { useDispatch } from 'react-redux';
import { PageType } from '../domain/website';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';
import { PageLayout } from '../layout/PageLayout';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import SEOMetadata from '../utils/browser/SEOMetadata';

interface INotFoundPage {
  location?: Location;
}

const NotFoundPage = (props: INotFoundPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.ERROR_404));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata title="404: Not found" />
      <DevelopmentPlaceholder text="Strona nie istnieje" />
    </PageLayout>
  );
};

export default NotFoundPage;
