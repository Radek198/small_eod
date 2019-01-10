


# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


@receiver(pre_save, sender=User)
def set_group(sender, **kwargs):
    user = kwargs["instance"]
    if user.is_staff == 0:
        user.is_staff = 1


@receiver(post_save, sender=User)
def set_permissions(sender, **kwargs):
    u, created = kwargs["instance"], kwargs["created"]
    ct = ContentType.objects.get(app_label='Cases', model="Case").id
    ct1 = ContentType.objects.get(app_label='Cases', model="Letter").id

    if created and u.email.endswith('@siecobywatelska.pl'):
        permission = Permission.objects.filter(Q(content_type=ct, codename='view_case')
                                               | Q(content_type=ct1, codename='view_letter'))
        u.user_permissions.set(permission)