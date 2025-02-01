from django.http import HttpResponse, HttpResponseRedirect
from .models import Books, NewUser, UserFile
from django.shortcuts import render, redirect
from .forms import BookForm, UserFileForm
# from .forms import LoginForm
# from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def home(request):
    return render(request, 'home.html')

# def books(request):
#     # return HttpResponse('Page with books')
#     query = request.GET.get('q')
#     if query: 
#         all_books = Books.objects.filter(title__icontains = query)
#     else:
#         all_books = Books.objects.all()
#         print(all_books)
#     return render(request, 'list_of_books.html', {'all_books': all_books})


# def book_id(request, book_id):
#     book = Books.objects.get(id=book_id)
#     return render(request, 'site_book_info.html', {'book': book})

# @login_required
# def add_book(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return HttpResponseRedirect(request.path)
#     else:
#         form = BookForm()
#     return render(request, 'book_form.html', {'form': form})

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
    all_files = UserFile.objects.filter(user=request.user)
    return render(request, 'file_form.html', {'file_form': form, 'all_files': all_files})

def file_id(request, file_id):
    return render(request, 'id_file.html', {'file_id': file_id})
     
def grafic(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path
    
    df = pd.read_csv(file_path)
    df=df.head(5)
    x = request.GET.get('x')
    y = request.GET.get('y')
    x_data = df[x]
    y_data = df[y]

    plt.figure(figsize=(10, 6))
    plt.plot(x_data, y_data, label=y)
    plt.title('График данных из CSV', fontsize=16)
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.legend()
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
        


    return render(request, 'grafic.html', {'file': file, 'image_base64': image_base64})

def pregrafic_and_prediagramm(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path
    df = pd.read_csv(file_path)
    columns = df.columns.tolist()[1:]
    if request.method == 'POST':
        selected_x = request.POST.get('x')
        # selected_y = request.POST.get('y') 
        selected_y = request.POST.getlist('y')
        
        return redirect(f"/add_file/{file_id}/pregrafic_and_prediagramm/grafic/?x={selected_x}&y={selected_y}")
    return render(request, 'pregrafic_and_prediagramm.html', {'columns': columns, 'file_id': file_id})

def diagramm(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path
    
    df = pd.read_csv(file_path)
    df=df.head(5)
    x = request.GET.get('x')
    y = request.GET.get('y')
    x_data = df[x]
    y_data = df[y]

    plt.figure(figsize=(10, 6))
    plt.bar(x_data, y_data, label=y, color='blue')
    plt.title('Диаграмма из CSV-файла', fontsize=16)
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.show()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render(request, 'diagramm.html', {'file': file, 'image_base64': image_base64})