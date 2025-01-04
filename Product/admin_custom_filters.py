from django.contrib.admin import SimpleListFilter

class ImageCountFilter(SimpleListFilter):
    title = 'Images Count' # or use _('country') for translated title
    parameter_name = 'Images Count'

    def lookups(self, request, model_admin):
        return [('AFRICA', 'AFRICA - ALL')]

    def queryset(self, request, queryset):
        if self.value() == 'AFRICA':
            return queryset