import os
import shutil
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.export_to_docx import create_docx_with_tables
from api.models import Branch, Organization, Tallon
from api.schemas import create_branch_schema, update_branch_schema, get_branches_schema, create_organization_schema, \
    update_organization_schema, get_organizations_schema, get_tallon_table_data_all_schema, \
    get_tallon_table_data_detail_schema, create_tallon_schema, update_tallon_schema, download_docx_schema
from api.serializers import BranchSerializer, OrganizationSerializer, TallonGetSerializer, TallonSerializer
from utils.pagination import pagination
from utils.permissions import allowed_only_admin
from utils.responses import success
from django.urls import reverse


@create_branch_schema
@api_view(['POST'])
@allowed_only_admin()
def create_branch(request):
    serializer = BranchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@update_branch_schema
@api_view(['PUT'])
@allowed_only_admin()
def update_branch(request):
    pk = request.query_params.get('pk')
    branch = Branch.objects.get(id=pk)
    serializer = BranchSerializer(branch, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_branches_schema
@api_view(['GET'])
# @allowed_only_admin()
def get_branches(request):
    branches = Branch.objects.all().order_by('name')
    serializor = BranchSerializer(branches, many=True)
    return Response(serializor.data, 200)


@create_organization_schema
@api_view(['POST'])
@allowed_only_admin()
def create_organization(request):
    serializer = OrganizationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@update_organization_schema
@api_view(['PUT'])
@allowed_only_admin()
def update_organization(request):
    pk = request.query_params.get('pk')
    organization = Organization.objects.get(id=pk)
    serializer = OrganizationSerializer(organization, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_organizations_schema
@api_view(['GET'])
# @allowed_only_admin()
def get_organizations(request):
    pk = request.query_params.get('pk')
    organizations = Organization.objects.filter(branch=pk).all().order_by('name')
    serializor = OrganizationSerializer(organizations, many=True)
    return Response(serializor.data, 200)


@create_tallon_schema
@api_view(['POST'])
def create_tallon(request):
    serializer = TallonSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@update_tallon_schema
@api_view(['PUT'])
def update_tallon(request):
    pk = request.query_params.get('pk')
    tallon = Tallon.objects.get(id=pk)
    serializer = TallonSerializer(tallon, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_tallon_table_data_all_schema
@api_view(['GET'])
def get_tallon_table_data_all(request):
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    if from_date and to_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'from_date and to_date date format is wrong!'}, status=422)

        if from_date > to_date:
            return Response({'detail': 'from_date must be less than to_date!'}, status=422)

        tallons = Tallon.objects.filter(date_received__range=[from_date, to_date])
        text = f"{from_date} - {to_date}"
    else:
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        tallons = Tallon.objects.filter(date_received__range=[start_of_month, today])
        text = f'{start_of_month} - {today}'

    table1_data = []
    table2_data = []
    branches = Branch.objects.all()
    for branch in branches:
        tallons_1 = tallons.filter(branch=branch, tallon_number__contains='1').count()
        tallons_2 = tallons.filter(branch=branch, tallon_number__contains='2').count()
        tallons_3 = tallons.filter(branch=branch, tallon_number__contains='3').count()
        jami = tallons_1 + tallons_2 + tallons_3

        table1_data.append({
            'branch': branch.name,
            'number1': tallons_1,
            'number2': tallons_2,
            'number3': tallons_3,
            'jami': jami
        })

        summa = tallons.filter(branch=branch).aggregate(Sum('consequence_amount'))['consequence_amount__sum']
        table2_data.append({
            'branch': branch.name,
            'jami': summa if summa is not None else 0
        })

    return Response({
        'text': text,
        'table1': table1_data,
        'table2': table2_data
    }, status=200)


@get_tallon_table_data_detail_schema
@api_view(['GET'])
def get_tallon_table_data_detail(request):
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    branch_pk = request.query_params.get('branch_pk')
    organization_pk = request.query_params.get('organization_pk')
    if from_date and to_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'from_date and to_date date format is wrong!'}, status=422)

        if from_date > to_date:
            return Response({'detail': 'from_date must be less than to_date!'}, status=422)

        if request.user.is_superuser:
            if branch_pk and organization_pk:
                tallons = Tallon.objects.filter(branch=branch_pk, organization=organization_pk,
                                                date_received__range=[from_date, to_date]
                                                ).select_related('branch', 'organization')
            elif branch_pk:
                tallons = Tallon.objects.filter(branch=branch_pk, date_received__range=[from_date, to_date]
                                                ).select_related('branch', 'organization')
            else:
                tallons = Tallon.objects.filter(date_received__range=[from_date, to_date]
                                                ).select_related('branch', 'organization')
        else:
            tallons = Tallon.objects.filter(branch=request.user.branch, date_received__range=[from_date, to_date]
                                            ).select_related('branch', 'organization')
    else:
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        if request.user.is_superuser:
            if branch_pk and organization_pk:
                tallons = Tallon.objects.filter(branch=branch_pk, organization=organization_pk,
                                                date_received__range=[from_date, to_date]
                                                ).select_related('branch', 'organization')
            elif branch_pk:
                tallons = Tallon.objects.filter(branch=branch_pk, date_received__range=[start_of_month, today]
                                                ).select_related('branch', 'organization')
            else:
                tallons = Tallon.objects.filter(date_received__range=[start_of_month, today]
                                                ).select_related('branch', 'organization')
        else:
            tallons = Tallon.objects.filter(branch=request.user.branch, date_received__range=[start_of_month, today]
                                            ).select_related('branch', 'organization')

    result = pagination(tallons, TallonGetSerializer, request)
    return Response(result, 200)


@download_docx_schema
@api_view(['GET'])
@allowed_only_admin()
def download_docx(request):
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')

    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({'detail': 'from_date and to_date date format is wrong!'}, status=422)

    if from_date > to_date:
        return Response({'detail': 'from_date must be less than to_date!'}, status=422)

    tallons = Tallon.objects.filter(date_received__range=[from_date, to_date])

    buffer = create_docx_with_tables(tallons, from_date, to_date)

    user_folder = os.path.join('docx', request.user.username)
    os.makedirs(user_folder, exist_ok=True)

    temp_filename = f'tallonlar_{from_date}_to_{to_date}.docx'
    temp_filepath = os.path.join(user_folder, temp_filename)

    with open(temp_filepath, 'wb') as f:
        f.write(buffer.getvalue())
    download_url = request.build_absolute_uri(reverse('download_temp_file', kwargs={
        'filename': temp_filename,
        'username': request.user.username}))

    response = HttpResponse(buffer,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename={temp_filename}'

    return Response({'download_url': download_url})


@extend_schema(exclude=True)
@api_view(['GET'])
@permission_classes([AllowAny])
def download_temp_file(request, filename, username):
    user_folder = os.path.join('docx', username)
    file_path = os.path.join(user_folder, filename)

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={filename}'
    except FileNotFoundError:
        return Response({'detail': 'File not found.'}, status=404)
    finally:
        if os.path.exists(user_folder):
            try:
                shutil.rmtree(user_folder)
            except OSError:
                pass

    return response
