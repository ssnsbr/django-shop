from django.db import models
import uuid


class Attribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AttributeOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=255)  # e.g., "XS", "S", "M", "L", etc.

    class Meta:
        unique_together = ('attribute', 'value')  # Ensures no duplicate options for an attribute

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class AttributeValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    option = models.ForeignKey(AttributeOption, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'option')

    def __str__(self):
        return f"{self.option.attribute.name}: {self.option.value}"
