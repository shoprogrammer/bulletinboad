from django.db import models
from django.contrib.auth.models import User

class BoardModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='boards',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(User,related_name='favorite_boards',through='Favorite')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','board')


class Contact(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)