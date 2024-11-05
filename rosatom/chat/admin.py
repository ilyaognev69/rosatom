from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Channel, Message
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields':('is_moderator',)}),
	)
	list_display = ('username', 'email', 'is_staff', 'is_moderator')
	list_filter = ('is_staff', 'is_moderator')
	
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
	list_display = ('name', )
	search_fields = ('name', )
	filter_horizontal = ('participants', 'blocked_users')
	
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('channel', 'user', 'timestamp', 'content')
	list_filter = ('channel', 'user')
	search_fields = ('content',)
	date_hierarchy = 'timestamp'