
"""api.v1.educator package

Expose educator submodules for explicit imports. This package intentionally
imports submodules to ensure attribute access like `api.v1.educator.course_views`
works when Django resolves URL modules.
"""

"""Package for educator API (submodules are imported lazily by Django)."""

__all__ = [
	'views', 'serializers', 'course_views', 'urls', 'auth_views'
]
