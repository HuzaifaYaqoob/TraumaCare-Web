from django.contrib import admin


from .models import BlogMedia, BlogPost, Tag, Category, BlogPostTopic
# Register your models here.


class TagsInline(admin.TabularInline):
    model = Tag
    extra = 0

class ImageInline(admin.TabularInline):
    model = BlogMedia
    extra = 1
    fields = ['image', 'thumbnail', 'mini_thumbnail']
    readonly_fields = ['thumbnail', 'mini_thumbnail']

@admin.register(BlogPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'images', 'category', 'tags', 'slug', 'created_at']
    #  'slug', 
    inlines = [TagsInline, ImageInline]

    def tags(self, obj):
        return obj.blog_tags_string
    
    def images(self, obj):
        images = obj.blog_post_medias.all()
        return len(images)

@admin.register(BlogMedia)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'image', 'thumbnail', 'mini_thumbnail']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(BlogPostTopic)
class BlogPostTopicAdmin(admin.ModelAdmin):
    list_display = ['name']