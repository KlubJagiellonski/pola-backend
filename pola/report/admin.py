from django.contrib import admin

from .models import Attachment, Report


class AttachmentIline(admin.TabularInline):
    model = Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'attachment')
    list_filter = ('report',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'client',
        'created',
        'resolved_at',
        'resolved_by',
    )
    list_filter = ('product', 'created', 'resolved_at', 'resolved_by')
    date_hierarchy = 'created'
    inlines = (AttachmentIline,)
