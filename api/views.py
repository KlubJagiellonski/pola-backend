from api.error_codes import BARCODE_NOT_VALID
from api.gs1 import GS1Api
from api.models import Product, Company
from api.utils import create_json_http_response, create_error_json_http_response, correct_barcode


def product(request, barcode):
    if not correct_barcode(barcode):
        return create_error_json_http_response(BARCODE_NOT_VALID)
    
    product = Product.objects.filter(barcode=barcode).first()
    if product is None:
        product = Product(barcode=barcode)

        product.fill_from_barcode(barcode)

        gs1Content = GS1Api.get_product_by_gtin(barcode)

        gs1Data = gs1Content['Data'] if ('Data' in gs1Content) else None
        if gs1Data:
            gs1ProductInfo = gs1Data['Product'] if ('Product' in gs1Data) else None
            if gs1ProductInfo:
                product.fill_from_gs1_product_info(gs1ProductInfo)

            gs1OwnerInfo = gs1Data['Owner'] if ('Owner' in gs1Data) else None
            if gs1OwnerInfo:
                company = Company.find_by_gs1_owner_info(gs1OwnerInfo)
                if not company:
                    company = Company()
                    company.fill_from_gs1(gs1OwnerInfo)
                    company.save()
                product.company = company

        gs1Information = gs1Content['CGs1Information'] if ('CGs1Information' in gs1Content) else None
        if gs1Information:
            product.fill_from_gs1_info(gs1Information)

    product.number_of_api_calls += 1
    product.save()

    return create_json_http_response(product.dict_representation())
