from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from wagtail_webradio.models import Podcast, RadioShow


class PodcastsSitemap(Sitemap):
    def items(self):
        return Podcast.objects.currents()

    def lastmod(self, obj):
        return obj.publish_date

    def location(self, obj):
        return reverse("core:podcast_detail", args=[obj.pk])


class RadioShowsSitemap(Sitemap):
    def items(self):
        return RadioShow.objects.all()

    def lastmod(self, obj):
        return Podcast.objects.filter(radio_show=obj).last().publish_date

    def location(self, obj):
        return reverse("core:radioshow_detail", args=[obj.pk])
