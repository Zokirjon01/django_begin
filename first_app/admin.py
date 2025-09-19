from django.contrib import admin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "user_agent", "visited_at")
    list_filter = ("visited_at",)
    search_fields = ("ip_address", "user_agent")
