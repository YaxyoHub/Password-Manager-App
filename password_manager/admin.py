from django.contrib import admin
from .models import (
    User,
    OTP_codes,
    App_Password
)

# Register your models here.

admin.site.register(User)
admin.site.register(OTP_codes)
admin.site.register(App_Password)
