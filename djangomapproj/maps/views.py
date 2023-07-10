from django.shortcuts import render

from .models import DataType, DataGraph, DataMap, FederalDistrict, Region, DataGraphInstance, DataMapInstance, Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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

