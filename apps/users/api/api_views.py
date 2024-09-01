from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.users.api.service import (
    accept_friend_request,
    reject_friend_request,
    send_friend_request,
)
from apps.users.models import FriendRequest, FriendRequestStatus, User
from apps.users.serializers import (
    FriendRequestSerializer,
    FriendSerializer,
    UserRegisterSerializers,
    UserSerializer,
)


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
                response = accept_friend_request(request.user, friend_request)
                return response
            elif action == "reject":
                response = reject_friend_request(request.user, friend_request)
                return response
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


class ListFriendsApiView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer

    def get(self, request, *args, **kwargs):
        try:
            friends = request.user.friends.all()

            data = self.serializer_class(friends, many=True).data
            return Response(data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListPendingFirendRequest(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get(self, request, *args, **kwargs):
        try:
            pending_request = FriendRequest.objects.filter(
                receiver=request.user, status=FriendRequestStatus.PENDING
            ).all()
            data = self.serializer_class(pending_request, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SearchUserAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        try:
            search_by = request.query_params.get("search_by", None)
            query = User.objects.filter(is_delete=False, is_active=True)
            if search_by:
                if "@" in search_by:
                    query = query.filter(email__iexact=search_by.lower())
                else:
                    query = query.filter(first_name__icontains=search_by)
            paginator = self.pagination_class()
            users = paginator.paginate_queryset(query, request)
            data = self.serializer_class(users, many=True).data
            return paginator.get_paginated_response(data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
