#coding: utf-8

from stigull_profile.models import StigullUserProfile

from user_profile.forms import UserProfileForm

class StigullUserProfileForm(UserProfileForm):
    model = StigullUserProfile
    
    