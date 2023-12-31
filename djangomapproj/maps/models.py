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
    summary = models.TextField(max_length=10000, help_text='Описание графика')
    key_dataset_on = models.CharField(max_length=200, primary_key=True, default='0000000')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('graph-detail', args=[str(self.id)])
    
class DataMap(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=10000, help_text='Описание карты')
    key_dataset_on = models.CharField(max_length=200, primary_key=True, default='0000000')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('map_list', args=[str(self.id)])
    
class FederalDistrict(models.Model):
    name = models.CharField(max_length=100, help_text='Введите название ФО')

    def __str__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField(max_length=100, help_text='Введите название региона')

    def __str__(self):
        return self.name

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
    rank = models.CharField(max_length=200, null=True, blank=True)
    federal_subject = models.CharField(max_length=200, null=True, blank=True)
    population_2023_estimate = models.CharField(max_length=200, null=True, blank=True)
    population_2021_census = models.CharField(max_length=200, null=True, blank=True)
    change =  models.CharField(max_length=200, null=True, blank=True)
    land_area_km2 = models.CharField(max_length=200, null=True, blank=True)
    pop_density_per_km2 = models.CharField(max_length=200, null=True, blank=True)

