from rest_framework import mixins, viewsets 


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    '''Кастомный вьюсет для наследования методов
    "list", "create", "destroy".'''

    pass
