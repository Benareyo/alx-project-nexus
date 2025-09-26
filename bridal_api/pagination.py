# bridal_api/pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10                 # Default items per page
    page_size_query_param = 'page_size'  # Allow client to override
    max_page_size = 100            # Maximum items per page
