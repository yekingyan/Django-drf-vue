
class SimplePage:

    def get_paginated_response(self, data):
        """
        调整返回的json结构，去除'next'、'previous'字段
        """
        from collections import OrderedDict
        from rest_framework.response import Response
        return Response(OrderedDict([
            ('count', self._paginator.page.paginator.count),
            # ('next', self._paginator.get_next_link()),
            # ('previous', self._paginator.get_previous_link()),
            ('results', data)
        ]))
