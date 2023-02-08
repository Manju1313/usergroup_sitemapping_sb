from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
import uuid
# Create your models here.
class BaseContent(models.Model):
    STATUS_CHOICES = ((1, 'Active'), (2, 'Inactive'),)
    
    status = models.PositiveIntegerField(
        choices=STATUS_CHOICES, default=1, db_index=True)
    server_created_on = models.DateTimeField(auto_now_add=True)
    server_modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='created%(app_label)s_%(class)s_related', null=True, blank=True,)
    modified_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='modified%(app_label)s_%(class)s_related', null=True, blank=True,)

    class Meta:
        abstract = True



class UserSiteMapping(BaseContent):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    #reporing_persons = models.fk(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username






class NoteModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    category = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notes"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.title

class Employee(models.Model):  
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)  
    mobile = models.CharField(max_length=10)  
    email = models.EmailField()  
  
    def __str__(self):  
        return "%s %s" % (self.first_name, self.last_name)  