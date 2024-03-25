from rest_framework import serializers
from .models import User,Doctors
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        token['is_active'] = user.is_active
        token['blocked'] = user.blocked
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
      
        user = self.user
        password = attrs.get("password")
        print(password , 'lllllllllllllllllllllll')
        print(user.password,'uuuuuuuuuu')


        
        if user.blocked:
            print(user,'blocked')
            raise AuthenticationFailed('Your account is blocked due to some reason, please contact admin')

     
        if not user.check_password(password):
            print(user,'Passwordddddddddddd')
            raise AuthenticationFailed('Incorrect password')

        return data
    

    
class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','password2','is_doctor']
      
    
    def validate(self,data):
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        is_doctor = data.get('is_doctor')

    
        if password != password2:
            raise serializers.ValidationError('password doesnot match')
        
        if len(password)<8:
            raise serializers.ValidationError('password must contain atleast 8 charactors')
        
        return data
    def validate_email(self, value):
       
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email address is already in use.')
        return value




class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['department','hospital','is_verified']



class UserListSerializer(serializers.ModelSerializer):
    doctors = DoctorProfileSerializer()
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','doctors']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        

        if instance.is_doctor:
            print(instance,'insta')
            doctorProfile = validated_data.get('doctors')
            print(doctorProfile,"prtjfhuhsi")
            if doctorProfile:
                doctor,created = Doctors.objects.get_or_create(user=instance)
                doctor.hospital = doctorProfile.get('hospital',doctor.hospital)
                doctor.department = doctorProfile.get('department',doctor.department)
                doctor.save()
        instance.save()
        return instance


                




class AdminSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer(source='doctors')
    class Meta:
        model = User
        fields = ['pk','username','first_name','last_name','email','is_active','is_admin','blocked','is_doctor','is_staff','doctor']