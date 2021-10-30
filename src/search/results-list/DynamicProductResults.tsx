import React from 'react';
import { PageSection } from '../../layout/PageSection';
import { color } from '../../styles/theme';
import { EAN, IProductData } from '../../domain/products';
import { SearchResultsList } from '../../search/results-list/SearchResultsList';
import { PrimaryButton } from '../../components/buttons/PrimaryButton';
import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';
import { Spinner } from '../../components/Spinner';
import { SearchStateName } from '../../state/search/search-reducer';
import { SearchResultsHeader } from '../../search/results-list/SearchResultsHeader';
import { MissingProductInfo } from '../../search/results-list/MissingProductInfo';

interface IDynamicProductResults {
  state: SearchStateName;
  phrase: string;
  token: string;
  pages: IProductData[];
  totalItems: number;

  onSelect: (code: EAN) => void;
  onLoadMore: () => void;
}

export const DynamicProductResults: React.FC<IDynamicProductResults> = ({
  state,
  phrase,
  pages,
  totalItems,
  onSelect,
  onLoadMore,
}) => {
  const loadButton =
    state === SearchStateName.LOADING ? (
      <PrimaryButton
        disabled={true}
        icon={<Spinner styles={{ size: 20, color: color.button.white }} />}
        styles={ButtonThemes[ButtonFlavor.RED]}
      />
    ) : (
      <PrimaryButton label="Wczytaj więcej" styles={ButtonThemes[ButtonFlavor.RED]} onClick={onLoadMore} />
    );

  return (
    <>
      <SearchResultsHeader phrase={phrase} totalItems={totalItems} searchState={state} />
      <PageSection>
        <SearchResultsList results={pages} totalItems={totalItems} onSelect={onSelect} actions={loadButton} />
        <MissingProductInfo />
      </PageSection>
    </>
  );
};
