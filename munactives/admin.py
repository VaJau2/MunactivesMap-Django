from django.contrib import admin

from .models import foundation, spr_type_foundation, company, spr_type_company, housing_stock, spr_type_stock, munitipal_land
from .models import holder

admin.site.register(foundation)
admin.site.register(spr_type_foundation)
admin.site.register(company)
admin.site.register(spr_type_company)
admin.site.register(housing_stock)
admin.site.register(spr_type_stock)
admin.site.register(munitipal_land)
admin.site.register(holder)