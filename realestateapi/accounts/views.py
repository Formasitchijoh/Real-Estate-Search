# authentication/views.py

from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from recommendations.models import Recommendation
from recommendations.serializers import RecommendationSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            
            user_recommendations = Recommendation.objects.filter(user=user.pk).first()
            if user_recommendations:
                recommendation = RecommendationSerializer(user_recommendations).data
                print('\n\n hellllle\n\n',recommendation)
                return Response({
                    'id': user.id,
                    'token': token.key,
                    'username': user.username,
                    "email":user.email,
                    'role': user.role,
                    'recommendation': recommendation
                })
            
            else:
                return Response({
                'id': user.id,
                'token': token.key,
                "email":user.email,
                'username': user.username,
                'role': user.role
            })
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLoginViews(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            user_recommendations = Recommendation.objects.filter(user=user.pk).first()
            if user_recommendations:
                recommendation = RecommendationSerializer(user_recommendations)
                return Response({'id':user.id, 'token': token.key, 'username': user.username, 'role': user.role,"recommendation":recommendation})
            return Response({'id':user.id, 'token': token.key, 'username': user.username, 'role': user.role})
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})