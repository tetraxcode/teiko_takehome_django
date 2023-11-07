from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    age = models.PositiveBigIntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    def __str__(self):
        return f"Subject {self.id} - Age: {self.age}, Sex: {self.sex}"
    
class Condition(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Treatment(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Sample(models.Model):
    RESPONSE_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    sample_type = models.CharField(max_length=255)
    time_from_treatment_start = models.PositiveBigIntegerField()
    response = models.CharField(max_length=1, choices=RESPONSE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Sample {self.id}"

class CellCount(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='cell_counts')
    b_cell = models.PositiveBigIntegerField()
    cd8_t_cell = models.PositiveBigIntegerField()
    cd4_t_cell = models.PositiveBigIntegerField()
    nk_cell = models.PositiveBigIntegerField()
    monocyte = models.PositiveBigIntegerField()

    def __str__(self):
        return f"CellCount for Sample {self.sample.id}"
    

