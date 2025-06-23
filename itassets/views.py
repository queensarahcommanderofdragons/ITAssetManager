from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from itassets.models import Asset, AssetHistory, InventoryUser
from .forms import AssetForm, UserForm
import csv
from django.http import HttpResponse
from itassets.models import Asset, InventoryUser
from django.core.management import call_command

from .models import InventoryUser


def asset_list(request):
    # View and search assets.
    query = request.GET.get("q")
    sort_by = request.GET.get("sort", "asset_id")
    status_filter = request.GET.get("status", "all") # defaults to all

    assets = Asset.objects.all()  # assets are defined before filtering

    if query:
        assets = assets.filter(asset_name__icontains=query)

    # Apply status filter
    if status_filter == "active":
        assets = assets.filter(status="Active")
    elif status_filter == "Inactive":
        assets = assets.filter(status="Inactive")

    #  Apply sorting
    assets = assets.order_by(sort_by)

    return render(request, "itassets/asset_list.html",{
        "assets": assets,
        "query": query,
        "sort_by": sort_by,

        "status_filter": status_filter
    })


@login_required
@permission_required("itassets.add_asset", raise_exception=True)
def asset_create(request):

    # Allow only authorized users to create assets. #
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("asset_list")

    else:
        form = AssetForm()
    return render(request, "itassets/asset_form.html", {"form": form})

@login_required
@permission_required("itassets.change_asset", raise_exception=True)
def asset_update(request, pk):
    # Allow only admins to update assets & log history as in permissions.
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()

            # Log history after saving, before redirecting
            AssetHistory.objects.create(
                asset=asset,
                changed_by=request.user,  # Track who made the change
                change_details=f"Updated asset: {asset.asset_name}"
            )
            return redirect("asset_list")  # Move redirect after history logging

    else:
        form = AssetForm(instance=asset)

    return render(request, "itassets/asset_form.html", {"form": form})

@login_required
@permission_required("itassets.delete_asset", raise_exception=True)
def asset_delete(request, pk):
    # Allow only admins to delete assets and log the deletion.
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        # Log deletion before actually removing the asset

        inventory_user = InventoryUser.objects.filter(username=request.user.username).first()

        if inventory_user:

            AssetHistory.objects.create(
                asset=asset,
                changed_by=request.inventory_user,
                change_details=f"Deleted asset: {asset.asset_name}"

            )
        asset.delete()
        return redirect("asset_list")

    return render(request, "itassets/asset_confirm_delete.html", {"asset": asset})

@login_required
@permission_required("itassets.view_asset", raise_exception=True)
def export_assets_csv(required):
    # Export asset list into CSV for Admin download
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposistion"] = 'attachment; filename"assets.csv'

    writer = csv.writer(response)
    writer.writerow(["Asset ID", "Name", "Type", "Purchase Date", "Assigned To", "Status"])

    for asset in Asset.objects.all():
        writer.writerow([asset.asset_id, asset.asset_name, asset.asset_type, asset.purchase_date, asset.assigned_to, asset.status])

        return response


@login_required
def user_list(request):
    #  Display all inventory users.
    users = InventoryUser.objects.all()
    return render(request, "itassets/user_list.html", {"users": users})


@login_required
@permission_required("itassets.add_user", raise_exception=True)
def user_create(request):
    # Allow admins to add a new inventory user
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserForm()
    return render(request, "itassets/InventoryUser_form.html", {"form": form})


@login_required
@permission_required("itassets.change_user", raise_exception=True)
def user_edit(request, username):
    # Allow admins to edit inventory users
    user = get_object_or_404(InventoryUser, username=username)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserForm(instance=user)

    return render(request, "itassets/user_form.html", {"form": form, "user": user})


@login_required
@permission_required("itassets.delete_user", raise_exception=True)
def user_delete(request, username):
    # Allow admins to delete inventory users.
    user = get_object_or_404(InventoryUser, username=username)
    if request.method == "POST":
        user.delete()

        return redirect("user_list")

    return render(request, "itassets/user_confirm_delete.html", {"users": user})

@login_required
def user_assets(request, username):
    user = get_object_or_404(InventoryUser, username=username)
    assets = Asset.objects.filter(assigned_to=user)

    return render(request, "itassets/user_assets.html", {
        "user": user,
        "assets": assets,

        "department": user.department,
        "email": user.email,
        "phone": user.phone,
    })

@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    return render(request, "itassets/asset_detail.html", {"asset": asset})



def load_db_view(request):
    try:
        call_command('loaddata', 'db.json')
        return HttpResponse("Data loaded successfully into PostgreSQL.")
    except Exception as e:
        return HttpResponse(f" Error: {e}")