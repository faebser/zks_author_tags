__author__ = 'faebser'

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class TagsAndAuthors(CMSApp):
    name = "Tags und Autoren"
    urls = ["author_and_tags.urls"]

apphook_pool.register(TagsAndAuthors)