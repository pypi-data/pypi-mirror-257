from celery import shared_task
from django.contrib.auth import get_user_model
from wagtail_localize.tasks import BaseJobBackend

import pickle # :(


class CeleryBackend(BaseJobBackend):

    def enqueue(self, func, args, kwargs):

        page_id, locales, components, user = args
        locale_ids = [l.pk for l in locales]
        components_data = pickle.dumps(components)
        user_id = user.pk
    
        do_translate_page_subtree.delay(page_id, locale_ids, components_data, user_id)


@shared_task(name="translate_page_subtree")
def do_translate_page_subtree(page_id, locale_ids, components_data, user_id):
    from wagtail.models import Locale
    from wagtail_localize.operations import (
        translate_page_subtree as translate_page_subtree_operation,
    )

    User = get_user_model()

    locales = Locale.objects.filter(pk__in=locale_ids)
    components = pickle.loads(components_data)
    user = User.objects.get(pk=user_id)

    translate_page_subtree_operation(page_id, locales, components, user)
    


