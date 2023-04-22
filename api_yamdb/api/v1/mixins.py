from rest_framework import viewsets, mixins


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    '''Кастомный вьюсет для наследования методов
    "list", "create", "destroy".'''

    pass
