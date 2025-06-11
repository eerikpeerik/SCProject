from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ListItem
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


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

#         FIX: By using Django's standard method, we can prevent SQL injections.
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

@csrf_exempt
@login_required
def change_password(request):
    # Get the username and new password from the URL's query parameters.
    user = User.objects.get(username=request.GET.get("user"))
    password = request.GET.get('password')
    
    # Change the user's password.
    user.set_password(password)
    user.save()
    
    # Optionally log the event (commented out here).
    # notesLogger.info("user "+user.username+" changed their password")
    
    return redirect('/')


def csrfView(request):
	return render(request,'list/csrf_attack.html')