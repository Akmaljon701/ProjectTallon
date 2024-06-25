from rest_framework.serializers import ModelSerializer
from api.models import Branch, Organization, Tallon


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class TallonSerializer(ModelSerializer):
    class Meta:
        model = Tallon
        fields = '__all__'
