from django.contrib import admin

from Secure.models import XpoKey, ApplicationReview
# Register your models here.


admin.site.register(XpoKey)

@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'email', 'rating', 'created_at' ]
