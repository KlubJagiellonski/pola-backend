from typing import Optional, TypedDict

import pola.logic_score
from pola.product.models import Product


class CompanyBasicInfo(TypedDict):
    name: str
    score: Optional[int]


class BrandBasicInfo(TypedDict):
    name: str


class SearchResult(TypedDict):
    name: str
    code: str
    company: Optional[CompanyBasicInfo]
    brand: Optional[BrandBasicInfo]

    @classmethod
    def create_from_product(cls, product: Product):
        return cls(
            name=str(product),
            code=product.code,
            company=(
                CompanyBasicInfo(
                    name=product.company.common_name or product.company.name,
                    score=pola.logic_score.get_pl_score(product.company),
                )
                if product.company and (product.company.common_name or product.company.name)
                else None
            ),
            brand=BrandBasicInfo(name=product.brand.name) if product.brand and product.brand.name else None,
        )


class SearchResultCollection(TypedDict):
    nextPageToken: Optional[str]
    products: list[SearchResult]
    totalItems: int
