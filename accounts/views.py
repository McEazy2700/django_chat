from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import status
from .serializers import AuthSerializer, RegisterSerializer

# Create your views here.


@api_view(['POST'])
def login(request: Request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request,
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password"),
        )
        if user is not None:
            # login(request, user)
            try:
                token = Token.objects.get(user=user)
                print(token.user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            response = {"success": True, "user": {"id": user.id, "token": token.key}}
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def logout(request: Request, id):
    try:
        user_token = Token.objects.get(user__id=id)
        print({"token": user_token, "user": user_token.user})
        user_token.delete()
    except Token.DoesNotExist:
        pass
    # logout(request)
    return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def sign_up(request: Request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(validated_data=serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
