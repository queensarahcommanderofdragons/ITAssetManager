from django.db import models

class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=50)
    asset_type = models.CharField(max_length=100)
    purchase_date = models.DateField()
    assigned_to = models.ForeignKey('InventoryUser', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.asset_name


class InventoryUser(models.Model):
    username = models.CharField(max_length=45, primary_key=True)
    fullname = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class AssetHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    changed_by = models.ForeignKey("InventoryUser", on_delete=models.SET_NULL, null=True)

    change_date = models.DateTimeField(auto_now_add=True)
    change_details = models.TextField()

    def __str__(self):
        return f"{self.asset.asset_name} updated by {self.changed_by}"
