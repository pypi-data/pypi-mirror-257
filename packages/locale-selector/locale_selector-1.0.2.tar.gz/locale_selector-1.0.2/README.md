locale_selector
================

A simple language selector pop-up modal for Django/Wagtail.

Has 2 integrated backends for wagtail-localize translate page subtree tasks.
 - `locale_selector.jobs.ThreadedBackend`
 - `locale_selector.tasks.CeleryBackend`

Quick start
-----------

1. Add 'locale_selector' to your INSTALLED_APPS setting like this:

```
INSTALLED_APPS = [
   ...,
   'locale_selector',
]
```

2. Add the following staticfiles accordingly:
```sh
locale_selector/css/locale_selector.css
locale_selector/js/locale_selector.js
```

3. Use the templatetag in your base.html:
```html
{% load locale_selector %}
...

{# maintainer        Which maintainer do you want to display      #}
{# maintainer_site   Which maintainer site do you want to display #}
{# current_flag      Show the flag for the current language       #}
{# modal             Show a modal or banner                       #}
{# sticky            Make the modal/banner open/close button sticky in the document #}

{% locale_selector current_flag=True modal=False sticky=True %}
```