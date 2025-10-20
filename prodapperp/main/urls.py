
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'dziennik', views.DziennikZdarzenRCPViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/user/', views.user_view, name='user'),
    path('api/status/<int:user_id>/', views.status_view, name='status'),
    path('api/zlecenia/', views.zlecenia_view, name='zlecenia'),
    path('api/login/', views.login_view, name='login'),
    path('api/change-status/', views.change_status_view, name='change_status'),
    path('import-users/', views.import_users, name='import_users'),
    path('import-zlecenia/', views.import_zlecenia, name='import_zlecenia'),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]
