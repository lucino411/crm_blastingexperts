from django.db import models
from userprofile.models import CustomUser

 
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    email = models.EmailField(unique=True)
    members = models.ManyToManyField(
        CustomUser, related_name='organizations', blank=True)
    created_by = models.OneToOneField(
        CustomUser, on_delete=models.SET_NULL, related_name='created_organizations', null=True, blank=True
    )
    # related_name='created_organizations': Este es el nombre que puedes utilizar para acceder desde un objeto CustomUser a las organizaciones que ha creado. Por ejemplo, si tienes un objeto CustomUser llamado user, puedes acceder a las organizaciones que ha creado utilizando user.created_organizations.all().

    def __str__(self):
        created_by_username = self.created_by.username if self.created_by else "Unknown"
        return f"{self.name} - {created_by_username}"


