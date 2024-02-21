from wagtail import hooks

css_path = "locale_selector/css/locale_selector.css"
js_path = "locale_selector/js/locale_selector.js"

@hooks.register("register_global_site_static")
def register_global_site_static(request, context):
    return [
        css_path,
    ]

@hooks.register("register_global_site_scripts")
def register_global_site_scripts(request, context):
    return [
        js_path,
    ]
