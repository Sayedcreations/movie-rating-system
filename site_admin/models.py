from django.db import models
from django.utils.timezone import now

# Create your models here.
class screens(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    screen_name = models.CharField(max_length=255, default='null', null=False)
    building_name = models.CharField(max_length=255, default='null', null=False)
    location = models.CharField(max_length=100, default='null', null=False)
    address = models.CharField(max_length=500, default='null', null=False)
    city = models.CharField(max_length=100, default='null', null=False)
    state = models.CharField(max_length=20000, default='null', null=False)
    photo = models.ImageField(upload_to='FILM_PEOPLE/', blank=True, null=True)
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.screen_name
