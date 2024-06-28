from django.contrib import admin


from .models import BlogMedia, BlogPost, Tag, Category
# Register your models here.


class TagsInline(admin.TabularInline):
    model = Tag
    extra = 0

@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'tags', 'created_at']
    inlines = [TagsInline]

    def tags(self, obj):
        tags = obj.tags.all()
        return ', '.join([tag.name for tag in tags])

@admin.register(BlogMedia)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'image']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']