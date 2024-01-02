from django.db import models

from django.conf import settings

# Create your models here.
class StudySpot(models.Model):
    id = models.AutoField(primary_key=True)  # Django will automatically add an auto-incrementing integer field named 'id' as the primary key
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    food = models.BooleanField(default=False)
    author = models.CharField(max_length=255)
    rejection_reason = models.TextField(blank=True, null=True)
    faved = models.BooleanField(default=False)



    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"

    STATUSES = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected')
    )

    status = models.CharField(max_length=15, choices=STATUSES, default=PENDING)

class Favorite(models.Model):
    pin=models.ForeignKey(StudySpot, on_delete=models.CASCADE)
    user=models.CharField(max_length=255)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['pin', 'user'], name='favid')]