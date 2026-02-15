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
    通用的Excel数据导出函数
    
    将Django查询集的数据导出为Excel文件，支持嵌套属性访问、
    日期格式化、自动列宽调整等功能

    参数:
        queryset: Django ORM查询集，包含要导出的数据
        fields: 字段列表，如 ['field1', 'field2', 'user.username']
                支持点号访问嵌套属性（外键关联）
        headers: 表头列表，如 ['表头1', '表头2', '用户名']
                 与fields一一对应
        filename: 导出的文件名（不含.xlsx扩展名）
        
    返回:
        HttpResponse: 包含Excel文件的HTTP响应对象
        
    使用示例:
        export_to_excel(
            User.objects.all(),
            ['username', 'email', 'profile.phone'],
            ['用户名', '邮箱', '手机号'],
            'user_list_20240101'
        )
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
            # 这样可以访问外键关联的对象属性
            if '.' in field:
                value = obj
                for attr in field.split('.'):
                    value = getattr(value, attr, '')
            else:
                value = getattr(obj, field, '')

            # 处理日期时间类型，格式化为易读的字符串
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            # 如果值是可调用的（如模型方法），则调用它
            elif callable(value):
                value = value()

            # 将值转换为字符串，空值转换为空字符串
            row.append(str(value) if value is not None else '')

        ws.append(row)

    # 自动调整列宽，根据内容长度动态设置
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        # 设置列宽，最大不超过50个字符
        adjusted_width = min(max_length + 2, 50)  # 最大50个字符宽度
        ws.column_dimensions[column_letter].width = adjusted_width

    # 生成HTTP响应，设置正确的content-type
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # 设置文件名，触发浏览器下载
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'

    # 将工作簿保存到响应对象
    wb.save(response)
    return response


def sanitize_event_title(title):
    """
    清理赛事名称，去除文件名中不允许的特殊字符
    
    由于要将赛事名称用作文件名的一部分，需要移除或替换
    操作系统文件名中不允许的特殊字符，如 / \ : * ? " < > |
    
    处理流程:
        1. 移除所有非字母、非数字、非下划线、非连字符、非空格的字符
        2. 将空格和连续的连字符替换为单个下划线
        3. 如果标题为空，返回默认值

    参数:
        title: 原始赛事名称字符串
        
    返回:
        str: 清理后的安全文件名字符串
        
    示例:
        sanitize_event_title("2024年春季田径赛") -> "2024年春季田径赛"
        sanitize_event_title("比赛<测试>") -> "比赛测试"
        sanitize_event_title("马拉松 - 专业组") -> "马拉松_专业组"
    """
    if not title:
        return "未知赛事"
    # 仅保留中文、字母、数字和部分特殊字符
    # \w 匹配字母、数字、下划线和Unicode字符（包括中文）
    title = re.sub(r'[^\w\s-]', '', title)
    # 替换空格和连续的特殊字符为下划线，使文件名更规范
    title = re.sub(r'[-\s]+', '_', title)
    return title


def build_filename(base_name, timestamp, event_title=None):
    """
    构建标准化的下载文件名
    
    生成格式：基础名_赛事名_时间戳.xlsx
    例如：registration_list_2024春季运动会_20240101120000.xlsx
    
    参数:
        base_name: 文件名前缀，如 'registration_list'、'results_list'
        timestamp: datetime对象，用于生成时间戳
        event_title: 可选的赛事名称，如果提供则会清理后加入文件名
        
    返回:
        str: 完整的文件名（不含扩展名）
        
    示例:
        build_filename('registration_list', datetime.now(), '春季运动会')
        # 返回: 'registration_list_春季运动会_20240315143025'
        
        build_filename('results_list', datetime.now())
        # 返回: 'results_list_20240315143025'
    """
    if event_title:
        # 清理赛事名称，确保可以安全用作文件名
        event_title = sanitize_event_title(event_title)
        # 格式：基础名_赛事名_时间戳
        return f"{base_name}_{event_title}_{timestamp.strftime('%Y%m%d%H%M%S')}"
    # 如果没有赛事名称，只使用基础名和时间戳
    return f"{base_name}_{timestamp.strftime('%Y%m%d%H%M%S')}"


def export_registrations(queryset, event_title=None):
    """
    导出报名名单到Excel文件
    
    将赛事的报名记录导出为Excel表格，包含报名者的基本信息
    和报名状态等关键字段
    
    导出字段包括:
        - 赛事名称
        - 用户名
        - 真实姓名
        - 出生日期
        - 身份证号
        - 手机号
        - 报名时间
        - 审核状态
    
    参数:
        queryset: Registration模型的查询集，包含要导出的报名记录
        event_title: 可选的赛事名称，用于生成文件名
        
    返回:
        HttpResponse: 包含Excel文件的HTTP响应
        
    使用示例:
        registrations = Registration.objects.filter(event_id=1)
        return export_registrations(registrations, '春季运动会')
    """
    # 定义要导出的字段，支持通过点号访问关联对象的属性
    fields = [
        'event.title',              # 通过外键访问赛事标题
        'user.username',            # 通过外键访问用户名
        'user.real_name',           # 通过外键访问用户真实姓名
        'participant_birth_date',   # 参赛者出生日期
        'participant_id_card',      # 参赛者身份证号
        'participant_phone',        # 参赛者联系电话
        'created_at',               # 报名创建时间
        'status',                   # 报名审核状态
    ]
    # 定义Excel表格的表头
    headers = ['赛事名称', '用户名', '姓名', '出生日期', '身份证', '手机号', '报名时间', '审核状态']
    # 构建文件名，包含时间戳确保唯一性
    filename = build_filename('registration_list', datetime.now(), event_title)

    return export_to_excel(queryset, fields, headers, filename)


def export_results(queryset):
    """
    导出成绩表到Excel文件
    
    将赛事的成绩记录导出为Excel表格，包含参赛者信息、
    比赛轮次、排名和成绩等信息
    
    导出字段包括:
        - 赛事名称
        - 用户名
        - 真实姓名
        - 比赛轮次（预赛/半决赛/决赛等）
        - 排名
        - 成绩
    
    参数:
        queryset: Result模型的查询集，包含要导出的成绩记录
        
    返回:
        HttpResponse: 包含Excel文件的HTTP响应
        
    使用示例:
        results = Result.objects.filter(event_id=1, is_published=True)
        return export_results(results)
    """
    # 定义要导出的字段
    fields = [
        'event.title',      # 赛事标题
        'user.username',    # 参赛者用户名
        'user.real_name',   # 参赛者真实姓名
        'round_type',       # 比赛轮次
        'rank',             # 排名
        'score'             # 成绩（时间、分数等）
    ]
    # 定义Excel表格的表头
    headers = ['赛事名称', '用户名', '姓名', '轮次', '排名', '成绩']
    # 构建文件名
    filename = build_filename('results_list', datetime.now())

    return export_to_excel(queryset, fields, headers, filename)
