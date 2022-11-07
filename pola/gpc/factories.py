import factory.fuzzy


class GPCSegmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'gpc.GPCSegment'

    code = factory.sequence(lambda n: f"{n:013}")
    text = factory.Sequence(lambda n: f'segment{n}')


class GPCFamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'gpc.GPCFamily'

    parent = factory.SubFactory(GPCSegmentFactory)
    code = factory.sequence(lambda n: f"{n:013}")
    text = factory.Sequence(lambda n: f'family{n}')


class GPCClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'gpc.GPCClass'

    parent = factory.SubFactory(GPCFamilyFactory)
    code = factory.sequence(lambda n: f"{n:013}")
    text = factory.Sequence(lambda n: f'class{n}')


class GPCBrickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'gpc.GPCBrick'

    parent = factory.SubFactory(GPCClassFactory)
    code = factory.sequence(lambda n: f"{n:013}")
    text = factory.Sequence(lambda n: f'brick{n}')
