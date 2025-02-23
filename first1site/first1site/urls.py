from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', views.password_reset_, name='password_reset'),
    path('add_file/', views.load_file, name='load_file'),
    path('add_file/<int:file_id>', views.file_id, name='file_id'),
    path('add_file/<int:file_id>/pregrafic/grafic/', views.grafic, name='grafic'),
    path('add_file/<int:file_id>/pregrafic/', views.pregrafic, name='pregrafic'),
    path('add_file/<int:file_id>/prestolb_diagramm/stolb_diagramm/', views.stolb_diagramm, name='stolb_diagramm'),
    path('add_file/<int:file_id>/prestolb_diagramm/', views.prestolb_diagramm, name='prestolb_diagramm'),
    path('add_file/<int:file_id>/preround_diagramm/round_diagramm/', views.round_diagramm, name='round_diagramm'),
    path('add_file/<int:file_id>/preround_diagramm/', views.preround_diagramm, name='preround_diagramm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
