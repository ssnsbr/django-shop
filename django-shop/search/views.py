from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from vendors.models import Vendor
from products.serializers import ProductSerializer
from vendors.serializers import VendorSerializer
from django.db.models import Q
from rest_framework.permissions import AllowAny


class SearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("q", None)
        category = request.query_params.get("category", None)
        price_min = request.query_params.get("price_min", None)
        price_max = request.query_params.get("price_max", None)

        if not query:
            return Response(
                {"error": "No search query provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Building the query for products
        product_filter = Q(name__icontains=query) | Q(description__icontains=query)
        if category:
            product_filter &= Q(category__name__icontains=category)
        if price_min and price_max:
            product_filter &= Q(price__gte=price_min, price__lte=price_max)

        products = Product.objects.filter(product_filter)
        product_results = ProductSerializer(products, many=True).data

        # Searching for vendors by store name
        vendors = Vendor.objects.filter(store_name__icontains=query)
        vendor_results = VendorSerializer(vendors, many=True).data

        return Response(
            {
                "products": product_results,
                "vendors": vendor_results,
            },
            status=status.HTTP_200_OK,
        )
