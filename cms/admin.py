from django.contrib import admin
from .models import Service, Project, Testimonial, FAQ, BlogPost, ContactSetting, Enquiry

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'icon')
    search_fields = ('title', 'shortDesc', 'fullDesc')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'metric', 'metricLabel')
    list_filter = ('category',)
    search_fields = ('title', 'desc')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'role', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'company', 'content')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question', 'answer')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'readTime')
    list_filter = ('category', 'date')
    search_fields = ('title', 'summary')


@admin.register(ContactSetting)
class ContactSettingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'phone', 'address')
    
    def has_add_permission(self, request):
        # Prevent adding more than one configuration
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the configuration
        return False


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'replied', 'created_at')
    list_filter = ('replied', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
