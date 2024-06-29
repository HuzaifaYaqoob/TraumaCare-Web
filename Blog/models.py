from django.db import models

# Create your models here.



import re
def convert_to_html(content):

    # Replace matched patterns with corresponding HTML tags
    
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
    
    print('done')
    content = re.sub(r'(#{1,3})\s*(.*?)($|<br>|<br\/>)($|<br>|<br\/>)(.*?)(?=$|#)', lambda match: f'<h{len(match.group(1))}>{match.group(2).strip()}</h{len(match.group(1))}>{match.group(3)}<div>{match.group(5)}</div>{match.group(4)}', content, flags=re.MULTILINE)

    
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
    slug = models.TextField(max_length=999, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def cover_image(self):
        return BlogMedia.objects.filter(post = self).first()

    @property
    def content_content(self):
        CLEANR = re.compile('<.*?>') # regex for cleaning html tags
        cleantext = re.sub(CLEANR, '', self.content)
        return cleantext.replace('#', '')
    
    def save(self, *args, **kwargs):
        self.content = convert_to_html(self.content)
        self.slug = self.title.replace(' ', '-').replace('/', '-').replace('--', '-')
        super(BlogPost, self).save(*args, **kwargs)


class BlogMedia(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blog_post_medias')
    image = models.ImageField(upload_to='Blog/Images/%Y-%m', default='')

    def __str__(self):
        return self.post.title


class Tag(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class BlogPostTopic(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name