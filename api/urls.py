from django.urls import path
from api.views import (create_branch, update_branch, get_branches, create_organization, update_organization,
                       get_organizations, get_tallon_table_data_all, get_tallon_table_data_detail, create_tallon,
                       update_tallon, download_docx, download_temp_file)

urlpatterns = [
    # path('branch/create/', create_branch, name='create_branch'),
    # path('branch/update/', update_branch, name='update_branch'),
    path('branch/all/', get_branches, name='get_branches'),

    path('organization/create/', create_organization, name='create_organization'),
    path('organization/update/', update_organization, name='update_organization'),
    path('organization/all/', get_organizations, name='get_organizations'),

    path('tallon/create/', create_tallon, name='create_tallon'),
    path('tallon/update/', update_tallon, name='update_tallon'),
    path('tallon/table/data/all/', get_tallon_table_data_all, name='get_tallon_table_data_all'),
    path('tallon/table/data/detail/', get_tallon_table_data_detail, name='get_tallon_table_data_detail'),
    path('tallon/download/docx/', download_docx, name='download_docx'),
    path('tallon/download/temp/<str:filename>/<str:username>/', download_temp_file, name='download_temp_file'),
]
