from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from vendor_products.models import VendorProduct
from vendor_products.permissions import IsOwnerOrReadOnly, IsVendorOwner
from vendor_products.serializers import VendorProductSerializer, is_valid_uuid
from rest_framework import status


class VendorProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for VendorProduct model.
    Supports filtering by product and vendor IDs.
    """

    permission_classes = [IsOwnerOrReadOnly, IsVendorOwner]
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    def get_queryset(self):
        """
        Optionally filters the queryset by product_id and vendor_id from the request parameters.
        """
        product_id = self.request.GET.get("p")
        vendor_id = self.request.GET.get("v")
        queryset = VendorProduct.objects.all()

        if product_id:
            if is_valid_uuid(product_id):
                queryset = queryset.filter(product_id=product_id)
            else:
                raise Http404({"detail": f"Invalid UUID: {product_id}"})

        if vendor_id:
            if is_valid_uuid(vendor_id):
                queryset = queryset.filter(vendor_id=vendor_id)
            else:
                raise Http404({"detail": f"Invalid UUID: {vendor_id}"})

        return queryset

    def get_object(self):
        """
        Retrieves the object by primary key (pk) from the filtered queryset.
        """
        pk = self.kwargs.get("pk")
        if is_valid_uuid(pk):
            return get_object_or_404(self.get_queryset(), pk=pk)
        else:
            raise Http404({"detail": f"Invalid UUID: {pk}"})

    def update(self, request, *args, **kwargs):
        """
        Custom update to check object permissions before updating.
        """
        print("Update operation triggered")
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        response = super().update(request, *args, **kwargs)
        print("Update successful")
        return response
