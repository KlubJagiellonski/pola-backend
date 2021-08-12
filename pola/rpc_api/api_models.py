from typing import List, Optional, TypedDict

from product.models import Product


class CompanyBasicInfo(TypedDict):
    name: str


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
            company=CompanyBasicInfo(name=product.company.name) if product.company else None,
            brand=BrandBasicInfo(name=product.brand.name) if product.brand else None,
        )


class SearchResultCollection(TypedDict):
    nextPageToken: Optional[str]
    products: List[SearchResult]
    totalItems: int
