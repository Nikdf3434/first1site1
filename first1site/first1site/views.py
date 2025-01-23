from django.http import HttpResponse, HttpResponseRedirect
from .models import Books, NewUser, UserFile
from django.shortcuts import render, redirect
from .forms import BookForm, UserFileForm
# from .forms import LoginForm
# from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    
    # for i in all_books:
    #     print(i.id, i.title, i.prace)

    # new_book = Books(title="Тест2", author="Н.Гоголь", publishing="Moscow", pages="600", prace="25")
    # new_book.save()

    # filtred_book = Books.objects.filter(publishing = 'Санкт-Петербург')
    # print(filtred_book)

    # book_to_change = Books.objects.get(id=17)
    # print(book_to_change)
    # book_to_change.title = 'Мёртвые души (18...)'
    # book_to_change.save()
    
    # Books.objects.get(id=15).delete()
    # return HttpResponse('Hello world')
    return render(request, 'home.html')

def books(request):
    # return HttpResponse('Page with books')
    query = request.GET.get('q')
    if query: 
        all_books = Books.objects.filter(title__icontains = query)
    else:
        all_books = Books.objects.all()
        print(all_books)
    return render(request, 'list_of_books.html', {'all_books': all_books})


def book_id(request, book_id):
    book = Books.objects.get(id=book_id)
    return render(request, 'site_book_info.html', {'book': book})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.path)
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            NewUser.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/') 
            else:
                return render(request, 'registration.html')
    return render(request, 'registration.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def password_reset_(request):
    return render(request, 'password_reset.html')

def load_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            userfile = form.save(commit=False)
            userfile.user = request.user
            userfile.save()
            messages.success(request, "Форма успешно отправлена!")
        elif not form.is_valid():
            print(form.errors)
            messages.error(request, "Разрешены только CSV файлы!")
        return HttpResponseRedirect(request.path)
    else:
        form = UserFileForm()
    all_files = UserFile.objects.all()
    # print(all_files)
    return render(request, 'file_form.html', {'file_form': form, 'all_files': all_files})



def file_id(request, file_id):
    file = UserFile.objects.get(id=file_id)
    return render(request, 'id_file.html', {'file': file})