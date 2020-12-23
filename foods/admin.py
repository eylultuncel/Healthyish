from django.contrib import admin
from .models import *


class foodAdmin(admin.ModelAdmin):
    class Meta:
        model=Food
    list_display=['name']
    list_filter=['name']


admin.site.register(DailyFood)
admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Food,foodAdmin)