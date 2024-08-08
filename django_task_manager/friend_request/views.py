from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required

from taskmanager.models import ProjectMembership
from .models import FriendRequest, User, Notification

User = get_user_model()


@login_required
def send_friend_request(request):
    if request.method == 'POST':
        email = request.POST.get('team_member_email')
        try:
            to_user = User.objects.get(email=email)
        except User.DoesNotExist:

            return render(request, 'projects/projects.html', {'error_message': 'User with this email does not exist.'})

        if to_user == request.user:
            return render(request, 'projects/projects.html',
                          {'error_message': 'You cannot send a friend request to yourself.'})

        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return render(request, 'projects/projects.html', {'error_message': 'Friend request already sent.'})

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)

        return redirect('start_project')

    return redirect('start_project')


@login_required
def manage_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if action == 'accept':
        friend_request.is_accepted = True
        friend_request.save()

        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)

        Notification.objects.create(
            user=friend_request.from_user,
            message=f"{request.user.username} has accepted your friend request."
        )
        friend_request.delete()


    elif action == 'decline':
        friend_request.delete()

    return redirect('home_page')


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('start_project')
