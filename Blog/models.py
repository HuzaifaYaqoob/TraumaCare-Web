from django.db import models

# Create your models here.

from PIL import Image
from django.conf import settings
from datetime import datetime

import re
import uuid
import time
import random
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
    gpt_content = models.TextField(default='')
    content = models.TextField()
    read_time = models.PositiveIntegerField(default=0)
    slug = models.TextField(max_length=999, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def cover_image(self):
        medias = BlogMedia.objects.filter(post = self).order_by('?')
        if len(medias) == 0:
            return None
        # random.shuffle(list(medias))
        return medias[0]


    @property
    def content_content(self):
        CLEANR = re.compile('<.*?>') # regex for cleaning html tags
        cleantext = re.sub(CLEANR, '', self.content)
        return cleantext.replace('#', '')
    
    @property
    def blog_tags_string(self):
        tags = self.tags.all()
        return ', '.join([tag.name for tag in tags])
    
    def save(self, *args, **kwargs):
        self.content = convert_to_html(self.gpt_content or self.content)
        self.slug = self.title.replace(' ', '-').replace('/', '-').replace("'", '').replace('"', '').replace(':', '-').replace('--', '-')
        super(BlogPost, self).save(*args, **kwargs)


class BlogMedia(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blog_post_medias')
    image = models.FileField(upload_to='Blog/Images/%Y-%m', default='')
    thumbnail = models.ImageField(upload_to='Blog/Images/%Y-%m', default='')
    mini_thumbnail = models.ImageField(upload_to='Blog/Images/%Y-%m', default='')
    is_thumbnail_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.post.title
    
    def save(self, *args, **kwargs):
        if not self.is_thumbnail_generated:

            # Assuming `self.image` is the background image path

            # background = Image.open(f'{settings.BASE_DIR}{self.image.url}')
            ext = self.image.name.split('.')[-1]
            background = Image.open(self.image)
            bg_w, bg_h = background.size

            # Calculate the size of the foreground image based on the background
            cfg_w, cfg_h = bg_w // 2, bg_h // 2

            foreground_path = f'{settings.BASE_DIR}/Files/tc_watermark.png'
            foreground = Image.open(foreground_path).convert("RGBA")

            # Calculate aspect ratio
            aspect_ratio = foreground.width / foreground.height

            # Calculate new width and height while maintaining aspect ratio
            new_width = cfg_w
            new_height = int(new_width / aspect_ratio)

            # Resize the foreground image
            foreground = foreground.resize((new_width, new_height), Image.ANTIALIAS)
            fg_w, fg_h = foreground.size

            # Calculate position to paste the foreground image at the center of the background
            x, y = ((bg_w - fg_w) // 2, (bg_h - fg_h) // 2)

            # Adjust alpha channel if it exists
            bands = list(foreground.split())
            if len(bands) == 4:
                # Assuming alpha is the last band
                bands[3] = bands[3].point(lambda x: x * 0.6)
                foreground = Image.merge(foreground.mode, bands)

            # Paste the foreground image onto the background
            background.paste(foreground, (x, y), foreground)

            # Save the resulting image
            time.sleep(1)
            time_now = datetime.now().strftime("%d-%H%M%S")
            
            slug = self.post.slug
            saving_url = f"media/Blog/Images/traumacare-{slug[0:34]}-{time_now}-{bg_w}x{bg_h}.{ext}"

            background.save(saving_url, quality=70)
            self.image = f'{saving_url}'.split('media/')[-1]

            new_width = 400
            if bg_w > new_width:
                bg_h = int((new_width / bg_w) * bg_h)
                bg_w = new_width

                tmb_bg = background.resize((bg_w, bg_h), Image.ANTIALIAS)
            else:
                tmb_bg = background

            saving_url = f"media/Blog/Images/traumacare-{slug[0:30]}-{time_now}-{bg_w}x{bg_h}.{ext}"
            tmb_bg.save(saving_url, quality=95)
            self.thumbnail = f'{saving_url}'.split('media/')[-1]

            new_width = 200
            if bg_w > new_width:
                bg_h = int((new_width / bg_w) * bg_h)
                bg_w = new_width

                background = background.resize((bg_w, bg_h), Image.ANTIALIAS)

            saving_url = f"media/Blog/Images/traumacare-{slug[0:30]}-{time_now}-{bg_w}x{bg_h}.{ext}"
            background.save(saving_url, quality=95)
            self.mini_thumbnail = f'{saving_url}'.split('media/')[-1]

            self.is_thumbnail_generated = True
        
        super(BlogMedia, self).save(*args, **kwargs)


class Tag(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class BlogPostTopic(models.Model):
    name = models.TextField(default='')

    def __str__(self):
        return self.name



# class VideoTopic(models.Model):
#     name = models.TextField(default='')

#     def __str__(self):
#         return self.name