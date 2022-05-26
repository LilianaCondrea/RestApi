from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10
