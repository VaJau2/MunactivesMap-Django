from django.contrib.gis.db import models

#модельки БД

class holder(models.Model):
    holder_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    address = models.TextField()
    fio = models.TextField()

    def __str__(self):
        return str(self.name)


class foundation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey('spr_type_foundation', on_delete=models.PROTECT)
    address = models.TextField()
    square = models.FloatField()
    describe = models.TextField()
    coordinates = models.PointField()
    holder_num = models.ForeignKey('holder', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)


class spr_type_foundation(models.Model):
    type = models.CharField(primary_key=True,max_length=50)
    description = models.TextField()
    purpose = models.TextField()

    def __str__(self):
        return str(self.type)


class company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey('spr_type_company', on_delete=models.PROTECT)
    address = models.TextField()
    square = models.FloatField()
    describe = models.TextField()
    coordinates = models.PointField()
    holder_num = models.ForeignKey('holder', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)


class spr_type_company(models.Model):
    type = models.CharField(primary_key=True,max_length=50)
    description = models.TextField()

    def __str__(self):
        return str(self.type)


class housing_stock(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.ForeignKey('spr_type_stock', on_delete=models.PROTECT)
    address = models.TextField()
    square = models.FloatField()
    describe = models.TextField()
    coordinates = models.PointField()
    floors = models.IntegerField()
    holder_num = models.ForeignKey('holder', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)


class spr_type_stock(models.Model):
    type = models.CharField(primary_key=True,max_length=50)
    description = models.TextField()

    def __str__(self):
        return str(self.type)
    

class munitipal_land(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    purpose = models.TextField()
    square = models.FloatField()
    describe = models.TextField()
    coordinates = models.PolygonField()
    holder_num = models.ForeignKey('holder', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)


