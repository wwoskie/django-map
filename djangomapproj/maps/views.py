from django.shortcuts import render
import numpy as np
import folium
from .models import DataType, DataGraph, DataMap, Author, ParcedModel
from django.views import generic
import pandas as pd
import geopandas as gpd
from django_pandas.io import read_frame
from django.http import Http404
from difflib import SequenceMatcher
from math import log10, floor, ceil

def find_exp(number):
    base10 = log10(number)
    return floor(base10)

def find_exp2(number):
    base10 = log10(number)
    return base10

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def index(request):
    num_data_types = DataType.objects.all().count()
    num_graph_types = DataGraph.objects.all().count()
    num_map_types = DataMap.objects.all().count()
    num_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_data_types': num_data_types,
        'num_graph_types': num_graph_types,
        'num_map_types': num_map_types,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author
    
def map_detail_view(request, pk):
    try:
        map_parameter = DataMap.objects.get(pk=pk).key_dataset_on
    except DataMap.DoesNotExist:
        raise Http404('Карта не существует')

    m = folium.Map(zoom_start=5, 
                              tiles='cartodbpositron', 
                              location = [55.799534, 37.460218], 
                              prefer_canvas=True,
                              max_bounds=True)
    
    queryset = ParcedModel.objects.all()
    map_title = DataMap.objects.get(pk=pk).title
    pop_data = read_frame(queryset)
    pop_data.dropna(inplace=True)

    pop_data = pop_data[['federal_subject', map_parameter]]
    pop_data[map_parameter] = pop_data[map_parameter].astype('float')

    adm_lvl_4 = gpd.read_file('../data/admin_level_4.geojson')
    adm_lvl_4 = adm_lvl_4[adm_lvl_4['addr:country'] == 'RU']
    adm_lvl_4 = adm_lvl_4[['name', 'name:en', 'geometry']]
    

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
    table.rename(columns={'name:en': 'name_en'}, inplace=True)

    choro = folium.Choropleth(
        line_weight=1.5,
        line_color='grey',
        geo_data=table,
        name=map_title,
        data=table,
        columns=['name_en', map_parameter],
        key_on='feature.properties.name_en',
        fill_color='Purples',
        fill_opacity=1,
        line_opacity=0.2,
        bins=50,
        use_jenks=True,
        legend_name=map_title,
    )


    for key in choro._children:
        if key.startswith('color_map'):
            del(choro._children[key])
    

    choro.add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
    
    highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

    highlight = folium.features.GeoJson(
        data = table,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name_en', map_parameter],
            aliases=['Region name', map_title],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        ))
    
    #folium.LayerControl().add_to(m)
    m.add_child(highlight)
    m.keep_in_front(highlight)
    
    m=m._repr_html_()

    context = {'my_map': m,
               'map_parameter': map_parameter,
               'map_title': DataMap.objects.get(pk=pk).title,
               'summary': DataMap.objects.get(pk=pk).summary}

    return render(request,'maps/map_detail.html', context=context)

class MapsListView(generic.ListView):
    model = DataMap
    context_object_name = 'maps_list'
    template_name = 'maps/maps_list.html'


