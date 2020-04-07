from rest_framework import viewsets
from django.views.generic import View
from django.shortcuts import render

from .models import foundation, spr_type_foundation, company, spr_type_company, housing_stock, spr_type_stock, munitipal_land
from .models import holder
from .serializers import FoundationSerializer, SprTypeFoundSerializer, CompanySerializer, SprTypeCompanySerializer
from .serializers import HousingStockSerializer, SprTypeStockSerializer, MunitipallandSerializer
from .serializers import HolderSerializer

class FrontEndView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class FoundationViewSet(viewsets.ModelViewSet):
    serializer_class = FoundationSerializer
    queryset = foundation.objects.all()

class SprTypeFoundationViewSet(viewsets.ModelViewSet):
    serializer_class = SprTypeFoundSerializer
    queryset = spr_type_foundation.objects.all()

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = company.objects.all()

class SprTypeCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = SprTypeCompanySerializer
    queryset = spr_type_company.objects.all()

class HousingStockViewSet(viewsets.ModelViewSet):
    serializer_class = HousingStockSerializer
    queryset = housing_stock.objects.all()

class SprTypeStockViewSet(viewsets.ModelViewSet):
    serializer_class = SprTypeStockSerializer
    queryset = spr_type_stock.objects.all()

class MunitipallandViewSet(viewsets.ModelViewSet):
    serializer_class = MunitipallandSerializer
    queryset = munitipal_land.objects.all()

class HolderViewSet(viewsets.ModelViewSet):
    serializer_class = HolderSerializer
    queryset = holder.objects.all()