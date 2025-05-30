from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ListItem
import sqlite3
from django.db import connection

@login_required
def list_view(request):
    items = ListItem.objects.filter(user=request.user)
    return render(request, 'list/list.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        item_text = request.POST.get('item_text')
        # Vulnerable raw SQL: directly linking user input into the query
        cursor = connection.cursor()
        sql = "INSERT INTO list_listitem (item_text, user_id) VALUES ('" + item_text + "', " + str(request.user.id) + ")"
        cursor.execute(sql)
        return redirect('list')
    return render(request, 'list/add_item.html')

# @login_required
# def add_item(request):
#    if request.method == 'POST':
#        item_text = request.POST.get('item_text')
#        if item_text:  # Ensure that the text is not empty
#            ListItem.objects.create(user=request.user, item_text=item_text)
#        return redirect('list')  # Redirect back to the list view
#    # Alternatively, if someone sends a GET request, you could render another template.
#    return render(request, 'list/add_item.html')s


@login_required
def delete_item(request, item_id):
    # Ensure that the logged-in user is the owner of the item
    item = get_object_or_404(ListItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        item.delete()
        return redirect('list')
    
    # For GET requests, render a confirmation page
    return render(request, 'list/confirm_delete.html', {'item': item})
