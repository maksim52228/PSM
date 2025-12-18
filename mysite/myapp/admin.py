from django.contrib import admin
from .models import News, NewsImage
from django.contrib import admin
from .models import Application
from .models import Employee,Works,ChatMessage
from django.utils.html import format_html



class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3  # Количество пустых форм для добавления изображений

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]





@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed')  # Заменили phone на email
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'description')  # Обновили поисковые поля
    list_editable = ('is_processed',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'display_photo', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('name', 'position')
    list_filter = ('is_published',)
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'photo', 'bio')
        }),
        ('Дополнительные настройки', {
            'fields': ('is_published', 'order'),
            'classes': ('collapse',)
        }),
    )

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                               obj.photo.url)
        return "-"

    display_photo.short_description = 'Фото'


@admin.register(Works)
class WorksAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_photo', 'is_published', 'order', 'created_at')
    list_editable = ('is_published', 'order')
    search_fields = ('name', 'bio')
    list_filter = ('is_published', 'created_at')
    readonly_fields = ('created_at',)

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.photo.url)
        return "-"

    display_photo.short_description = 'Превью'


admin.site.register(ChatMessage)