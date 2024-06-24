# Django One-Shot

Complete the project specs from Learn.

## Optional Debugging Tool Setup:

### Install Django Debug Toolbar

This toolbar will help you have visibility such as over your context in templates and the queries that are running to get your model data.

https://django-debug-toolbar.readthedocs.io/en/latest/

### Pip Install

```bash
python -m pip install django-debug-toolbar
```

### Install the App

Add `"debug_toolbar"` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # ...
    "debug_toolbar",
    # ...
]
```

### Add to urls

Add django-debug-toolbar’s URLs to your project’s URLconf `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
]
```

### Add to MIDDLEWARE

Add it to your `MIDDLEWARE` setting in `settings.py`:

```python
MIDDLEWARE = [
    # ...
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]
```

### Add to INTERNAL_IPS

Add the following to `settings.py`:

```python
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
```

