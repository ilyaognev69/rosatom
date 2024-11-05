from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Channel, CustomUser, Message
from .permissions import IsModerator
from .serializers import RegisterSerializer, MessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class RegisterView(generics.CreateAPIView):
	serializer_class = RegisterSerializer
	permission_classes = [AllowAny]
	
class BlockUserView(APIView):
	permission_classes = [IsAuthenticated, IsModerator]
	
	def post(self, request, channel_id, user_id):
		try:
			channel = Channel.objects.get(id=channel_id)
			user_to_block = CustomUser.objects.get(id=user_id)
			
			channel.blocked_users.add(user_to_block)
			return Response({"status": "User blocked"}, status=status.HTTP_200_OK)
		except Channel.DoesNotExist:
			return Response({"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)
		except CustomUser.DoesNotExist:
			return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
	
class UnblockUserView(APIView):
	permission_classes = [IsAuthenticated, IsModerator]
	
	def post(self, request, channel_id, user_id):
		try:
			channel = Channel.objects.get(id=channel_id)
			user_to_unblock = CustomUser.objects.get(id=user_id)
			
			channel.blocked_users.remove(user_to_unblock)
			return Response({"status": "User unblocked"}, status=status.HTTP_200_OK)
		except Channel.DoesNotExist:
			return Response({"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)
		except CustomUser.DoesNotExist:
			return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
		
class MessageHistoryView(generics.ListAPIView):
	serializer_class = MessageSerializer
	permission_classes = [IsAuthenticated]
	
	def get_queryset(self):
		channel_name = self.kwargs['channel_name']
		try:
			channel = Channel.objects.get(name=channel_name)
			return Message.objects.filter(channel=channel).order_by('timestamp')
		except Channel.DoesNotExist:
			return Message.objects.none()