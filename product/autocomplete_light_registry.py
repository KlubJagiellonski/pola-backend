import autocomplete_light
from .models import Product


class ProductAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name', 'code']
    model = Product
autocomplete_light.register(ProductAutocomplete)
