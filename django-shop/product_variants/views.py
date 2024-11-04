from .models import ProductVariant, VariantAttributeValue
from .serializers import ProductVariantSerializer, VariantAttributeValueSerializer
from rest_framework import viewsets, status
from products.models import Product
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .services import create_or_get_variant  # Assuming this is in a services module


class ProductsVariantViewsets(viewsets.ModelViewSet):
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        # If product_id is in the URL, filter variants for that product
        product_id = self.kwargs.get('product_id')
        if product_id:
            return ProductVariant.objects.filter(product_id=product_id)
        return ProductVariant.objects.all()

    def create(self, request, product_id=None):
        # Step 1: Get the product
        product = get_object_or_404(Product, id=product_id)

        # Step 2: Validate that all attribute IDs are provided
        attribute_ids = request.data.get("attributes")
        if not attribute_ids:
            return Response(
                {"error": "All required attributes must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 3: Attempt to create or retrieve existing variant
        variant, created = create_or_get_variant(
            product=product,
            attribute_ids=attribute_ids,
            name=request.data.get("name")
        )

        # Step 4: Prepare and send the response
        if created:
            return Response(
                {"variant_id": variant.id, "message": "New variant created."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"variant_id": variant.id, "message": "Variant already exists."},
                status=status.HTTP_200_OK,
            )


class VariantAttributeValueViewsets(viewsets.ModelViewSet):
    queryset = VariantAttributeValue.objects.all()
    serializer_class = VariantAttributeValueSerializer
