from django.db import models
from userprofile.models import CustomUser
from organization.models import Organization

class Agent(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_agent': True})
    organizations = models.ManyToManyField(Organization, related_name='agents')
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='created_agents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        org_names = ", ".join([org.name for org in self.organizations.all()])
        return f"{self.user.username} - {org_names}"
    
