from django.shortcuts import render, redirect
import os
import folium
from .models import DataType, DataGraph, DataMap, FederalDistrict, Region, DataGraphInstance, DataMapInstance, Author, ParcedModel
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
import geopandas as gpd
from django_pandas.io import read_frame
from difflib import SequenceMatcher

def index(request):
    num_data_types = DataType.objects.all().count()
    num_graph_types = DataGraph.objects.all().count()
    num_map_types = DataMap.objects.all().count()
    num_graph_instances = DataGraphInstance.objects.all().count()
    num_map_instances = DataMapInstance.objects.all().count()
    num_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_data_types': num_data_types,
        'num_graph_types': num_graph_types,
        'num_map_types': num_map_types,
        'num_graph_instances': num_graph_instances,
        'num_map_instances': num_map_instances,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

class UserCreatedGraphListView(LoginRequiredMixin,generic.ListView):
    model = DataGraphInstance
    template_name = 'maps/datagraphinstance_list_created_user.html'
    paginate_by = 1

    def get_queryset(self):
        return (
            DataGraphInstance.objects.filter(user=self.request.user)
        )
    
def map(request):
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    R_border_style = {
        'color': 'red',
        'weight': 1,
        'fill': False
    }

    m = folium.Map(zoom_start=5, 
                              tiles='cartodbpositron', 
                              location = [55.799534, 37.460218], 
                              prefer_canvas=True,
                              max_bounds=True)
    adm_lvl_4 = gpd.read_file('admin_level_4.geojson')
    adm_lvl_4 = adm_lvl_4[adm_lvl_4['addr:country'] == 'RU']
    adm_lvl_4 = adm_lvl_4[['name', 'name:en', 'geometry']]
    
    '''qs = ParcedModel.objects.all()
    pop_data = read_frame(qs)

    pop_data.to_csv('table_before.csv', index=False, sep='\t')

    pop_data.dropna(inplace = True)

    pop_data.to_csv('table_after.csv', index=False, sep='\t')
    
    

    pop_list = list(pop_data['federal_subject'])
    geo_list = list(adm_lvl_4['name:en'])
    match_name = []
    match_geo = []

    ratio_dct_all = {}
    for df_name in pop_list:
        ratio_dct = {}
        for geojson_name in geo_list:
            if similar(df_name, geojson_name) == 1:
                match_name.append(df_name)
                match_geo.append(geojson_name)
            ratio_dct[geojson_name] = similar(df_name, geojson_name)
        dict_max = max(ratio_dct.values())
        ratio_dct_all[df_name] = ratio_dct
    
    match_matrix = pd.DataFrame(ratio_dct_all)
    match_matrix.drop(match_name, inplace = True)
    match_matrix.drop(match_geo, axis=1, inplace = True)

    for column in match_matrix:
        match_geo.append(match_matrix[column].idxmax())
        match_name.append(column)
        match_matrix.drop(match_matrix[column].idxmax(), inplace = True)

    match_df = pd.DataFrame({'match_name': match_name, 'match_geo': match_geo})
    pop_data = pop_data.merge(match_df, how="left", left_on=['federal_subject'], right_on=['match_name'])
    table = adm_lvl_4.merge(pop_data, how="left", left_on=['name:en'], right_on=['match_geo'])
    table.drop(columns=['match_name', 'match_geo'], inplace=True)
    table.rename(columns={'name:en': 'name_en'}, inplace=True)
    table.dropna(inplace = True)

    table.to_csv('table_after_after.csv', index=False, sep='\t')'''
    '''
    
    folium.Choropleth(
        geo_data=table,
        name='Population',
        data=table,
        columns=['name_en', 'population_2023_estimate'],
        key_on='feature.properties.name',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='rus_pop'
    ).add_to(m)
    '''

    folium.GeoJson(data = 'admin_level_4.geojson',
               name = 'Регионы',
               style_function=lambda x:R_border_style).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    m=m._repr_html_()

    context = {'my_map': m}

    return render(request,'maps/map.html', context=context)


