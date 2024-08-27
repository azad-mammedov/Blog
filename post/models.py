from django.db import models

from users.models import CustomUser

class Post(models.Model):
    title = models.CharField(max_length=200 , unique=True)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    


