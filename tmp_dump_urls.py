from django.urls import get_resolver
resolver = get_resolver()

def walk(patterns, prefix=''):
    for pattern in patterns:
        path = prefix + str(pattern.pattern)
        name = getattr(pattern, 'name', None)
        if 'referee-access' in path or (name and 'refereeaccess' in name):
            print('PATTERN', path, 'NAME', name)
        if hasattr(pattern, 'url_patterns'):
            walk(pattern.url_patterns, path)

walk(resolver.url_patterns)
