from django.contrib import admin

# Register your models here.
from .models import DataType, DataGraph, DataMap, FederalDistrict, Region, Author, ParcedModel

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'user')

@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    pass

'''class  DataGraphInstanceInline(admin.TabularInline):
    model = DataGraphInstance
    extra = 0'''

@admin.register(DataGraph)
class DataGraphAdmin(admin.ModelAdmin):
    pass
    #inlines = [DataGraphInstanceInline]

'''class  DataMapInstanceInline(admin.TabularInline):
    model = DataMapInstance
    extra = 0'''

@admin.register(DataMap)
class DataMapAdmin(admin.ModelAdmin):
    pass
    #inlines = [DataMapInstanceInline]

@admin.register(FederalDistrict)
class FederalDistrictAdmin(admin.ModelAdmin):
    pass

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass

'''@admin.register(DataGraphInstance)
class DataGraphInstanceAdmin(admin.ModelAdmin):
    list_display = ('region', 'federal_district', 'created')
    list_filter = ('region', 'federal_district', 'created')
    fieldsets = (
        ('Регион и ФО', {'fields': ('region', 'federal_district')}), 
                 (None, {'fields': ('created', 'user')}),)'''
    

'''@admin.register(DataMapInstance)
class DataMapInstanceAdmin(admin.ModelAdmin):
    list_display = ('region', 'federal_district', 'created')
    list_filter = ('region', 'federal_district', 'created')
    fieldsets = (
        ('Регион и ФО', {'fields': ('region', 'federal_district')}), 
                 (None, {'fields': ('created')}),)
                 '''
    
@admin.register(ParcedModel)
class ParcedModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'population_2023_estimate', 'population_2021_census', 'change', 'land_area_km2', 'pop_density_per_km2')
    list_filter = ('name', 'population_2023_estimate', 'population_2021_census', 'change', 'land_area_km2', 'pop_density_per_km2')
