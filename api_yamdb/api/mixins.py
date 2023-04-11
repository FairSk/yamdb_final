from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class CreateDestroyListMixin(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
):
    pass
