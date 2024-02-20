from django.template import library
from django.templatetags.static import static
from django.utils import safestring
from django.http import HttpRequest
from django.conf import settings
from django.core.cache.utils import make_template_fragment_key
from django.utils import (
    timezone,
    translation,
)
from wagtail.models import Locale


register = library.Library()

@register.inclusion_tag("locale_selector/locale_selector.html", takes_context=True, name="locale_selector")
def do_locale_selector(context, maintainer: str = None, maintainer_site: str = None, current_flag: bool = True, modal: bool = True, sticky: bool = True):
    request: HttpRequest = context.get("request")

    if not maintainer:
        maintainer = getattr(settings, "MAINTAINER", "Good Advice IT")

    if not maintainer_site:
        maintainer_site = getattr(settings, "MAINTAINER_SITE", "https://goodadvice.it")

    if callable(maintainer):
        maintainer = maintainer(
            request
        )

    if callable(maintainer_site):
        maintainer_site = maintainer_site(
            request
        )

    selector_tpl = "locale_selector/locale_selector_banner.html"
    if modal:
        selector_tpl = "locale_selector/locale_selector_modal.html"

    if hasattr(request, "cookie_consent"):
        immediately_show = False
        cookie_consent = getattr(request, "cookie_consent", None)
        if not getattr(cookie_consent, "submitted", False):
            immediately_show = True
    else:
        active_locale = translation.get_language()
        loc_sess_k = f"immediately_show_locale_selector_{active_locale}"
        immediately_show = request.session.get(loc_sess_k, True)

        if immediately_show:
            request.session[loc_sess_k] = False
            request.session.modified = True

    if hasattr(request, "site"):
        site_domain = getattr(request.site, "domain", f"{request.scheme}://{request.get_host()}")
    else:
        site_domain = f"{request.scheme}://{request.get_host()}"

    if "page" not in context:
        cache_key_components = [
            site_domain,
            request.path,
            translation.get_language(),
            request.user.is_authenticated,
            request.user.pk if request.user.is_authenticated else 0,
        ]
        context["page"] = {
            "get_cache_key_components": cache_key_components,
            "cache_key": make_template_fragment_key(
                "locale_selector",
                cache_key_components,
            ),
        }

    context["project_maintainer"] = maintainer
    context["project_maintainer_site"] = maintainer_site
    context["show_current_locale_flag"] = current_flag
    context["immediately_show"] = immediately_show
    context["selector_tpl"] = selector_tpl
    context["now"] = timezone.now()
    context["modal"] = modal
    context["sticky"] = sticky
    return context

@register.simple_tag(takes_context=True, name="locale_hello")
def do_locale_hello(context, locale: Locale):
    user = context.get("user")   
    if user and user.is_authenticated:
        return f"{do_translate_for_locale('Welcome,', locale)} {user.get_full_name()}"
    else:
        return do_translate_for_locale("Home", locale)

    
@register.simple_tag(takes_context=False, name="translate_for_locale")
def do_translate_for_locale(text: str, locale: Locale):
    code = locale
    if not isinstance(code, str):
        code = code.language_code

    if translation.check_for_language(code):
        with translation.override(code):
            translated = translation.gettext(text)
    else:
        translated = translation.gettext(text)
    return translated

@register.simple_tag(takes_context=False, name="translate_page_name_for_locale")
def do_translate_page_name_for_locale(page, locale: Locale):
    return do_translate_for_locale(f"View %s", locale) % page.title

@register.simple_tag(name="locale_flag")
def do_locale_flag(locale: Locale = None, size = None):
    lang_code = locale

    if not lang_code:
        lang_code = translation.get_language()

    if not isinstance(lang_code, str):
        lang_code = lang_code.language_code

    if size:
        return {
            "path": safestring.mark_safe(
                static(f"locale_selector/flags-4x3/{lang_code}.svg"),
            ),
            "size_css": safestring.mark_safe(f"--size:{str(size)};"),
            "lang_code": lang_code,
        }
    
    return safestring.mark_safe(
        static(f"locale_selector/flags-4x3/{lang_code}.svg"),
    )

