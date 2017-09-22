import importlib
from django.conf import settings

# Assets with be cached the first 
# time module is imported.

_js = {}
_css = {}
cached = False


def _add_namespace(namespace, data):
    """
    Add namespace:key to each key in data.
    """

    new_data = {}

    for key in data.keys():
        new_data["%s:%s" % (namespace, key)] = data[key]

    print(new_data)
    return new_data

def _assets_from_apps():
    """
    Search the INSTALLED_APPS for assets.py files,
    and fill the js/css with its contents. Namespace
    bundles with their app's name.
    """
    for app in settings.INSTALLED_APPS:
        try:
            assets = importlib.import_module("%s.assets"% app)
            js = getattr(assets, "PIPELINE_JS", {})
            css = getattr(assets, "PIPELINE_CSS", {})

            js = _add_namespace(app, js)
            css = _add_namespace(app, css)

            _js.update(js)
            _css.update(css)
        except ImportError:
            continue

if not cached:
    _assets_from_apps()
    cached = True


def find_js():
    return _js

def find_css():
    return _css
