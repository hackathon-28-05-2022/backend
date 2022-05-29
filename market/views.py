from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from .serializer import LotSerializer
from .models import Lot


# Create your views here.

class ListLots(generics.ListAPIView):
    serializer_class = LotSerializer

    def get_queryset(self):
        return Lot.objects.filter(is_closed=False)


class BuyLot(APIView):
    def post(self, request):
        lot_id = request.POST.data.get('lot_id')
        lot = Lot.objects.get(id=lot_id)
        return lot.buy_lot(request.user)
