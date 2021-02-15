import factory.fuzzy


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'product.Product'

    name = factory.Sequence(lambda n: 'product%s' % n)
    code = factory.sequence(lambda n: '00000000%s' % n)

    @factory.post_generation
    def companies(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.companies.add(group)
