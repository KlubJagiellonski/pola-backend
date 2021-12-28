from django.contrib import admin

from .models import AIAttachment, AIPics


class AIAttachmentAdminInline(admin.TabularInline):
    model = AIAttachment
    list_display = ('id', 'ai_pics', 'file_no', 'attachment')
    list_filter = ('ai_pics',)


@admin.register(AIPics)
class AIPicsAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'created_at',
    )
    fields = [
        'id',
        'product',
        'client',
        'created_at',
        ('original_width', 'original_height', 'width', 'height'),
        'device_name',
        'flash_used',
        'was_portrait',
        'is_valid',
    ]
    list_display = (
        'id',
        'product',
        'client',
        'created_at',
        'is_valid',
    )
    inlines = [AIAttachmentAdminInline]
    list_filter = ('product', 'created_at', 'is_valid')
    date_hierarchy = 'created_at'


@admin.register(AIAttachment)
class AIAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ai_pics', 'file_no', 'attachment')
    list_filter = ('ai_pics',)
