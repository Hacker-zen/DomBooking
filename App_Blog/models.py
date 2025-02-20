from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from App_Auth.models import CustomerProfile
# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='post_author')
    blog_title = models.CharField(max_length=264, verbose_name="Put a Title")
    slug = models.SlugField(max_length=264, unique=True)
    blog_content = RichTextField(blank=True, null=True)
    blog_image = models.ImageField(upload_to='blog_image', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date',]

    def __str__(self):
        return self.blog_title
    
    def get_blog_image_url(self):
        # Ensure the image URL is always a string
        if self.blog_image:
            return str(self.blog_image.url)
        return ""


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date',]


    def __str__(self):
        return self.comment


class Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='liked_blog')
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='liked_user')

    def __str__(self):
        return self.user , " likes " , self.blog
    

    