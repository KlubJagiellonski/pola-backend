import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f'username{n}')
    name = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'pass')

    class Meta:
        model = 'users.User'  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('username',)


class StaffFactory(UserFactory):
    is_staff = True
    is_superuser = True
