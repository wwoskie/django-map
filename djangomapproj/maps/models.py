from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
# Create your models here.

class DataType(models.Model):
    name = models.CharField(max_length=200, help_text='Введите тип данных: график, карта, др.')

    def __str__(self):
        return self.name
    
class DataGraph(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=10000, help_text='Описание графика')
    data_type = models.ForeignKey(DataType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('graph-detail', args=[str(self.id)])
    
class DataMap(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(max_length=10000, help_text='Описание карты')
    data_type = models.ForeignKey(DataType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('map-detail', args=[str(self.id)])
    
class FederalDistrict(models.Model):
    name = models.CharField(max_length=100, help_text='Введите название ФО')

    def __str__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField(max_length=100, help_text='Введите название региона')

    def __str__(self):
        return self.name

class DataGraphInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный ID графика')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('Region', on_delete=models.RESTRICT, null=True)
    federal_district = models.ForeignKey('FederalDistrict', on_delete=models.RESTRICT, null=True)
    data_graph = models.ForeignKey('DataGraph', on_delete=models.RESTRICT, null=True)
    created = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.data_graph.title} {self.region} {self.federal_district} ({self.id})'

class DataMapInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный ID карты')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('Region', on_delete=models.RESTRICT, null=True)
    federal_district = models.ForeignKey('FederalDistrict', on_delete=models.RESTRICT, null=True)
    data_map = models.ForeignKey('DataMap', on_delete=models.RESTRICT, null=True)
    created = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.data_map.title} {self.region} {self.federal_district} ({self.id})'

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
class ParcedModel(models.Model):
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    geometry = models.CharField(max_length=20000)
    rank = models.CharField(max_length=200)
    federal_subject = models.CharField(max_length=200)
    population_2023_estimate = models.CharField(max_length=200)
    population_2021_census = models.CharField(max_length=200)
    change =  models.CharField(max_length=200)
    land_area_km2 = models.CharField(max_length=200)
    pop_density_per_km2 = models.CharField(max_length=200)

