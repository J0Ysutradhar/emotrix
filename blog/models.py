from django.db import models
import uuid

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default='EmoTrix')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
