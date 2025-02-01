"""
URL configuration for first1site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('books/', views.books, name='books'),
    # path('books/<int:book_id>', views.book_id, name='book_id'),
    # path('books/add_book', views.add_book, name='add_book'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', views.password_reset_, name='password_reset'),
    path('add_file/', views.load_file, name='load_file'),
    path('add_file/<int:file_id>', views.file_id, name='file_id'),
    path('add_file/<int:file_id>/pregrafic_and_prediagramm/grafic/', views.grafic, name='grafic'),
    path('add_file/<int:file_id>/pregrafic_and_prediagramm/', views.pregrafic_and_prediagramm, name='pregrafic_and_prediagramm'),
    path('add_file/<int:file_id>/pregrafic_and_prediagramm/diagramm/', views.diagramm, name='diagramm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)