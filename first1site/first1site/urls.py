from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('add_file/', views.load_file, name='load_file'),
    path('add_file/<int:file_id>', views.file_id, name='file_id'),
    path('add_file/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('add_file/<int:file_id>/pregrafic/grafic/', views.grafic, name='grafic'),
    path('add_file/<int:file_id>/pregrafic/', views.pregrafic, name='pregrafic'),
    path('add_file/<int:file_id>/prestolb_diagramm/stolb_diagramm/', views.stolb_diagramm, name='stolb_diagramm'),
    path('add_file/<int:file_id>/prestolb_diagramm/', views.prestolb_diagramm, name='prestolb_diagramm'),
    path('add_file/<int:file_id>/preround_diagramm/round_diagramm/', views.round_diagramm, name='round_diagramm'),
    path('add_file/<int:file_id>/preround_diagramm/', views.preround_diagramm, name='preround_diagramm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

