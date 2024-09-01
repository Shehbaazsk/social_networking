from apps.users.models import FriendRequest, FriendRequestStatus


def send_friend_request(sender, receiver):
    if sender == receiver:
        raise ValueError("You cannot send a friend request to yourself.")
    try:
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=sender, receiver=receiver
        )
        if not created:
            if friend_request.status == FriendRequestStatus.PENDING:
                return {"message": "Friend request already sent and is pending."}
            elif friend_request.status == FriendRequestStatus.REJECTED:
                return {"message": "Friend request was rejected before."}

        return {"message": "Friend request sent successfully."}
    except Exception as e:
        raise ValueError("Something went wrong", str(e))


def accept_friend_request(current_user, friend_request):
    if friend_request.receiver == current_user:
        friend_request.status = FriendRequestStatus.ACCEPTED
        friend_request.save()
        current_user.friends.add(friend_request.sender)
        friend_request.sender.friends.add(current_user)
    else:
        raise ValueError("You cannot accept a friend request that not send to you.")


def reject_friend_request(current_user, friend_request):
    if friend_request.receiver == current_user:
        friend_request.status = FriendRequestStatus.REJECTED
        friend_request.save()
    else:
        raise ValueError("You cannot reject a friend request that not send to you.")
