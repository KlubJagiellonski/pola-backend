import React from 'react';
import { PageSection } from '../../layout/PageSection';
import { EAN, IProductData } from '../../domain/products';
import { SearchResultsList } from '../../search/results-list/SearchResultsList';
import { PrimaryButton } from '../../components/buttons/PrimaryButton';
import { ButtonThemes, ButtonFlavor } from '../../components/buttons/Button';
import { SearchResultsHeader } from '../../search/results-list/SearchResultsHeader';
import { urls } from '../../domain/website';
import { SearchStateName } from '../../state/search/search-reducer';
import { MissingProductInfo } from '../../search/results-list/MissingProductInfo';
import { Spinner } from '../../components/Spinner';
import { InfoBox } from '../../components/InfoBox';

interface IFirstPageResults {
  state: SearchStateName;
  phrase: string;
  token: string;
  products: IProductData[];
  totalItems: number;

  onSelect: (code: EAN) => void;
  onClear: () => void;
}

export const FirstPageResults: React.FC<IFirstPageResults> = ({
  state,
  phrase,
  products,
  totalItems,
  onSelect,
  onClear,
}) => {
  const isLoaded = state === SearchStateName.LOADED || state === SearchStateName.SELECTED;
  const isLoading = state === SearchStateName.LOADING;
  const isError = state === SearchStateName.ERROR;

  return (
    <>
      {(isLoaded || isLoading) && (
        <SearchResultsHeader
          phrase={phrase}
          totalItems={totalItems}
          searchState={state}
          resultsUrl={totalItems > 0 ? urls.pola.products : undefined}
        />
      )}
      <PageSection>
        {isLoading && <Spinner text="Wyszukiwanie produktów..." />}
        {isLoaded && (
          <SearchResultsList
            results={products}
            totalItems={totalItems}
            actions={
              totalItems > 0 ? (
                <PrimaryButton styles={ButtonThemes[ButtonFlavor.GRAY]} onClick={onClear}>
                  <span>Anuluj</span>
                </PrimaryButton>
              ) : undefined
            }
            onSelect={onSelect}
          />
        )}
        {(isLoaded || isLoading) && <MissingProductInfo />}
        {isError && (
          <InfoBox>
            <h3>Błąd Wyszukiwania</h3>
            <p>Spróbuj wprowadzić inną frazę...</p>
          </InfoBox>
        )}
      </PageSection>
    </>
  );
};
