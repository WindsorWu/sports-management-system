"""
分页工具模块
提供自定义的分页类，用于API响应的分页处理
"""
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页类
    
    继承自DRF的PageNumberPagination，提供灵活的分页配置
    
    属性说明:
        page_size_query_param: 用于指定每页大小的URL参数名，例如 ?page_size=20
        max_page_size: 每页允许返回的最大记录数，防止一次查询过多数据
    
    使用示例:
        GET /api/users/?page=1&page_size=20
        # 返回第1页的数据，每页20条记录
    """
    page_size_query_param = 'page_size'  # 允许客户端通过URL参数控制每页大小
    max_page_size = 1000  # 限制每页最多返回1000条记录
