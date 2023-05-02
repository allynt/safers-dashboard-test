from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from safers.core.decorators import swagger_fake

from safers.users.models import User
from safers.users.permissions import IsUserOrAdmin
from safers.users.serializers import UserSerializer


class UserView(
    # generics.CreateAPIView,  # creating users is handled by RegisterView
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsAuthenticated, IsUserOrAdmin]
    queryset = User.objects.active()
    serializer_class = UserSerializer

    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    @swagger_fake(None)
    def get_object(self):
        if self.kwargs[self.lookup_url_kwarg] == "current":
            return self.request.user
        return super().get_object()

    def delete(self, request, *args, **kwargs):
        retval = super().delete(request, *args, **kwargs)
        # TODO: (logout and) delete user from auth
        return retval

    def perform_update(self, serializer):
        retval = super().perform_update(serializer)
        # TODO: synchronize profile w/ auth
        return retval
