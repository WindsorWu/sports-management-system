from django.urls import get_resolver

resolver = get_resolver()

def walk(patterns, prefix=''):
    for pattern in patterns:
        path = prefix + str(pattern.pattern)
        if 'referee-access' in path:
            print(path)
        if hasattr(pattern, 'url_patterns'):
            walk(pattern.url_patterns, path)

walk(resolver.url_patterns)
