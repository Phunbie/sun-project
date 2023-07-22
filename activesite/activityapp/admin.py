from django.contrib import admin
from .models import  Visit, Team,  UserTeam, Task, Profile , Audit

class visitAdmin(admin.ModelAdmin):
    list_display = ["user", "date","goal","achievement","notes","picture","created_at","updated_at"]

#admin.site.register(User)
admin.site.register(Visit, visitAdmin)
#admin.site.register(Visit)
admin.site.register(Team)
admin.site.register(UserTeam)
admin.site.register(Audit)
admin.site.register(Profile)
admin.site.register(Task)