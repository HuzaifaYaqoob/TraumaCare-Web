from django.db import models

# Create your models here.



import re
def convert_to_html(content):
    # Replace '**' for bold text
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    
    # Replace '*' or '_' for italic text
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    content = re.sub(r'\_(.*?)\_', r'<em>\1</em>', content)
    
    # Replace '~~' for strikethrough text
    content = re.sub(r'\~\~(.*?)\~\~', r'<del>\1</del>', content)
    
    # Replace '`' for inline code
    content = re.sub(r'\`(.*?)\`', r'<code>\1</code>', content)
    
    # Replace links
    content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
    
    # Replace '\n' for new lines
    content = content.replace('\n', '<br>')
    
    # Handle nested Markdown (bold and italic together)
    content = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', content)
    
    # Handle bullet points (unordered lists)
    content = re.sub(r'^\s*-\s+(.*)', r'<li>\1</li>', content, flags=re.MULTILINE)
    if '<li>' in content:
        content = '<ul>' + content + '</ul>'
        content = content.replace('<ul><br>', '<ul>')
        content = content.replace('<br></li>', '</li>')
    
    return content


class Category(models.Model):
    name = models.CharField(max_length=999, default='')
    slug = models.CharField(max_length=999, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        name = self.name
        name = name.replace(' ', '-').replace('/', '-').replace('--', '-')
        name = name.lower()
        self.slug = f'{name}-{self.id}'
        super(Category, self).save(*args, **kwargs)
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts', default=None)
    content = models.TextField()
    read_time = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.content = convert_to_html(self.content)
        super(BlogPost, self).save(*args, **kwargs)


class BlogMedia(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='Blog/Images/%Y-%m', default='')

    def __str__(self):
        return self.post.title


class Tag(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name