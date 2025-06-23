from django import forms
from .models import Asset, InventoryUser


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["asset_name", "asset_type", "purchase_date", "assigned_to", "status"]


class UserForm(forms.ModelForm):
    class Meta:
        model = InventoryUser
        fields = ["username", "fullname", "department", "email", "phone"]