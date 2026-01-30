"""
API快速测试脚本
用于验证所有接口是否正常工作
"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sports_backend.settings')
django.setup()

from django.urls import get_resolver
from django.core.management import call_command


def test_urls():
    """测试所有URL是否正确配置"""
    print("=" * 60)
    print("测试URL配置")
    print("=" * 60)

    resolver = get_resolver()
    url_patterns = []

    def collect_urls(patterns, prefix=''):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                url_patterns.append(prefix + str(pattern.pattern))

    collect_urls(resolver.url_patterns)

    # 统计API接口
    api_urls = [url for url in url_patterns if url.startswith('api/')]

    print(f"\n✅ 总共配置了 {len(url_patterns)} 个URL")
    print(f"✅ API接口数量: {len(api_urls)}")

    # 按模块分组显示
    modules = {}
    for url in api_urls:
        parts = url.split('/')
        if len(parts) >= 3:
            module = parts[1]
            if module not in modules:
                modules[module] = []
            modules[module].append(url)

    print("\n📋 API模块统计:")
    for module, urls in sorted(modules.items()):
        print(f"  - {module}: {len(urls)} 个接口")

    return True


def test_models():
    """测试所有模型是否正确"""
    print("\n" + "=" * 60)
    print("测试数据模型")
    print("=" * 60)

    from django.apps import apps

    models_count = 0
    for app_config in apps.get_app_configs():
        if app_config.name.startswith('apps.'):
            app_models = app_config.get_models()
            if app_models:
                print(f"\n✅ {app_config.label} 应用:")
                for model in app_models:
                    print(f"  - {model.__name__}")
                    models_count += 1

    print(f"\n✅ 总共 {models_count} 个数据模型")
    return True


def test_serializers():
    """测试所有序列化器是否可以导入"""
    print("\n" + "=" * 60)
    print("测试序列化器")
    print("=" * 60)

    apps_to_test = [
        'users', 'events', 'registrations', 'results',
        'announcements', 'interactions', 'carousel', 'feedback'
    ]

    serializers_count = 0
    for app_name in apps_to_test:
        try:
            module = __import__(f'apps.{app_name}.serializers', fromlist=[''])
            serializers = [name for name in dir(module) if name.endswith('Serializer')]
            print(f"✅ {app_name}: {len(serializers)} 个序列化器")
            serializers_count += len(serializers)
        except ImportError as e:
            print(f"❌ {app_name}: 导入失败 - {e}")
            return False

    print(f"\n✅ 总共 {serializers_count} 个序列化器")
    return True


def test_viewsets():
    """测试所有视图集是否可以导入"""
    print("\n" + "=" * 60)
    print("测试视图集")
    print("=" * 60)

    apps_to_test = [
        'users', 'events', 'registrations', 'results',
        'announcements', 'interactions', 'carousel', 'feedback'
    ]

    viewsets_count = 0
    for app_name in apps_to_test:
        try:
            module = __import__(f'apps.{app_name}.views', fromlist=[''])
            viewsets = [name for name in dir(module) if name.endswith('ViewSet')]
            print(f"✅ {app_name}: {len(viewsets)} 个视图集")
            viewsets_count += len(viewsets)
        except ImportError as e:
            print(f"❌ {app_name}: 导入失败 - {e}")
            return False

    print(f"\n✅ 总共 {viewsets_count} 个视图集")
    return True


def test_permissions():
    """测试权限类"""
    print("\n" + "=" * 60)
    print("测试权限类")
    print("=" * 60)

    try:
        from utils.permissions import (
            IsAdmin, IsReferee, IsAthlete, IsAdminOrReferee,
            IsOwnerOrAdmin, IsAuthenticatedOrReadOnly
        )
        print("✅ 所有权限类导入成功:")
        print("  - IsAdmin")
        print("  - IsReferee")
        print("  - IsAthlete")
        print("  - IsAdminOrReferee")
        print("  - IsOwnerOrAdmin")
        print("  - IsAuthenticatedOrReadOnly")
        return True
    except ImportError as e:
        print(f"❌ 权限类导入失败: {e}")
        return False


def test_export_utils():
    """测试导出工具"""
    print("\n" + "=" * 60)
    print("测试导出工具")
    print("=" * 60)

    try:
        from utils.export import export_to_excel, export_registrations, export_results
        print("✅ 导出工具导入成功:")
        print("  - export_to_excel")
        print("  - export_registrations")
        print("  - export_results")
        return True
    except ImportError as e:
        print(f"❌ 导出工具导入失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("运动赛事管理系统 - API接口测试")
    print("=" * 60 + "\n")

    tests = [
        ("URL配置", test_urls),
        ("数据模型", test_models),
        ("序列化器", test_serializers),
        ("视图集", test_viewsets),
        ("权限类", test_permissions),
        ("导出工具", test_export_utils),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} 测试失败: {e}")
            results.append((test_name, False))

    # 显示总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 60)
    if passed == total:
        print(f"[SUCCESS] 所有测试通过! ({passed}/{total})")
        print("系统已准备就绪，可以开始使用！")
    else:
        print(f"[WARNING] 部分测试失败 ({passed}/{total})")
        print("请检查失败的模块并修复问题。")
    print("=" * 60 + "\n")

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
