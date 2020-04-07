from .models import foundation, spr_type_foundation, company, spr_type_company, housing_stock, spr_type_stock, munitipal_land
from .models import holder
from rest_framework_gis.serializers import GeoFeatureModelSerializer, ModelSerializer
from rest_framework import serializers


class HolderSerializer(ModelSerializer):
    class Meta:
        model = holder
        fields = ('holder_num', 'name', 'phone', 'address', 'fio')

class FoundationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = foundation
        geo_field = 'coordinates'
        fields = ('id', 'name', 'type', 'address', 'square', 'describe', 'holder_num')


class SprTypeFoundSerializer(ModelSerializer):
    class Meta:
        model = spr_type_foundation
        fields = ('type', 'description', 'purpose')
        

class CompanySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = company
        geo_field = 'coordinates'
        fields = ('id', 'name', 'type', 'address', 'square', 'describe', 'holder_num')


class SprTypeCompanySerializer(ModelSerializer):
    class Meta:
        model = spr_type_company
        fields = ('type', 'description')


class HousingStockSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = housing_stock
        geo_field = 'coordinates'
        fields = ('id', 'type', 'address', 'square', 'describe', 'floors', 'holder_num')


class SprTypeStockSerializer(ModelSerializer):
    class Meta:
        model = spr_type_stock
        fields = ('type', 'description')


class MunitipallandSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = munitipal_land
        geo_field = 'coordinates'
        fields = ('id', 'name', 'purpose', 'square', 'describe', 'holder_num')
