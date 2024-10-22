from rest_framework import viewsets
from .models import Vendor, VendorRating, VendorTransaction
from .serializers import (
    VendorSerializer,
    VendorRatingSerializer,
    VendorTransactionSerializer,
)


class VendorViewsets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


# class VendorViewSet(generics.ListCreateAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
# permission_classes = [IsAuthenticated]

# def get_queryset(self):
#     return self.queryset.filter(user=self.request.user)


class VendorRatingViewsets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = VendorRating.objects.all()
    serializer_class = VendorRatingSerializer


class VendorTransactionViewsets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = VendorTransaction.objects.all()
    serializer_class = VendorTransactionSerializer
