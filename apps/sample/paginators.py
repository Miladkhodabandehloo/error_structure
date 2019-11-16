from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from best_practice.utils.response_utils import APIResponse


class CustomPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return APIResponse(data=data, pagination={
            "items_count": self.page.paginator.count,
            "current_page": self.page.number,
            "pages_count": self.page.paginator.num_pages,
        })
