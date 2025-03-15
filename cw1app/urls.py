from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from cw1app.views import UserViewSet, ProfessorViewSet, ProfessorAvgViewSet, ModuleViewSet, ModuleInstanceViewSet, RatingViewSet

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
professor_list = ProfessorViewSet.as_view({
    'get': 'list'
})
professorAvg_list = ProfessorAvgViewSet.as_view({
    'get': 'retrieve'
})
module_list = ModuleViewSet.as_view({
    'get': 'list'
})
moduleinstance_list = ModuleInstanceViewSet.as_view({
    'get': 'list'
})
rating_list = RatingViewSet.as_view({
    'get': 'list'
})

urlpatterns = format_suffix_patterns(
    [
        path('users/', user_list),
        path('professors/', professor_list),
        path('professors-avg/<str:professorCode>/<str:moduleCode>/', professorAvg_list),
        path('modules/', module_list),
        path('moduleinstances/', moduleinstance_list),
        path('ratings/', rating_list),
    ]
)