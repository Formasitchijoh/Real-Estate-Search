from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed

import jwt
import datetime

# Create your views here.

from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
import datetime

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        #find user using email
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found:)')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

       
        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token.decode('utf-8')
        #we set token via cookies
        

        response = Response() 

        response.set_cookie(key='jwt', value=token, httponly=True)  #httonly - frontend can't access cookie, only for backend

        response.data = {
            'jwt token': token
        }

        #if password correct
        return response


# get user using cookie
class UserViews(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
            #decode gets the user

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
        #cookies accessed if preserved

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
            user = User.objects.filter(id=payload['id']).first()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successful'
        }

        return response