import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Room
from .forms import JoinRoomForm, CreateRoomForm, SendMessageForm


def index(request):
    return render(request, 'chat_app/index.html')


@login_required
def profile(request):
    return render(request, 'chat_app/profile.html')


@login_required
def chat_default(request):
    rooms = request.user.users.all() # Apparently fetches all rooms the user is in
    return render(request, 'chat_app/room.html', {'rooms': rooms, 'current': None}) 


@login_required
def chat(request, invite):
    current = get_object_or_404(Room, invite=invite)
    rooms = request.user.users.all()

    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.room = current

            message.save()
    else:
        form = SendMessageForm()

    return render(request, 'chat_app/room.html', {'rooms': rooms, 'current': current, 'form': form})


@login_required
def new_chat(request):
    if request.method == "POST":
        if 'join_room' in request.POST:
            form1 = JoinRoomForm(request.POST, user=request.user)

            if form1.is_valid():
                room = Room.objects.get(invite=form1.cleaned_data['invite'])
                room.users.add(request.user)
                
                return redirect(f'/room/{room.invite}')
            form2 = CreateRoomForm()
    
        elif 'create_room' in request.POST:
            form2 = CreateRoomForm(request.POST)
            if form2.is_valid():
                room = None
                while not room:
                    invite = ''.join(random.sample(string.ascii_uppercase + string.digits, 8))
                    if Room.objects.filter(invite=invite).exists():
                        continue
                    
                    room = form2.save(commit=False)
        
                room.owner = request.user
                room.invite = invite
                room.save()
                room.users.add(request.user)

                return redirect(f'chat/room/{invite}')
            form1 = JoinRoomForm(user=request.user)
    else:
        form1 = JoinRoomForm(user=request.user)
        form2 = CreateRoomForm()

    return render(request, 'chat_app/new.html', {'form1': form1, 'form2': form2})

