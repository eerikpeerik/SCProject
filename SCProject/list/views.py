from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ListItem
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages 

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
    
    item = get_object_or_404(ListItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        item.delete()
        return redirect('list')
    
    return render(request, 'list/confirm_delete.html', {'item': item})

@login_required
def list_view(request):
    items = ListItem.objects.filter(user=request.user)
    return render(request, 'list/list.html', {'items': items, 'user': request.user})

    
@csrf_exempt # Remove @crsf_exempt to enable CSRF protection
    # Add in @login_required to provent Broken Access Control
def change_password(request):

    # Add in this to fix BAC
    #user = request.user

    # Comment out these two snippets of code to remove vulnerability to CSRF
    user = User.objects.get(username=request.GET.get("user"))
    password = request.GET.get('password')

    # Add these two snippets of code back in to protect against CSRF.
    #user = User.objects.get(username=request.POST.get("user"))
    #password = request.POST.get('password')
    
    # Checks if the password contains any character -> Prevents the password from being empty
    if (password):
        user.set_password(password)
        user.save()
    
    return redirect('/')


def csrfView(request):
	return render(request,'list/csrf_attack.html')