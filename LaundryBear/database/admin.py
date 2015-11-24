from django.contrib import admin

from database.models import LaundryShop, Price, Rating, Service, UserProfile, Transaction, Order, Fees
# Register your models here.


class PricesInline(admin.TabularInline):
    model = Price


class RatingsInline(admin.TabularInline):
    model = Rating


class LaundryShopAdmin(admin.ModelAdmin):
    inlines = [PricesInline, RatingsInline]


admin.site.register(LaundryShop, LaundryShopAdmin)
admin.site.register(Service)
admin.site.register(Rating)
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(Fees)
