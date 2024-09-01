from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.users.api.service import (
    accept_friend_request,
    reject_friend_request,
    send_friend_request,
)
from apps.users.models import FriendRequest, User
from apps.users.serializers import UserRegisterSerializers


class UserRegisterAPIView(GenericAPIView):
    """ " Api for registering user"""

    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "user created successfully"}, status=status.HTTP_201_CREATED
        )


###### HERE WE CAN ALSO SPECIFY LOGIN API AND GIVE TOKEN MANUALLY BUT I'M DIRECTLY USING JWT ######


class SendFriendRequestAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "send-friend-request"

    def post(self, request, *args, **kwargs):
        try:
            receiver_uuid = request.data.get("receiver_uuid")
            if not receiver_uuid:
                return Response(
                    {"error": "The 'receiver_uuid' parameter is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            receiver = User.objects.get(uuid=receiver_uuid)

            if not receiver:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )
            response = send_friend_request(request.user, receiver)
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RespondFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            friend_request_uuid = request.data.get("friend_request_uuid")
            if not friend_request_uuid:
                return Response(
                    {"error": "The 'friend_request_uuid' parameter is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            friend_request = FriendRequest.objects.get(uuid=friend_request_uuid)
            action = request.data.get("action")

            if action == "accept":
                accept_friend_request(friend_request)
                return Response(
                    {"status": "friend request accepted"}, status=status.HTTP_200_OK
                )
            elif action == "reject":
                reject_friend_request(friend_request)
                return Response(
                    {"status": "friend request rejected"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
                )

        except FriendRequest.DoesNotExist:
            return Response(
                {"error": "Friend Request Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
