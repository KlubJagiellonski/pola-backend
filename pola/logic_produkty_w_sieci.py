import logging
from typing import Optional

from pola.company.models import Brand, Company
from pola.gpc.models import GPCBrick
from pola.integrations.produkty_w_sieci import ProductBase
from pola.logic_bot_report import create_bot_report
from pola.product.models import Product
from pola.text_utils import strip_dbl_spaces

LOGGER = logging.getLogger(__file__)


def is_code_supported(code: str):
    # Check if 590 only is supported by GS1
    return code[0:3] == '590' and len(code) == 13


def create_from_api(
    code: str, get_products_response: Optional[ProductBase], product: Optional[Product] = None
) -> Product | None:
    if not is_code_supported(code):
        raise Exception(f"Unsupported code: {code}")
    result_product = get_products_response
    result_company = result_product.company if result_product else None

    company_created, expected_company = ensure_company_exists(result_company)
    brand_created, expected_brand = ensure_brand_exists(expected_company, result_product)

    if not result_product:
        LOGGER.info(f"Did not get a response for product {code}")

    if not product and result_product:
        LOGGER.info("Product missing. Creating a new product.")
        product = Product.objects.create(
            name=result_product.name,
            code=code,
            company=expected_company,
            brand=expected_brand,
            # TODO: co jesli jest wiecej niz jeden GPC?
            gpc_brick=(
                GPCBrick.objects.filter(code=result_product.gpc[0].code).first()
                if len(result_product.gpc) > 0
                else None
            ),
            commit_desc="Produkt utworzony automatycznie na podstawie skanu użytkownika",
        )
        return product

    LOGGER.info("Product exists. Updating a product.")
    product_commit_desc = ""
    if product.name:
        if result_product and result_product.name and product.name != result_product.name:
            LOGGER.info(
                "Product name mismatch. Old name: %s, new name: %s, Creating a report.",
                product.name,
                result_product.name,
            )
            create_bot_report(
                product,
                f"Wg. najnowszego odpytania w bazie ILiM nazwa tego produktu to: {result_product.name}",
                check_if_already_exists=not company_created,
            )
    else:
        if result_product and result_product.name != code and result_product.name:
            LOGGER.info("A previously unknown product name was found. Updating the product.")
            product_commit_desc += 'Nazwa produktu zmieniona na podstawie bazy GS1. '
            product.name = result_product.name

    if expected_company:
        if product.company and product.company.name and not ilim_compare_str(product.company.name, result_company.name):
            LOGGER.info(
                "Company name mismatch. Old name: %s, new name: %s, Creating a report.",
                product.company.name,
                result_company.name,
            )
            create_bot_report(
                product,
                f"Wg. najnowszego odpytania w bazie ILiM producent tego produktu to: {result_company.name!r}",
                check_if_already_exists=not company_created,
            )
        else:
            LOGGER.info("A previously unknown company was found. Updating the product.")
            product_commit_desc += 'Producent produktu zmieniony na podstawie bazy GS1. '
            product.company = expected_company

    if expected_brand:
        if product.brand:
            if result_product and product.brand.name != result_product.brand:
                LOGGER.info("Brand name mismatch. Creating a report.")
                create_bot_report(
                    product,
                    f"Wg. najnowszego odpytania w bazie ILiM marka tego produktu to: {result_product.brand!r}",
                    check_if_already_exists=not company_created,
                )
        else:
            LOGGER.info("A previously unknown brand was found. Updating the product.")
            product.brand = expected_brand
            product_commit_desc += 'Marka produktu zmieniona na podstawie bazy GS1. '

    if product.gpc_brick:
        if (
            result_product
            and result_product.gpc
            and len(result_product.gpc) > 0
            and product.gpc_brick.code != result_product.gpc[0].code
        ):
            LOGGER.info(
                "GPC Brick mismatch. Old value: %s, new name: %s, Creating a report.",
                product.name,
                result_product.name,
            )
            create_bot_report(
                product,
                f"Wg. najnowszego odpytania w bazie ILiM kod GPC tego produktu to: {result_product.gpc[0].code}",
                check_if_already_exists=not company_created,
            )
    else:
        if result_product and result_product.gpc:
            LOGGER.info("A previously unknown GPC Brick name was found. Updating the product.")
            product_commit_desc += 'Kod GPC zmieniony na podstawie bazy GS1. '
            product.gpc_brick = GPCBrick.objects.filter(code=result_product.gpc[0].code).first()

    product.gs1_last_response = get_products_response.dict()
    product.save(commit_desc=product_commit_desc)

    return product


def ensure_company_exists(result_company):
    have_info_about_company = bool(result_company and result_company.nip and result_company.name)
    company_created = False
    if have_info_about_company:
        LOGGER.info(
            "Result contains information about company: name=%s, nip=%s. Checking db.",
            result_company.name,
            result_company.nip,
        )
        expected_company, company_created = Company.objects.get_or_create(
            nip=result_company.nip,
            defaults={
                'name': result_company.name,
            },
            commit_desc='Firma utworzona automatycznie na podstawie API - Produkty w sieci',
        )
        LOGGER.info("Company created: %s", company_created)
    else:
        LOGGER.info("Result miss information about company.")
        expected_company = None
    return company_created, expected_company


def ensure_brand_exists(expected_company, result_product):
    brand_created = False

    if result_product.brand:
        LOGGER.info("Result contains information about brand: name=%s. Checking db.", result_product.brand)
        expected_brand, brand_created = Brand.objects.get_or_create(
            name=result_product.brand,
            company=expected_company,
            commit_desc='Marka utworzona automatycznie na podstawie API ILiM',
        )
        LOGGER.info("Brand created: %s", brand_created)
    else:
        LOGGER.info("Result miss information about brand.")
        expected_brand = None
    return brand_created, expected_brand


def ilim_compare_str(s1, s2):
    s1 = strip_dbl_spaces(s1)
    s2 = strip_dbl_spaces(s2)
    return s1.upper() == s2.upper()
