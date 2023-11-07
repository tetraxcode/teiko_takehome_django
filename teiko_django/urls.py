"""
URL configuration for teiko_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from teiko_takehome import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello/', views.hello_world, name='hello_world'),
    path('upload/', views.upload_file, name='upload_file'),
    path('api/subject-count/', views.get_subject_count_by_condition_view, name='get_subject_count'),
    path('api/melanoma-pmbc/', views.get_melanoma_pbmc_baseline_tr1_view, name='get_melanoma_pmbc'),
    path('api/sample-count/', views.sample_count_by_project_view, name='sample_count_by_project'),
    path('api/responder-count/', views.get_responder_count_view, name='responder_count'),
    path('api/gender-count', views.get_gender_count_view, name='gender_count'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)