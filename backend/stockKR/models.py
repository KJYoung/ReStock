from unicodedata import category
from django.db import models
from stock import models as core_models

# Create your models here.
class krStockElementModel(models.Model):
    """Abstract Stock Core Model"""

    stock_type = models.ForeignKey("stockKR.stockKR", on_delete=models.CASCADE, related_name="daily_element")

    date = models.DateField()

    # Price Info.
    start_price = models.IntegerField()
    end_price = models.IntegerField()
    high_price = models.IntegerField()
    low_price = models.IntegerField()

    # Trade quantity.
    trade_quant = models.IntegerField()
    trade_money = models.IntegerField()

    # Macro Info.
    total_stock_count = models.IntegerField()
    total_comp_price = models.IntegerField()

    def __str__(self):
        return f"{self.stock_type.category}/{self.stock_type.name}_{self.date}"


# Create your models here.
class stockKR(core_models.AbstractStockModel):
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=20)
    short_code = models.CharField(max_length=30)
    isin_code = models.CharField(max_length=40)

    first_date = models.DateField()
    last_date = models.DateField()
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    def total_daily_num(self):
        daily_elements = self.daily_element.all().count()
        return daily_elements
    
    total_daily_num.short_description = "불러온 개수"
    name.verbose_name = "종목명"
    category.verbose_name   = "카테고리"
    first_date.verbose_name = "시작일"
    last_date.verbose_name  = "종료일"