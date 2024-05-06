from django.contrib import admin
# Register your models here.
from .models import User, Listing, Offers, Comments, Winners

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Offers)
admin.site.register(Comments)
admin.site.register(Winners)
