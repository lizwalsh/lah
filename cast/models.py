from django.db import models


# Create your models here.
class Intro(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    picture = models.ImageField(upload_to='images/cast/', blank=True)
    
class CastEntry(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(max_length=20, choices=[('humans', 'humans'), ('werewolves', 'werewolves'), ('hunters', 'hunters'), ('sorcerors', 'sorcerors')])
    picture = models.ImageField(upload_to='images/cast/', blank=True)
    
    class Meta:
        verbose_name_plural = 'Cast entries'
    
    def __str__(self):
        return "Cast member: " + str(self.title)
