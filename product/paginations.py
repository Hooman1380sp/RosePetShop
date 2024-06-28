from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationSize10(PageNumberPagination):
    page_size = 10