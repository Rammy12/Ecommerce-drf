from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    keyword=filters.CharFilter(field_name='Name',lookup_expr="icontains")
    min_price=filters.NumberFilter(field_name='Price' or 0,lookup_expr="gte")
    max_price=filters.NumberFilter(field_name='Price' or 10000000,lookup_expr="lte")
    class Meta:
        model=Product
        fields=('keyword','Category','Brand','min_price','max_price')

