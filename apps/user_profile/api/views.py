from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED

from apps.user_profile.api.serializers import UserProfileRetrieveSerializer, UserProfileCreateUpdateSerializer, \
    UserProfileAuthSerializer, UserProfileRetrieveUpdateSerializer


class UserProfileCreateAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = UserProfileCreateUpdateSerializer
    retrieve_serializer = UserProfileRetrieveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = self.retrieve_serializer(user).data
        response_data['auth_token'] = user.auth_token.key
        return Response(response_data, status=HTTP_201_CREATED)


class UserProfileAuthAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = UserProfileAuthSerializer
    retrieve_serializer = UserProfileRetrieveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        response_data = self.retrieve_serializer(user).data
        auth_token, _ = Token.objects.get_or_create(user=user)
        response_data['auth_token'] = user.auth_token.key
        return Response(response_data)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class UserProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileRetrieveUpdateSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user
