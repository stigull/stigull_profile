#coding: utf-8
from django.db.models import signals
from django.contrib.auth.models import Group
from django.utils.translation import ugettext, ugettext_lazy as _

import user_profile
from user_profile.models import UserProfile

STIGULL_GROUP = u"Stigull"
GOVERNMENT_GROUP = u"Stjórn"
FRESHMEN_GROUP = u"Nýnemar"
MATH_GROUP = u'Stærðfræðinemar'
PHYSICS_GROUP = u'Eðlisfræðinemar'

class StigullUserProfile(UserProfile):
    def is_stigull(self):
        """
        Usage:  is_stigull = user.get_profile().is_stigull()
        After:  is_stigull is True if and only if user is a part of Stigull
        """
        return self.user.groups.filter(name = STIGULL_GROUP).count() == 1
    
    def is_freshman(self):
        """
        Usage:  is_freshman = user.get_profile().is_freshman()
        After:  is_frashman is True if and only if the user is a freshman
        """
        return self.user.groups.filter(name = FRESHMEN_GROUP).count() == 1
    
    def in_government(self):
        """
        Usage:  in_government = user.get_profile().in_government()
        After:  in_government is True if and only if the user is a part of the student government
        """
        return self.user.groups.filter(name = GOVERNMENT_GROUP).count() == 1
    
    def has_roles(self):
        """
        Usage:  has_roles = user.get_profile.has_roles()
        After:  has_roles is True if and only if the user occupies some roles
        """
        return self.user.roles.count() > 0
    
    def get_roles(self):
        """
        Usage:  roles = user.get_profile().roles
        After:  roles is a list of the roles of the user
        """
        return [ user_in_role.role for user_in_role in self.user.roles.select_related().all() ]
    roles = property(get_roles)
        
    
    def get_department(self):
        """
        Usage:  department_description = user.get_profile.get_department()
        After:  department_description is a human readable description of the deparment of the user
        """
        is_freshman = self.is_freshman()
        if self.user.groups.filter(name = MATH_GROUP).count() > 0:
            if is_freshman:
                return _(u"Stærðfræðinýnemi")
            else:
                return _(u"Stærðfræðinemi")
        elif self.user.groups.filter(name = PHYSICS_GROUP).count() > 0:
            if is_freshman:
                return _(u"Eðlisfræðinýnemi")
            else:            
                return _(u"Eðlisfræðinemi")
        else:
            return u""
        
    

def create_groups(**kwargs):
    groupnames = [STIGULL_GROUP, GOVERNMENT_GROUP, FRESHMEN_GROUP, MATH_GROUP, PHYSICS_GROUP]
    for groupname in groupnames:
        group, created = Group.objects.get_or_create(name = groupname)
    
signals.post_syncdb.connect(create_groups)