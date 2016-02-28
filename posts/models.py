from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.CharField(max_length=4000)
    slug = models.SlugField(max_length=40)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    show = models.BooleanField(default=True)

    # this is a custom save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.updated_at = timezone.now()
        if not self.id:
            self.created_at = timezone.now()
        super(Post, self).save(*args, **kwargs)