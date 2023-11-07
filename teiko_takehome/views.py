from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
import math
import os
import pandas as pd

from teiko_takehome.models import Project, Subject, Condition, Treatment, Sample, CellCount
from teiko_takehome.tools.analyzer import CellAnalyzer
import teiko_takehome.tools.queries as queries


def hello_world(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'Hello, world! (POST RESPONSE)'})
    return JsonResponse({'message': 'Hello, world!'})


def insert_into_database(file):
    try:
        reader = pd.read_csv(file, encoding='utf-8-sig')

        for index, row in reader.iterrows():
            project, _ = Project.objects.get_or_create(name=row['project'])
            subject, _ = Subject.objects.get_or_create(
                age=row['age'], sex=row['sex'])
            condition, _ = Condition.objects.get_or_create(
                name=row['condition'])
            treatment, _ = Treatment.objects.get_or_create(
                name=row['treatment'])

            sample, created = Sample.objects.get_or_create(
                subject=subject,
                project=project,
                treatment=treatment,
                condition=condition,
                sample_type=row['sample_type'],
                time_from_treatment_start=int(
                    row['time_from_treatment_start']) if not math.isnan(row['time_from_treatment_start']) else 0,
                response=row['response']
            )

            if created:
                CellCount.objects.create(
                    sample=sample,
                    b_cell=int(row['b_cell']),
                    cd8_t_cell=int(row['cd8_t_cell']),
                    cd4_t_cell=int(row['cd4_t_cell']),
                    nk_cell=int(row['nk_cell']),
                    monocyte=int(row['monocyte'])
                )
        return True
    except Exception as e:
        raise e


def upload_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']

        if insert_into_database(uploaded_file) == False:
            return JsonResponse({"message": "Failed to insert into Database!"})
        
        upload_dir = 'uploads/'

        os.makedirs(upload_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename_with_timestamp = f'{timestamp}_{uploaded_file.name}'

        with open(os.path.join(upload_dir, filename_with_timestamp), 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        analysis, image_urls = CellAnalyzer(filename_with_timestamp,
                     f'{filename_with_timestamp}_analyzed.csv')
        
        response_data = {
            'message': 'Successful upload!',
            'analysis': analysis,
            'image_urls': image_urls,
        }

        return JsonResponse(response_data)


def get_subject_count_by_condition_view(request):
    result = queries.get_subject_count_by_condition()
    result_json = list(result.values())
    return JsonResponse({'message': result_json})


def get_melanoma_pbmc_baseline_tr1_view(request):
    result = queries.get_melanoma_pbmc_baseline_tr1()
    result_json = list(result.values())
    return JsonResponse({'message': result_json})


def sample_count_by_project_view(request):
    result = queries.get_sample_count_by_project()
    result_json = list(result.values())
    return JsonResponse({'message': result_json})


def get_responder_count_view(request):
    result = queries.get_responder_count()
    result_json = list(result.values())
    return JsonResponse({'message': result_json})


def get_gender_count_view(request):
    result = queries.get_gender_count()
    result_json = list(result.values())
    return JsonResponse({'message': result_json})
