from django.contrib.admin import SimpleListFilter
from django.db.models import Count

class ImageCountFilter(SimpleListFilter):
    title = 'Images Count' # or use _('country') for translated title
    parameter_name = 'Images Count'

    def lookups(self, request, model_admin):
        return [
            ('0', 'Zero Images'),
            ('1', '1 Image'),
            ('2', '2 Images'),
            ('3', '3 Images'),
            ('4', '4 Images'),
            ('5', '5 Images'),
            ('SIX_OR_PLUS', '6+ Images'),
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            if val == 'SIX_OR_PLUS':
                return queryset.annotate(images_count = Count('product_images')).filter(images_count__gte=6).order_by('images_count')
            return queryset.annotate(images_count = Count('product_images')).filter(images_count=val)