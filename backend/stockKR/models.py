from django.db import models
from stock import models as core_models

# Create your models here.
class krStockElementModel(models.Model):
    """Abstract Stock Core Model"""
    stockType = models.ForeignKey("stockKR.stockKR", related_name="daily_element")
    
    date = models.DateField()
    
    
    # Price Info.
    start_price = models.IntegerField()
    end_price = models.IntegerField()
    high_price = models.IntegerField()
    low_price  = models.IntegerField()

    # Trade quantity.
    trade_quant = models.IntegerField()
    trade_money = models.IntegerField()

    # Macro Info.
    total_stock_count = models.IntegerField()
    total_comp_price  = models.IntegerField()

# Create your models here.
class stockKR(core_models.AbstractStockModel):
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=20)

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
