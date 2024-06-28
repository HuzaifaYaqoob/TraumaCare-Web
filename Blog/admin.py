from django.contrib import admin


from .models import BlogMedia, BlogPost, Tag, Category
# Register your models here.


class TagsInline(admin.TabularInline):
    model = Tag
    extra = 0

@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    inlines = [TagsInline]

@admin.register(BlogMedia)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'image']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']