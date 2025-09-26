# bridal_api/filters.py
import django_filters
from .models import Product, Category, Collection, Designer

# Product filter
class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.NumberFilter(field_name="category__id", lookup_expr='exact')
    designer = django_filters.NumberFilter(field_name="designer__id", lookup_expr='exact')
    collection = django_filters.NumberFilter(field_name="collection__id", lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'designer', 'collection', 'min_price', 'max_price']


# Category filter
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']


# Collection filter
class CollectionFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Collection
        fields = ['title']


# Designer filter
class DesignerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Designer
        fields = ['name']
