from django.shortcuts import render
from rest_framework import generics
from .serializer import LotSerializer
from .models import Lot


# Create your views here.

class ListLots(generics.ListAPIView):
    serializer_class = LotSerializer

    def get_queryset(self):
        return Lot.objects.filter(is_closed=False)
