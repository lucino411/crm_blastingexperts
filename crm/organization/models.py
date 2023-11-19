from django.db import models
from userprofile.models import CustomUser

 
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    email = models.EmailField(unique=True)
    members = models.ManyToManyField(
        CustomUser, related_name='organizations', blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='created_organizations', null=True, blank=True
    )

    def __str__(self):
        created_by_username = self.created_by.username if self.created_by else "Unknown"
        return f"{self.name} - {created_by_username}"


