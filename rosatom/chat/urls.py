from django.urls import path
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
)
from .views import RegisterView, BlockUserView, UnblockUserView, MessageHistoryView

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('channels/<int:channel_id>/block/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
	path('channels/<int:channel_id>/unblock/<int:user_id>/', UnblockUserView.as_view(), name="unblock_user"),
	path('channels/<str:channel_name>/history/', MessageHistoryView.as_view(), name='message_history')
]