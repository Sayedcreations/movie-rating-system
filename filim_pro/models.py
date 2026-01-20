from django.db import models
from django.utils.timezone import now

# Create your models here.
class registration(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    firstname = models.CharField(max_length=100, default='null', null=False)
    lastname = models.CharField(max_length=100, default='null', null=False)
    email = models.CharField(max_length=255, default='null', null=False)
    password = models.CharField(max_length=500, default='null', null=False)
    phone = models.CharField(max_length=15, default='null', null=False)
    profile_photo = models.ImageField(upload_to='FILM_PRO/', blank=True, null=True)
    state = models.CharField(max_length=10,default='null', null=False )
    status_choices = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="pending")
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.email

class people(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    firstname = models.CharField(max_length=255, default='null', null=False)
    lastname = models.CharField(max_length=255, default='null', null=False)
    date_of_birth = models.CharField(max_length=100, default='null', null=False)
    country = models.CharField(max_length=100, default='null', null=False)
    biography = models.CharField(max_length=20000, default='null', null=False)
    cast_crew = models.CharField(max_length=100, default='null', null=False)
    position = models.CharField(max_length=500, default='null', null=False)
    photo = models.ImageField(upload_to='FILM_PEOPLE/', blank=True, null=True)
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.firstname

class people_photo(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    people = models.ForeignKey(people,on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='FILM_PRO/', blank=True, null=True)
    date_added = models.DateTimeField(default=now, editable=False)

class movie(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    title = models.CharField(max_length=255, default='null', null=False)
    photo = models.ImageField(upload_to='FILM_MOVIE/', blank=True, null=True)
    country = models.CharField(max_length=100, default='null', null=False)
    overview = models.CharField(max_length=20000, default='null', null=False)
    release_date = models.DateTimeField(max_length=100, null=False)
    running_time = models.CharField(max_length=100, default='null', null=False)
    certificate = models.CharField(max_length=100, default='null', null=False)
    trailer_link = models.CharField(max_length=100, default='null', null=True)
    genere = models.CharField(max_length=100, default='null', null=False)
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.title

class movie_photo(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    movie = models.ForeignKey(movie,on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='FILM_PRO/', blank=True, null=True)
    date_added = models.DateTimeField(default=now, editable=False)

class movie_cast_crew(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    status_choices = [
        ('cast', 'Cast'),
        ('crew', 'Crew'),
    ]
    type = models.CharField(max_length=15, choices=status_choices, default="cast")
    movie = models.ForeignKey(movie,on_delete=models.CASCADE)
    people = models.ForeignKey(people,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='null', null=True)
    date_added = models.DateTimeField(default=now, editable=False)
