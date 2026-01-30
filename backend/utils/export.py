"""
Excel导出工具
用于导出报名名单和成绩表
"""
from openpyxl import Workbook
from django.http import HttpResponse
from datetime import datetime


def export_to_excel(queryset, fields, headers, filename):
    """
    导出数据到Excel

    :param queryset: Django查询集
    :param fields: 字段列表 ['field1', 'field2']
    :param headers: 表头列表 ['表头1', '表头2']
    :param filename: 文件名（不含扩展名）
    :return: HttpResponse
    """
    # 创建工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = "数据导出"

    # 写入表头
    ws.append(headers)

    # 设置表头样式（加粗）
    for cell in ws[1]:
        cell.font = cell.font.copy(bold=True)

    # 写入数据
    for obj in queryset:
        row = []
        for field in fields:
            # 支持点号访问嵌套属性  eg: 'user.username'
            if '.' in field:
                value = obj
                for attr in field.split('.'):
                    value = getattr(value, attr, '')
            else:
                value = getattr(obj, field, '')

            # 处理日期时间类型
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif callable(value):
                value = value()

            row.append(str(value) if value is not None else '')

        ws.append(row)

    # 自动调整列宽
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)  # 最大50个字符宽度
        ws.column_dimensions[column_letter].width = adjusted_width

    # 生成HTTP响应
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'

    wb.save(response)
    return response


def export_registrations(queryset):
    """
    导出报名名单
    """
    fields = [
        'event.name',
        'user.username',
        'user.real_name',
        'user.phone',
        'registered_at',
        'status',
    ]
    headers = ['赛事名称', '用户名', '姓名', '手机号', '报名时间', '审核状态']
    filename = f'registration_list_{datetime.now().strftime("%Y%m%d%H%M%S")}'

    return export_to_excel(queryset, fields, headers, filename)


def export_results(queryset):
    """
    导出成绩表
    """
    fields = [
        'event.name',
        'user.username',
        'user.real_name',
        'score',
        'rank',
        'created_at',
    ]
    headers = ['赛事名称', '用户名', '姓名', '成绩', '名次', '录入时间']
    filename = f'results_list_{datetime.now().strftime("%Y%m%d%H%M%S")}'

    return export_to_excel(queryset, fields, headers, filename)
