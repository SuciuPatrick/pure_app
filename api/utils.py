from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class StandardResultsSetPagination(LimitOffsetPagination):
    """
    Standard pagination class for all endpoints using limit/offset pagination.
    Includes both total count and current page count in the response.
    """

    default_limit = 100
    max_limit = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.count,
                "page_count": len(data),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
