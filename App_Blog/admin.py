from django.contrib import admin

# Register your models here.

from App_Blog import models

class BlogAdmin(admin.ModelAdmin):
    list_display = ['blog_title', 'publish_date', 'update_date']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.blog_image:
            obj.blog_image = str(obj.blog_image)  # Ensure blog_image is a string
        return form

admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Likes)

