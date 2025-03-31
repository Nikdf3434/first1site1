import matplotlib
matplotlib.use('Agg')
from django.http import HttpResponseRedirect, HttpResponse
from .models import NewUser, UserFile
from django.shortcuts import render, redirect
from .forms import UserFileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'home.html')

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
            messages.error(request, "Неверное имя пользователя или пароль")
            return render(request, 'login.html')
    return render(request, 'login.html')

def registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        usernames = NewUser.objects.values_list('username', flat=True)
        print(usernames)
        if username in usernames:
            messages.error(request, 'Пользователь с таким именем уже есть!')
            return render(request, 'registration.html')
        if password != password2:
            messages.error(request, "Пароли не совпадают. Попробуйте снова.")
            return render(request, 'registration.html')
        NewUser.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Ошибка при авторизации нового пользователя.")
            return render(request, 'registration.html')
    return render(request, 'registration.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def password_reset_(request):
    return render(request, 'password_reset.html')

def read_csv(file_path):
    df = pd.read_csv(file_path, sep=None, engine='python')
    first_row = df.iloc[0]
    if all(pd.to_numeric(first_row, errors='coerce').notnull()):
        df = df.iloc[1:].reset_index(drop=True)
    return df
 
def load_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UserFileForm(request.POST, request.FILES)
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        if UserFile.objects.filter(file__icontains=file_name, user=request.user).exists():
            messages.error(request, "Этот файл уже загружен!")
            return HttpResponseRedirect(request.path)
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

@login_required
def delete_file(request, file_id):
    file_obj = get_object_or_404(UserFile, id=file_id, user=request.user)
    file_obj.file.delete(save=False)
    file_obj.delete()
    messages.success(request, "Файл успешно удалён!")
    return redirect('load_file')

def file_id(request, file_id):
    return render(request, 'id_file.html', {'file_id': file_id})
     
def grafic(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path

    df = read_csv(file_path)
    count = len(df)
    if count < 20:
        count = 20
    x = request.GET.get('x')
    y_list = request.GET.getlist('y')
    x_data = df[x]

    plt.figure(figsize=(count//2, 6))
    for y in y_list:
        y_data = df[y]
        plt.plot(x_data, y_data, marker='o', label=y)
        for x_val, y_val in zip(x_data, y_data):
            plt.annotate(f'{y_val}', xy=(x_val, y_val),
                         textcoords="offset points", xytext=(0, 5),
                         ha='center', fontsize=8)
    plt.margins(x=0.001)
    plt.title('График данных из CSV', fontsize=16)
    plt.xlabel(x, fontsize=10)
    plt.ylabel('Значения', fontsize=10)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    download_format = request.GET.get('download', None)
    if download_format:
        buf = BytesIO()
        plt.savefig(buf, format=download_format, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        if download_format.lower() in ['jpg', 'jpeg']:
            content_type = 'image/jpeg'
        elif download_format.lower() == 'pdf':
            content_type = 'application/pdf'
        else:
            content_type = 'image/png'
        response = HttpResponse(buf.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename=grafic.{download_format}'
        buf.close()
        plt.close()
        return response

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render(request, 'grafic.html', {'file': file, 'image_base64': image_base64})

def pregrafic(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path
    df = read_csv(file_path)

    
    all_columns = df.columns.tolist()[1:]
    string_columns = [col for col in all_columns if pd.api.types.is_string_dtype(df[col])]
    numeric_columns = [col for col in all_columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if request.method == 'POST':
        selected_x = request.POST.get('x')
        selected_y = request.POST.getlist('y')

        u = f"x={selected_x}"
        for yzn in selected_y:
            u += f"&y={yzn}"
        return redirect(f"/add_file/{file_id}/pregrafic/grafic/?{u}")
    
    return render(request, 'pregrafic.html', {'string_columns': string_columns,
                                               'numeric_columns': numeric_columns,
                                               'file_id': file_id})

def prestolb_diagramm(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path
    df = read_csv(file_path)

    
    all_columns = df.columns.tolist()[1:]
    string_columns = [col for col in all_columns if pd.api.types.is_string_dtype(df[col])]
    numeric_columns = [col for col in all_columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if request.method == 'POST':
        selected_x = request.POST.get('x')
        selected_y = request.POST.get('y')
        
        return redirect(f"/add_file/{file_id}/prestolb_diagramm/stolb_diagramm/?x={selected_x}&y={selected_y}")
    
    return render(request, 'prestolb_diagramm.html', {'string_columns': string_columns,
                                                        'numeric_columns': numeric_columns,
                                                        'file_id': file_id})

def stolb_diagramm(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path

    df = read_csv(file_path)
    count = len(df)
    if count < 20:
        count = 20
    x = request.GET.get('x')
    y = request.GET.get('y')
    x_data = df[x]
    y_data = df[y]

    plt.margins(x=0.001)
    plt.figure(figsize=(count//2, 6))
    plt.bar(x_data, y_data, label=y, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', 'blue', 'red', 'green'])
    plt.title('Диаграмма из CSV-файла', fontsize=16)
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.xticks(rotation=60)
    for i in range(len(x_data)):
        plt.text(x_data[i], y_data[i] + 0.5, f'{y_data[i]}', ha='center')

    download_format = request.GET.get('download', None)
    if download_format:
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        if download_format.lower() in ['jpg', 'jpeg']:
            content_type = 'image/jpeg'
        elif download_format.lower() == 'pdf':
            content_type = 'application/pdf'
        else:
            content_type = 'image/png'
        response = HttpResponse(buf.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename=stolb_diagramm.{download_format}'
        buf.close()
        plt.close()
        return response

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render(request, 'stolb_diagramm.html', {'file': file, 'image_base64': image_base64})

def round_diagramm(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path

    df = read_csv(file_path)
    x = request.GET.get('x')
    y = request.GET.get('y')

    categories = df[x]
    values = df[y]

    count = len(df)
    if count < 16:
        count = 16
    if count > 128:
        count = 128
    plt.figure(figsize=(count//2, count//2))
    plt.pie(
        values,
        labels=categories,
        autopct='%.1f%%',
        startangle=90, 
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', 'blue', 'red', 'green']
    )
    plt.title('Круговая диаграмма')
    plt.xticks(rotation=60)

    download_format = request.GET.get('download', None)
    if download_format:
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        if download_format.lower() in ['jpg', 'jpeg']:
            content_type = 'image/jpeg'
        elif download_format.lower() == 'pdf':
            content_type = 'application/pdf'
        else:
            content_type = 'image/png'
        response = HttpResponse(buf.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename=round_diagramm.{download_format}'
        buf.close()
        plt.close()
        return response

    buf = BytesIO()                                      
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render(request, 'round_diagramm.html', {'file': file, 'image_base64': image_base64})

def preround_diagramm(request, file_id):
    file = UserFile.objects.get(id=file_id)
    file_path = file.file.path
    df = read_csv(file_path)
    
    all_columns = df.columns.tolist()[1:]
    string_columns = [col for col in all_columns if pd.api.types.is_string_dtype(df[col])]
    numeric_columns = [col for col in all_columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if request.method == 'POST':
        selected_x = request.POST.get('x')
        selected_y = request.POST.get('y') 
        
        return redirect(f"/add_file/{file_id}/preround_diagramm/round_diagramm/?x={selected_x}&y={selected_y}")
    
    return render(request, 'preround_diagramm.html', {'string_columns': string_columns,
                                                       'numeric_columns': numeric_columns,
                                                       'file_id': file_id})
                                                    