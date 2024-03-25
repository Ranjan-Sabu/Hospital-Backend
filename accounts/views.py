from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializers import UserRegisterSerializer,MyTokenObtainPairSerializer,UserListSerializer,AdminSerializer
from accounts.models import User,Doctors
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from django.db.models import Q



# Create your views here.

class Registration(APIView):

    def post(self,request,format = None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():

            first_name=serializer.validated_data.get('first_name')
            last_name=serializer.validated_data.get('last_name')
            username=serializer.validated_data.get('username')
            email=serializer.validated_data.get('email')
            password=serializer.validated_data.get('password')
            is_doctor=serializer.validated_data.get('is_doctor')

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_doctor=is_doctor
            )
            if user.is_doctor:
                Doctors.objects.create(user=user)
            return Response({'msg':'data inserted'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    



class UserProfileView(APIView):

    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserListSerializer(user)
        return Response({'msg':'user','data':serializer.data},status=status.HTTP_200_OK)

 

    def patch(self, request):
        user = request.user
        data = request.data
        serializer = UserListSerializer(instance=user,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request):
        user = request.user

        if user.is_doctor:
            try:
                doctor_profile = Doctors.objects.get(user=user)
                doctor_profile.delete()
                return Response({'detail': 'Doctor profile deleted.'}, status=status.HTTP_204_NO_CONTENT)
            except Doctors.DoesNotExist:
                return Response({'detail': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                user_profile = User.objects.get(id=user.id)
                user_profile.delete()
                return Response({'detail': 'User profile deleted.'}, status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
            

class UserDoctorView(APIView):
    def get(self, request):
        doctors = User.objects.filter(is_doctor=True)
        serializer = UserListSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AdminViewUsers(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminSerializer
    queryset = User.objects.filter(is_admin=False)


    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            print(user)
            user.blocked = not user.blocked
            
            user.save()
            serializer = AdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer