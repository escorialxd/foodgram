from rest_framework.pagination import PageNumberPagination


class RecipePagination(PageNumberPagination):
    """Recipe pagination configuration."""

    page_size = 6
    page_size_query_param = "limit"
