from django.db import models
from . import managers


class AbstractStockModel(models.Model):
    """Abstract Stock Core Model"""
    # DateTimes
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # objects = managers.CustomModelManager()

    class Meta:
        abstract = True
