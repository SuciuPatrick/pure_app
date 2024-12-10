from django.core.cache import cache
from django.conf import settings
from functools import wraps
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


def cache_schedule_view(timeout=None):
    """
    Decorator to cache schedule view responses.
    Assumes JSON responses only.
    
    Args:
        timeout: Cache timeout in seconds. Defaults to settings.CACHE_TTL
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(view_instance, request, *args, **kwargs):
            cache_key = f"schedule:view:{request.get_full_path()}"
            
            # Try to get from cache
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                logger.info(f"Cache HIT for key: {cache_key}")
                return Response(cached_data)
            
            # If not in cache, generate response and cache it
            logger.info(f"Cache MISS for key: {cache_key}")
            response = view_func(view_instance, request, *args, **kwargs)
            cache.set(
                cache_key,
                response.data,
                timeout or getattr(settings, 'CACHE_TTL', 900)
            )
            logger.info(f"Cached data for key: {cache_key}")
            
            return response
        return wrapped_view
    return decorator


def invalidate_schedule_cache():
    """Clear all schedule-related cache entries"""
    cache.delete_pattern("schedule:view:*")
