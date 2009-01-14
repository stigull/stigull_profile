#coding: utf-8

from django.contrib import admin
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from stigull_profile.models import StigullUserProfile
from stigull_profile.forms import StigullUserProfileForm

from user_profile.settings import controller
from user_profile.admin import UserWithProfileAdmin
from user_profile.models import Website
from user_profile.utils import reset_password_link

def in_stigull(user):
    """
    Usage:  in_stigull = in_stigull(user)
    After:  in_stigull is True if and only if the user is a part of the group Stigull
    """
    try:
        profile = user.get_profile()
        return profile.is_stigull()
    except StigullUserProfile.DoesNotExist:
        return False
in_stigull.short_description = _(u"Í Stigli")
in_stigull.boolean = True

def is_freshman(user):
    """
    Usage:  is_freshman = in_stigull(user)
    After:  is_freshman is True if and only if the user is a part of the group Nýnemar
    """
    try:
        profile = user.get_profile()
        return profile.is_freshman()
    except StigullUserProfile.DoesNotExist:
        return False
is_freshman.short_description = _(u"Nýnemi")
is_freshman.boolean = True


class StigullUserWithProfileAdmin(UserWithProfileAdmin):
    fieldsets = (
        (None, {'fields': ('username', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

    list_display = UserWithProfileAdmin.list_display + (in_stigull, is_freshman, reset_password_link)

controller.register(StigullUserWithProfileAdmin, StigullUserProfileForm) #Connects the StigullUserProfile with the UserProfile functionality

def save_user(sender, instance, raw, **kwargs):
    """
    Handler for a pre_save signal sent by the User model. Guarantees that the email of each user is
    username@hi.is
    """
    instance.email = u"%s@hi.is" % instance.username
signals.pre_save.connect(save_user, sender=User)

def save_user_profile(sender, instance, created, raw, **kwargs):
    """
    Handler for a post_save signal sent by the StigullUserProfile model
    On creation each StigullUserProfile gets a default homepage
       http://www.hi.is/~username
    and the password gets reset and either the user or the administrators get sent the new password
    """
    if created:
        homepage, created = Website.objects.get_or_create(url = "http://www.hi.is/~%s" % instance.user.username,
                            name = ugettext(u"Heimasvæði"))
        instance.homepages.add(homepage)
signals.post_save.connect(save_user_profile, sender = StigullUserProfile)