from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from filim_pro.models import *
from .models import *
from django.db.models import Avg, Count
from django.core.files.storage import FileSystemStorage

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
                    request.session['usertype'] = 'user'
                    return redirect(reverse('film_user:dashboard'))
                else:
                    messages.error(request, 'User is suspended. Contact the admin!')
                    return redirect(reverse('film_user:login'))
            else:
                messages.error(request, 'Invalid credentials!')
                return redirect(reverse('film_user:login'))
    return render(request, 'film_user/login.html')

def signup(request):
    if request.method == 'POST':
        data_record = request.POST
        if registration.objects.filter(email=data_record['email_address']):
            messages.error(request, 'Email already exists! Please try again!')
            return redirect(reverse('film_user:signup'))
        elif registration.objects.filter(phone=data_record['mobile_number']):
            messages.error(request, 'Mobile number already exists! Please try again!')
            return redirect(reverse('film_user:signup'))
        else:
            signup = registration(
            firstname=data_record['firstname'],
            lastname=data_record['lastname'],
            email=data_record['email_address'],
            phone=data_record['mobile_number'],
            state=data_record['state'],
            password=data_record['password'],
            status='active',
            )
            signup.save()
            messages.success(request, 'User registered successfully!')
            return redirect(reverse('film_user:login'))
    context = {}
    return render(request, 'film_user/signup.html', context)

def logout(request):
    del request.session['is_logged_in']
    del request.session['firstname']
    del request.session['lastname']
    del request.session['email']
    del request.session['user_id']
    del request.session['mobile_number']
    del request.session['usertype']
    return redirect(reverse('film_user:login'))

def dashboard(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'user'):
        return redirect(reverse('film_user:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    context = { 'userdata': userdata }
    return render(request, 'film_user/dashboard.html', context)

def edit_profile(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'user'):
        return redirect(reverse('film_user:login'))
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
        return redirect(reverse('film_user:edit_profile'))
    context = { 'userdata':userdata }
    return render(request, 'film_user/edit-profile.html', context)

def edit_password(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'user'):
        return redirect(reverse('film_user:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    if request.method == 'POST':
        data_record = request.POST
        if userdata.password == data_record['old_password']:
            userdata.password = data_record['password']
            userdata.save()
            messages.success(request, 'Password updated successfully!')
        else:
            messages.error(request, 'Please enter correct previous password!')
    return redirect(reverse('film_user:edit_profile'))

def edit_avatar(request):
    if not (request.session.get('is_logged_in') and request.session['usertype'] == 'user'):
        return redirect(reverse('film_user:login'))
    userdata = registration.objects.get(unique_id=request.session['user_id'])
    if request.method == 'POST':
        uploaded_file = request.FILES['change_avatar']
        fs = FileSystemStorage()
        file_name = fs.save("FILM_USER_"+uploaded_file.name, uploaded_file)
        userdata.profile_photo = fs.url(file_name)
        userdata.save()
        messages.success(request, 'Avatar changed successfully!')
    return redirect(reverse('film_user:edit_profile'))

def list_people(request, query = ''):
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
    return render(request, 'film_user/list-people.html', context)

def view_people(request, id):
    userdata = people.objects.get(unique_id=id)
    userdata_photos = people_photo.objects.filter(people_id=id)
    userdata_filmography = movie_cast_crew.objects.filter(people_id=id)
    context = { 'userdata': userdata, 'userdata_photos':userdata_photos, 'userdata_filmography':userdata_filmography }
    return render(request, 'film_user/view-people.html', context)

def list_movie(request, query = ''):
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
    rating = movie_rating.objects.values('movie_id').annotate(rating_value=Avg('rating_scale', distinct=True))
    context = { 'data_list': data_list, 'rating': rating, 'query':query }
    return render(request, 'film_user/list-movie.html', context)

def view_movie(request, id):
    director = []
    writer = []
    if request.method == 'POST':
        data_record = request.POST
        record = movie_rating(
            user_id=request.session['user_id'],
            movie_id=id,
            review_title=data_record['title'],
            review=data_record['review'],
            rating_scale=data_record['rating'],
            )
        record.save()
        messages.success(request, 'Review added successfully!')
        return redirect(reverse('film_user:view_movie', args=[id]))

    userdata = movie.objects.get(unique_id=id)
    userdata_photos = movie_photo.objects.filter(movie_id=id)
    userdata_cast = movie_cast_crew.objects.filter(type="cast",movie_id=id)
    userdata_crew = movie_cast_crew.objects.filter(type="crew",movie_id=id)
    userdata_reviews = movie_rating.objects.filter(movie_id=id)
    rating_val = movie_rating.objects.filter(movie_id=id).values('movie_id').annotate(rating_value=Avg('rating_scale', distinct=True),rating_count=Count('rating_scale'))
    for row in userdata_crew:
        position = row.people.position
        if position.find('director') != -1:
            director.append({ 'unique_id': row.people.unique_id, 'firstname': row.people.firstname, 'lastname': row.people.lastname })
        if position.find('writer') != -1:
            writer.append({ 'unique_id': row.people.unique_id, 'firstname': row.people.firstname, 'lastname': row.people.lastname })
    context = { 'userdata': userdata, 'userdata_photos':userdata_photos, 'userdata_cast':userdata_cast,'userdata_crew':userdata_crew, 'userdata_rating':rating_val, 'userdata_reviews':userdata_reviews, 'record_id':id , 'director': director, 'writer': writer  }
    return render(request, 'film_user/view-movie.html', context)

def search_movie(request):
    if request.method == 'POST':
        data_record = request.POST
        if data_record['search_value'] != '':
            if data_record['search_item'] == "movie":
                return redirect(reverse('film_user:list_movie', args=[data_record['search_value']]))
            else:
                return redirect(reverse('film_user:list_people', args=[data_record['search_value']]))

def view_movie_write_review(request):
    context = { 'userdata': '' }
    return render(request, 'film_user/view-movie.html', context)

def view_movie_buy_ticket(request, id):
    if not ( request.session.get('is_logged_in', None) == True and request.session.get('usertype', None) == "user"):
       messages.success(request, 'You must log in to buy a ticket.')
       return redirect(reverse('film_user:login'))
    userdata = movie.objects.get(unique_id=id)
    context = { 'userdata': userdata, 'record_id': id }
    return render(request, 'film_user/buy-ticket.html', context)
