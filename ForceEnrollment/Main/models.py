from django.db import models

# Create your models here.
class Query(models.Model):
  query = models.CharField(max_length=255, default='')
  queryTimes = models.IntegerField(default=0)
  class Meta:
    db_table="Query"
