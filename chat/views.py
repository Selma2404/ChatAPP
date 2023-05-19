import json
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
from .forms import  CreateUserForm
from django.views.decorators.csrf import csrf_exempt
from .models import  ChatUser
from django.utils.safestring import mark_safe
import json


@unauthenticated_user
def registerUser(request):
    if request.user.is_authenticated:
        return redirect('/chat')
    else:

        form = CreateUserForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                user=form.save
                username = form.cleaned_data.get('username')

                password=form.cleaned_data.get('password1')
                email=form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')

                user = User.objects.create_user(username=username,password=password , email=email, first_name=first_name, last_name=last_name)

                chatuser=ChatUser.objects.create(user=user, email=email ,first_name=first_name,last_name=last_name)


                messages.success(
                    request, 'Account was created for ' + username + ' you can login now')
                return redirect('/')
            else : 
                messages.error(request, 'Register Failed , Register again')

    context = {'form': form}
    return render(request, 'chat/register.html', context)

@unauthenticated_user
def loginUser(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('/chat')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/chat')
            else:
                messages.error(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'chat/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def chat(request):
    if request.user.is_authenticated:
        try:
            chat_user = ChatUser.objects.get(user=request.user)
        except ChatUser.DoesNotExist:
            chat_user = ChatUser.objects.create(user=request.user)
        users = User.objects.all()
        context = {'chat_user': chat_user, 'users': users}
        return render(request, 'chat/chat.html', context)
    else:
        return redirect('/')
    
def chat_room(request, user_id):
    if request.user.is_authenticated:
    # Retrieve the ChatUser objects for the currently logged in user and the selected user
        current_user = request.user.chatuser
        selected_user = get_object_or_404(ChatUser, pk=user_id)
        users = User.objects.all()

        context = {
            'selected_user': selected_user,
            'users' : users
        }
        return render(request, 'chat/chat.html', context)
    else :
        return redirect('/')



def get_messages(request, user_id):
    # get the logged-in user
    logged_in_user = request.user.chatuser

    # get the selected user
    selected_user = ChatUser.objects.get(pk=user_id)

    # get the messages between the logged-in user and the selected user
    messages = Messages.objects.filter(sender=logged_in_user, receiver=selected_user) | Messages.objects.filter(sender=selected_user, receiver=logged_in_user)

    # render the messages as HTML
    messages_html = ''
    for message in messages:
        messages_html += '<p>{}</p>'.format(message.content)

    # return the messages as JSON
    return JsonResponse({'messages': messages_html})

