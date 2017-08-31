from django.core.cache import cache


def get_value(key):
    return cache.get(key)


def get_search_result():
    return get_value('search_result')


def store_search_result(result):
    cache_key = 'search_result'
    cache_time = 1800  # secs
    cache.set(cache_key, result, cache_time)
