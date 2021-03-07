import factory.fuzzy
from django.utils import timezone

from product.factories import ProductFactory


class AIPicsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ai_pics.AIPics'

    product = factory.SubFactory(ProductFactory)
    client = factory.sequence(lambda n: f"client{n}")
    created_at = factory.lazy_attribute(lambda o: timezone.now())

    original_width = 800
    original_height = 800

    width = 800
    height = 800

    device_name = factory.sequence(lambda n: f"client{n}")
    flash_used = factory.sequence(lambda n: n % 2 == 0)
    was_portrait = factory.sequence(lambda n: n % 3 == 0)

    is_valid = factory.sequence(lambda n: n % 4 == 0)


class AIAttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ai_pics.AIAttachment'

    ai_pics = factory.SubFactory(AIPicsFactory)
    attachment = factory.django.ImageField(width=200, height=200, filename=factory.sequence(lambda n: f"client{n}.png"))
