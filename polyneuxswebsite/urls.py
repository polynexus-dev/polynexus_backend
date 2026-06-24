"""
URL configuration for polyneuxswebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from cms import views as cms_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Public Read-Only APIs
    path('api/services', cms_views.get_services, name='api_services'),
    path('api/projects', cms_views.get_projects, name='api_projects'),
    path('api/projects/<int:id>/detail', cms_views.get_project, name='api_get_project'),
    path('api/testimonials', cms_views.get_testimonials, name='api_testimonials'),
    path('api/faqs', cms_views.get_faqs, name='api_faqs'),
    path('api/blog/posts', cms_views.get_blog_posts, name='api_blog_posts'),
    path('api/settings/contact', cms_views.get_contact_info, name='api_contact_settings'),
    path('api/settings/hero', cms_views.get_hero_info, name='api_hero_settings'),

    # Admin Auth API
    path('api/admin/login', cms_views.admin_login, name='api_admin_login'),

    # Admin CRUD APIs
    path('api/settings/hero/update', cms_views.update_hero_info, name='api_update_hero_info'),
    path('api/services/create', cms_views.create_service, name='api_create_service'),
    path('api/services/<str:id>', cms_views.update_delete_service, name='api_update_delete_service'),
    
    path('api/projects/create', cms_views.create_project, name='api_create_project'),
    path('api/projects/<int:id>', cms_views.update_delete_project, name='api_update_delete_project'),
    
    path('api/testimonials/create', cms_views.create_testimonial, name='api_create_testimonial'),
    path('api/testimonials/<int:id>', cms_views.update_delete_testimonial, name='api_update_delete_testimonial'),
    
    path('api/faqs/create', cms_views.create_faq, name='api_create_faq'),
    path('api/faqs/<int:id>', cms_views.update_delete_faq, name='api_update_delete_faq'),
    
    path('api/blog/posts/create', cms_views.create_blog_post, name='api_create_blog_post'),
    path('api/blog/posts/<int:id>', cms_views.update_delete_blog_post, name='api_update_delete_blog_post'),
    
    path('api/settings/contact/update', cms_views.update_contact_info, name='api_update_contact_info'),
]
