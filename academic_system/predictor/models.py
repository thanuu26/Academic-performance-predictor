from django.db import models

class StudentPrediction(models.Model):
    student_name = models.CharField(max_length=100) # Used to store the student's email
    attendance_rate = models.FloatField()
    study_hours = models.FloatField()
    online_courses = models.FloatField()
    assignment_rate = models.FloatField()
    learning_style = models.CharField(max_length=50) 
    is_at_risk = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name