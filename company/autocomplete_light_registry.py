import autocomplete_light
from .models import Company


class CompanyAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name', 'official_name', 'common_name']
    model = Company
autocomplete_light.register(CompanyAutocomplete)
