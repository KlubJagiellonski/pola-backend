import factory.fuzzy


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'

    name = factory.Sequence(lambda n: f'product{n}')
    code = factory.sequence(lambda n: f'00000000{n}')

    @factory.post_generation
    def companies(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.companies.add(group)
