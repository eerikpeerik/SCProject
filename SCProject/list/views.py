from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ListItem
import sqlite3
from django.db import connection

@login_required
def add_item(request):
    if request.method == 'POST':
        item_text = request.POST.get('item_text')
        cursor = connection.cursor()

        sql = f"""
        INSERT INTO list_listitem (user_id, item_text)
        VALUES ({request.user.id}, '{item_text}');
        """
        cursor.executescript(sql)

#   FIX: By using Django's standard method, we can prevent SQL injections.
#     if request.method == 'POST':
#         item_text = request.POST.get('item_text')
#         ListItem.objects.create(user=request.user, item_text=item_text)

        return redirect('list')

    return render(request, 'list')


@login_required
def delete_item(request, item_id):
    # Ensure that the logged-in user is the owner of the item
    item = get_object_or_404(ListItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        item.delete()
        return redirect('list')
    
    # For GET requests, render a confirmation page
    return render(request, 'list/confirm_delete.html', {'item': item})

@login_required
def list_view(request):
    items = ListItem.objects.filter(user=request.user)
    return render(request, 'list/list.html', {'items': items, 'user': request.user})