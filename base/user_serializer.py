from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(UserDetailsSerializer):
    role = serializers.CharField(source="userprofile.role")

    class Meta:
        model = User
        fields = UserDetailsSerializer.Meta.fields + ('role', 'id')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        role = profile_data.get('role')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.userprofile
        if profile_data and role:
            profile.role = role
            profile.save()
        return instance

class UserRegisterSerializer(RegisterSerializer):
    VALID_DOMAINS = (
        "husky.neu.edu",
        "northeastern.edu",
        "neu.edu",
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    def validate_username(self, username):
        """
        Return the username (email) if it is a valid Northeastern address.
        """
        email = super(UserRegisterSerializer, self).validate_username(username)
        domain = email.split('@')[-1]
        if domain not in self.VALID_DOMAINS:
            raise serializers.ValidationError(
                    _("Not a valid Northeastern email address."))
        return email

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }
