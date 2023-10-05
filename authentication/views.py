from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Message, ChatRoom, User
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json
import asyncio
import websockets
from blog.forms import ImageForm
from .serializers import ChatRoomSerializer
# from .models import Profile


@login_required
def users(request):
    # users = User.objects.all()
    users = User.objects.all().exclude(id=request.user.id)
    return render(request, "home/all_users.html", {'users': users})


def get_chat_socket(request):
    # Retrieve the WebSocket server URL
    ws_url = 'ws://' + request.get_host() + '/ws/'
    # Get the current event loop
    loop = asyncio.get_event_loop()
    # Create a new WebSocket connection
    chat_socket = loop.run_until_complete(websockets.connect(ws_url))
    return chat_socket


@login_required
def start_chat(request, connection_id=None):
    
    if connection_id:
        other_user = get_object_or_404(User, id=connection_id)
        chat_room1 = ChatRoom.objects.filter(
            user1=request.user.user, user2=other_user).first()
        chat_room2 = ChatRoom.objects.filter(
            user1=other_user, user2=request.user.user).first()
        # Retrieve all user objects except the current user
        # users = User.objects.exclude(id=request.user.id)
        users = User.objects.all()

        # If chat room doesn't exist, create one
        if not chat_room1 and not chat_room2:
            chat_room = ChatRoom.objects.create(
                user1=request.user.user, user2=other_user)
        else:
            chat_room = chat_room1 or chat_room2

        if request.method == 'POST':
            content = request.POST.get('content')
            # Create a new message
            message = Message.objects.create(
                user=request.user.user, content=content, chat_room=chat_room)
            # Send the message to the WebSocket connection
            chatSocket = get_chat_socket(request)
            chatSocket.send(json.dumps({
                'type': 'chat',
                'message': message.content,

            }))

        # Retrieve all messages for this chat room
        messages = Message.objects.filter(chat_room=chat_room)
        chat_rooms = ChatRoom.objects.filter(
            user1=request.user.user) | ChatRoom.objects.filter(user2=request.user.user)
        # serializer = ChatRoomSerializer(chat_rooms, many=True)
        sidebar_info = ChatRoomSerializer(
            chat_rooms, many=True, context={'request': request})
        sidebar_info_data = sidebar_info.data
        # Render the start_chat template with the chat room and other user's name
        context = {
            'chat_room': chat_room,
            'messages': messages,
            'other_user': other_user,
            'users': users,
            'sidebar_info_data': sidebar_info_data,
            # 'chat_rooms': serialized_chat_rooms,
            'connection_id':connection_id,
        }
        return render(request, 'home/start_chat.html', context)

    else:
      users = User.objects.exclude(id=request.user.id)

      context = {
          'users':users,
         'connection_id':connection_id,       
      }
    
      return render(request, 'home/start_chat.html', context)


@csrf_protect
# def home_page(request, room_name=None):
#     return render(request, 'authentication/index.html')

def user_settings(request):
    user = request.user.user
    context = {
        'user': user,
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_image = request.FILES.get('profile_image')

        if not first_name:
            messages.error(request, 'First name is required.')
        if not last_name:
            messages.error(request, 'Last name is required.')

        if not messages.get_messages(request):  # If no error messages exist
            user.first_name = first_name
            user.last_name = last_name
            if profile_image:
                user.profile_image = profile_image
            user.save()
            messages.success(request, 'Profile updated successfully.')

    return render(request, 'home/user_settings.html', context)

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        if password1 != password2:
            print(password1, password2)
            messages.error(request, "Passwords do not match")
            return redirect("signup")
        
        # if not firstname or not lastname:
        #     messages.error(request, "First name and last name are required")
        #     return redirect("signup")

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        
        messages.success(
            request, "Your account has been created successfully!")
        return redirect("signin")
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Add this line to set the user in the session
            login(request, user)
            fname = user.first_name
            # return redirect("users")
            return redirect("initial_start_chat")
        else:
            messages.error(request, "Bad Credentials")
            return redirect("signin")
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')


async def websocket_consumer(websocket, path):
    # Do nothing, since we're just using the WebSocket connection to send messages
    print("hi")
