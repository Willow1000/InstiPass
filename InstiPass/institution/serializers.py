from rest_framework import serializers
from .models import *

class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = "__all__"

class InstitutionSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstitutionSettings
        fields = "__all__"        