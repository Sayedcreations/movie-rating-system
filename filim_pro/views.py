from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from filim_user.models import movie_rating as film_user__movie_rating
from django.db.models import Avg, Count
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def login(request):
    if request.method == 'POST':
            data_record = request.POST
            if registration.objects.filter(phone=data_record['mobile_number'],password=data_record['password']):
                user_details = registration.objects.get(phone=data_record['mobile_number'],password=data_record['password'])
                if user_details.status == 'active':
                    request.session['is_logged_in'] = True
                    request.session['email'] = user_details.email
                    request.session['firstname'] = user_details.firstname
                    request.session['lastname'] = user_details.lastname
                    request.session['user_id'] = user_details.unique_id
                    request.session['mobile_number'] = user_details.phone
                    request.session['usertype'] = 'pro'
                    return redirect(reverse('film_pro:dashboard'))
                else:
                    messages.error(request, 'User not approved. Contact the admin!')
                    return redirect(reverse('film_pro:login'))
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect(reverse('film_pro:login'))
    return render(request, 'film_pro/login.html')

def signup(request):
    if request.method == 'POST':
        data_record = request.POST
        if registration.objects.filter(email=data_record['email_address']):
            messages.error(request, 'Email already exists! Please try again!')
            return redirect(reverse('film_pro:signup'))
        elif registration.objects.filter(phone=data_record['mobile_number']):
            messages.error(request, 'Mobile number already exists! Please try again!')
            return redirect(reverse('film_pro:signup'))
        else:
            signup = registration(
            firstname=data_record['firstname'],
            lastname=data_record['lastname'],
            email=data_record['email_address'],
            phone=data_record['mobile_number'],
            state=data_record['state'],
            password=data_record['password'],
            status='pending',
            )
            signup.save()
            messages.success(request, 'User registered successfully!')
            return redirect(reverse('film_pro:login'))
    context = {}
    return render(request, 'film_pro/signup.html', context)

def logout(request):
    del request.session['is_logged_in']
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['user_id']
    del request.session['mobile_number']
    del request.session['usertype']
    return redirect(reverse('film_pro:login'))

def dashboard(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    context = { 'userdata': userdata }
    return render(request, 'film_pro/dashboard.html', context)

def edit_profile(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    if request.method == 'POST':
        data_record = request.POST
        userdata.firstname = data_record['firstname']
        userdata.lastname = data_record['lastname']
        userdata.phone = data_record['mobile_number']
        userdata.email = data_record['email_address']
        userdata.state = data_record['state']
        userdata.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect(reverse('film_pro:edit_profile'))
    context = { 'userdata':userdata }
    return render(request, 'film_pro/edit-profile.html', context)

def edit_password(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    if request.method == 'POST':
        data_record = request.POST
        if userdata.password == data_record['old_password']:
            userdata.password = data_record['password']
            userdata.save()
            messages.success(request, 'Password updated successfully!')
        else:
            messages.error(request, 'Please enter correct previous password!')
    return redirect(reverse('film_pro:edit_profile'))

def edit_avatar(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    if request.method == 'POST':
        uploaded_file = request.FILES['change_avatar']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_PRO_"+uploaded_file.name, uploaded_file)
        userdata.profile_photo = fs.url(file_name)
        userdata.save()
        messages.success(request, 'Avatar changed successfully!')
    return redirect(reverse('film_pro:edit_profile'))

def add_people(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    if request.method == 'POST':
        data_record = request.POST
        position = data_record.getlist('position')
        print(",".join(position))
        uploaded_file = request.FILES['celeb_photo']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_PEOPLE_"+uploaded_file.name, uploaded_file)
        add_people = people(
        firstname = data_record['firstname'],
        lastname = data_record['lastname'],
        date_of_birth = data_record['date_of_birth'],
        country = data_record['country'],
        biography=data_record['biography'],
        cast_crew=data_record['cast_crew'],
        position=",".join(position),
        photo=fs.url(file_name),
        )
        add_people.save()
        messages.success(request, 'People added successfully!')
        return redirect(reverse('film_pro:add_people'))
    context = { 'userdata':'' }
    return render(request, 'film_pro/add-people.html', context)

def list_people(request, query = ''):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    data_list = people.objects.all()
    if query != '':
        data_list = people.objects.filter(firstname__icontains=query) | people.objects.filter(lastname__icontains=query)
    if request.method == 'POST':
        data_record = request.POST
        celebrity_letter = data_record.get('celebrity_letter', '')
        celebrity_name = data_record['celebrity_name']
        if celebrity_letter == '':
            data_list = people.objects.filter(firstname__icontains=celebrity_name) | people.objects.filter(lastname__icontains=celebrity_name)
        elif celebrity_name == '':
            data_list = people.objects.filter(firstname__icontains=celebrity_letter) | people.objects.filter(lastname__icontains=celebrity_letter)
        else:
            data_list = people.objects.filter(firstname__icontains=celebrity_name) | people.objects.filter(lastname__icontains=celebrity_name) | people.objects.filter(firstname__icontains=celebrity_letter) | people.objects.filter(lastname__icontains=celebrity_letter)
    context = { 'data_list': data_list.all(), 'query':query }
    return render(request, 'film_pro/list-people.html', context)

def view_people(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = people.objects.get(unique_id=id)
    userdata_photos = people_photo.objects.filter(people_id=id)
    userdata_filmography = movie_cast_crew.objects.filter(people_id=id)
    context = { 'userdata': userdata, 'userdata_photos':userdata_photos, 'userdata_filmography':userdata_filmography }
    return render(request, 'film_pro/view-people.html', context)

def edit_people(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = people.objects.get(unique_id=id)
    if request.method == 'POST':
            data_record = request.POST
            position = data_record.getlist('position')
            userdata.firstname = data_record['firstname']
            userdata.lastname = data_record['lastname']
            userdata.date_of_birth = data_record['date_of_birth']
            userdata.country = data_record['country']
            userdata.biography = data_record['biography']
            userdata.position = ",".join(position)
            userdata.cast_crew = data_record['cast_crew']
            userdata.save()
            messages.success(request, 'Record updated successfully!')
            return redirect(reverse('film_pro:view_people', args=[id] ))
    context = { 'userdata': userdata }
    return render(request, 'film_pro/edit-people.html', context)

def edit_people_avatar(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = people.objects.get(unique_id=id)
    if request.method == 'POST':
        uploaded_file = request.FILES['change_avatar']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_PEOPLE_"+uploaded_file.name, uploaded_file)
        userdata.photo = fs.url(file_name)
        userdata.save()
        messages.success(request, 'Avatar changed successfully!')
    return redirect(reverse('film_pro:view_people', args=[id]))

def add_people_photo(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    if request.method == 'POST':
        uploaded_file = request.FILES['add_photo']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_PEOPLE_PHOTOS_"+uploaded_file.name, uploaded_file)
        add_people_photo = people_photo(
        photos=fs.url(file_name),
        people=people.objects.get(unique_id=id),
        )
        add_people_photo.save()
    messages.success(request, 'Photo added successfully!')
    return redirect(reverse('film_pro:view_people', args=[id]))

def add_movie(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    if request.method == 'POST':
        data_record = request.POST
        genere = data_record.getlist('genre')
        uploaded_file = request.FILES['title_photo']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_MOVIE_"+uploaded_file.name, uploaded_file)
        add_movie = movie(
        title = data_record['title'],
        photo=fs.url(file_name),
        overview=data_record['overview'],
        release_date = data_record['release_date'],
        running_time = data_record['running_time'],
        country = data_record['country'],
        certificate=data_record['certificate'],
        trailer_link=data_record['trailer_link'],
        genere=",".join(genere),
        )
        add_movie.save()
        messages.success(request, 'Movie added successfully!')
        return redirect(reverse('film_pro:add_movie'))
    context = { 'userdata':'' }
    return render(request, 'film_pro/add-movie.html', context)

def list_movie(request, query = ''):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    data_list = movie.objects.all()
    if query != '':
        data_list = movie.objects.filter(title__icontains=query).all()
    if request.method == 'POST':
        data_record = request.POST
        genre=data_record.get('genre', '')
        movie_name=data_record['movie_name']
        if movie_name == '':
            data_list = movie.objects.filter(genere__icontains=genre).all()
        elif genre == '':
            data_list = movie.objects.filter(title__icontains=movie_name).all()
        else:
            data_list = movie.objects.filter(title__icontains=movie_name,genere__icontains=genre).all()
    rating = film_user__movie_rating.objects.values('movie_id').annotate(rating_value=Avg('rating_scale', distinct=True))
    context = { 'data_list': data_list, 'rating': rating, 'query':query }
    return render(request, 'film_pro/list-movie.html', context)

def view_movie(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    director = []
    writer = []
    userdata = movie.objects.get(unique_id=id)
    userdata_photos = movie_photo.objects.filter(movie_id=id)
    userdata_cast = movie_cast_crew.objects.filter(type="cast",movie_id=id)
    userdata_crew = movie_cast_crew.objects.filter(type="crew",movie_id=id)
    userdata_reviews = film_user__movie_rating.objects.filter(movie_id=id)
    rating_val = film_user__movie_rating.objects.filter(movie_id=id).values('movie_id').annotate(rating_value=Avg('rating_scale', distinct=True),rating_count=Count('rating_scale'))
    for row in userdata_crew:
        position = row.people.position
        if position.find('director') != -1:
            director.append({ 'unique_id': row.people.unique_id, 'firstname': row.people.firstname, 'lastname': row.people.lastname })
        if position.find('writer') != -1:
            writer.append({ 'unique_id': row.people.unique_id, 'firstname': row.people.firstname, 'lastname': row.people.lastname })
    context = { 'userdata': userdata, 'userdata_photos':userdata_photos, 'userdata_cast':userdata_cast,'userdata_crew':userdata_crew, 'userdata_rating':rating_val, 'userdata_reviews':userdata_reviews, 'record_id':id , 'director': director, 'writer': writer }
    return render(request, 'film_pro/view-movie.html', context)

def edit_movie(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = movie.objects.get(unique_id=id)
    if request.method == 'POST':
            data_record = request.POST
            genere = data_record.getlist('genre')
            userdata.title = data_record['title']
            userdata.overview = data_record['overview']
            userdata.release_date = data_record['release_date']
            userdata.running_time = data_record['running_time']
            userdata.country = data_record['country']
            userdata.certificate = data_record['certificate']
            userdata.trailer_link = data_record['trailer_link']
            userdata.genere = ",".join(genere)
            userdata.save()
            messages.success(request, 'Record updated successfully!')
            return redirect(reverse('film_pro:view_movie', args=[id] ))
    context = { 'userdata': userdata }
    return render(request, 'film_pro/edit-movie.html', context)

def edit_movie_avatar(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = movie.objects.get(unique_id=id)
    if request.method == 'POST':
        uploaded_file = request.FILES['change_avatar']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_MOVIE_"+uploaded_file.name, uploaded_file)
        userdata.photo = fs.url(file_name)
        userdata.save()
        messages.success(request, 'Photo changed successfully!')
    return redirect(reverse('film_pro:view_movie', args=[id]))

def add_movie_photo(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    if request.method == 'POST':
        uploaded_file = request.FILES['add_photo']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_MOVIE_PHOTOS_"+uploaded_file.name, uploaded_file)
        add_movie_photo = movie_photo(
        photos=fs.url(file_name),
        movie=movie.objects.get(unique_id=id),
        )
        add_movie_photo.save()
    messages.success(request, 'Photo added successfully!')
    return redirect(reverse('film_pro:view_movie', args=[id]))

def edit_movie_cast(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = people.objects.filter(cast_crew='cast').all()
    if request.method == 'POST':
        data_record = request.POST
        check_exists = movie_cast_crew.objects.filter(type="cast",movie_id=id,people_id=data_record['cast'])
        if check_exists:
           messages.error(request, 'Already added! Try another!')
           return redirect(reverse('film_pro:edit_movie_cast', args=[id]))
        else:
           cast = movie_cast_crew(
           type="cast",
           title=data_record['title'],
           movie=movie.objects.get(unique_id=id),
           people=people.objects.get(unique_id=data_record['cast'])
           )
           cast.save()
           messages.success(request, 'Cast added successfully!')
    context = { 'userdata': userdata }
    return render(request, 'film_pro/edit-movie-cast.html', context)

def edit_movie_crew(request, id):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    userdata = people.objects.filter(cast_crew='crew').all()
    if request.method == 'POST':
        data_record = request.POST
        check_exists = movie_cast_crew.objects.filter(type="crew",movie_id=id,people_id=data_record['crew'])
        if check_exists:
           messages.error(request, 'Already added! Try another!')
           return redirect(reverse('film_pro:edit_movie_crew', args=[id]))
        else:
           crew = movie_cast_crew(
           type="crew",
           movie=movie.objects.get(unique_id=id),
           people=people.objects.get(unique_id=data_record['crew'])
           )
           crew.save()
           messages.success(request, 'Crew added successfully!')
    context = { 'userdata': userdata }
    return render(request, 'film_pro/edit-movie-crew.html', context)

def search_movie(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'pro'):
        return redirect(reverse('film_pro:login'))
    if request.method == 'POST':
        data_record = request.POST
        if data_record['search_value'] != '':
            if data_record['search_item'] == "movie":
                return redirect(reverse('film_pro:list_movie', args=[data_record['search_value']]))
            else:
                return redirect(reverse('film_pro:list_people', args=[data_record['search_value']]))

def delete_people(request, id):
    people.objects.get(unique_id=id).delete()
    return redirect(reverse('film_pro:list_people'))

def delete_movie(request, id):
    movie.objects.get(unique_id=id).delete()
    return redirect(reverse('film_pro:list_movie'))
