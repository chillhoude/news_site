from django import forms
from django.contrib import admin
from  .models import  Blog, BlogHeshtags,Comment_user
from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.register(BlogHeshtags)
admin.site.register(Comment_user)

class BlogHeshtag(admin.StackedInline):
    model = BlogHeshtags

class BlogAdminForm(forms.ModelForm):
    full_text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    inlines = [BlogHeshtag]
    class Meta:
        model=Blog