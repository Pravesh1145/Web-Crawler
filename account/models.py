from django.db import models

class deals(models.Model):
    id = models.AutoField(primary_key=True, db_column='deals_id')
    name = models.CharField(max_length=256, db_column="deals_name", default=0)
    url = models.CharField(max_length=512, db_column="deals_url", default=0)
    image = models.CharField(max_length=512, db_column="deals_image", default=0)
    mrp = models.DecimalField(max_digits=11, decimal_places=2, db_column="deals_mrp", default=0)
    price = models.DecimalField(max_digits=11, decimal_places=2, db_column="deals_price", default=0)
    storeimage = models.CharField(max_length=512, db_column="deals_store_image", default=0)
    