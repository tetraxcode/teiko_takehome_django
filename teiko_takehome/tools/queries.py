from django.db.models import Count
from teiko_takehome.models import Subject, Sample, Project, Treatment, Condition

# Function to summarize the number of subjects available for each condition
def get_subject_count_by_condition():
    subject_counts = Condition.objects.annotate(
        number_of_subjects=Count('sample__subject', distinct=True))
    return subject_counts

# Function that returns all melanoma PBMC samples at baseline from patients who have treatment tr1
def get_melanoma_pbmc_baseline_tr1():
    samples = Sample.objects.filter(
        condition__name='melanoma',
        sample_type='PBMC',
        treatment__name='tr1',
        time_from_treatment_start=0
    )
    return samples

# Function to get the number of samples from each project
def get_sample_count_by_project():
    sample_counts = Project.objects.annotate(number_of_samples=Count('sample'))
    return sample_counts

# Function to get the number of responders/non-responders
def get_responder_count():
    responder_counts = Sample.objects.values('response').annotate(number_of_samples=Count('id')).exclude(response='nan')
    return responder_counts

# Function to get the count of males and females
def get_gender_count():
    gender_counts = Subject.objects.values('sex').annotate(number_of_subjects=Count('id'))
    return gender_counts

