from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.api_views import (
    ListFriendsApiView,
    ListPendingFirendRequest,
    RespondFriendRequestView,
    SendFriendRequestAPIView,
    UserRegisterAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path(
        "send-friend-request/",
        SendFriendRequestAPIView.as_view(),
        name="send-friend-request",
    ),
    path(
        "respond-friend-request/",
        RespondFriendRequestView.as_view(),
        name="respond-friend-request",
    ),
    path("list-friends/", ListFriendsApiView.as_view(), name="list-friends"),
    path(
        "list-pending-request/",
        ListPendingFirendRequest.as_view(),
        name="list-pending-request",
    ),
]
