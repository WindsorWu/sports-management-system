"""
Excel导出工具
用于导出报名名单和成绩表
"""
from openpyxl import Workbook
from django.http import HttpResponse
from datetime import datetime
import re


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


def sanitize_event_title(title):
    """
    清理赛事名称，去除特殊字符

    :param title: 原始赛事名称
    :return: 清理后的赛事名称
    """
    if not title:
        return "未知赛事"
    # 仅保留中文、字母、数字和部分特殊字符
    title = re.sub(r'[^\w\s-]', '', title)
    # 替换空格和连续的特殊字符为下划线
    title = re.sub(r'[-\s]+', '_', title)
    return title


def build_filename(base_name, timestamp, event_title=None):
    """
    构建下载文件名

    :param base_name: 基础文件名
    :param timestamp: 时间戳
    :param event_title: 赛事名称（可选）
    :return: 完整的文件名
    """
    if event_title:
        event_title = sanitize_event_title(event_title)
        return f"{base_name}_{event_title}_{timestamp.strftime('%Y%m%d%H%M%S')}"
    return f"{base_name}_{timestamp.strftime('%Y%m%d%H%M%S')}"


def export_registrations(queryset, event_title=None):
    """
    导出报名名单
    """
    fields = [
        'event.title',
        'user.username',
        'user.real_name',
        'participant_birth_date',
        'participant_id_card',
        'participant_phone',
        'created_at',
        'status',
    ]
    headers = ['赛事名称', '用户名', '姓名', '出生日期', '身份证', '手机号', '报名时间', '审核状态']
    filename = build_filename('registration_list', datetime.now(), event_title)

    return export_to_excel(queryset, fields, headers, filename)


def export_results(queryset):
    """
    导出成绩表
    """
    fields = [
        'event.title',
        'user.username',
        'user.real_name',
        'round_type',
        'rank',
        'score'
    ]
    headers = ['赛事名称', '用户名', '姓名', '轮次', '排名', '成绩']
    filename = build_filename('results_list', datetime.now())

    return export_to_excel(queryset, fields, headers, filename)
