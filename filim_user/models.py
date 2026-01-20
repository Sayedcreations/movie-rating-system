from django.db import models
from filim_pro import models as filim_pro_models
from django.utils.timezone import now


# Create your models here.
class registration(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    firstname = models.CharField(max_length=100, default='null', null=False)
    lastname = models.CharField(max_length=100, default='null', null=False)
    email = models.CharField(max_length=255, default='null', null=False)
    password = models.CharField(max_length=500, default='null', null=False)
    phone = models.CharField(max_length=15, default='null', null=False)
    profile_photo = models.ImageField(upload_to='FILM_USER/', blank=True, null=True)
    state = models.CharField(max_length=10,default='null', null=False )
    status_choices = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="active")
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.email

class movie_rating(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(registration,on_delete=models.CASCADE)
    movie = models.ForeignKey(filim_pro_models.movie,on_delete=models.CASCADE)
    rating_scale = models.FloatField(max_length=10, default=0, null=False)
    review_title = models.CharField(max_length=500, default='null', null=False)
    review = models.CharField(max_length=20000, default='null', null=False)
    date_added = models.DateTimeField(default=now, editable=False)
