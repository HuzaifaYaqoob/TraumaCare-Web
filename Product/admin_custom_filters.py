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
            ('6', '6 Images'),
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            return queryset.annotate(images_count = Count('product_images')).filter(images_count=val)