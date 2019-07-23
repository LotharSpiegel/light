from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


User = settings.AUTH_USER_MODEL


# class MemberGroup(models.Model):
# 	pass


class MemberProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	slug = models.SlugField(max_length=50, unique=True)
	website = models.URLField(blank=True)
	about = models.TextField(blank=True)

	def __str__(self):
		return self.user.get_username()

	def get_absolute_url(self):
		return reverse('accounts:profile_view', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('accounts:profile_update')
		#reverse('accounts:profile_update')

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	# MemberProfile.objects.update_or_create(
	# 	defaults={
	# 		'slug': slugify(user.get_username())
	# 	},
	# 	user=in
	# )
    if created:
    	MemberProfile.objects.create(user=instance)
    	#MemberProfile.objects.update_or_create(
		# 	user=user,
		# 	defaults={
		# 		'slug': slugify(user.get_username()),
		# 	}
		# )
    instance.profile.save() # needed?

@receiver(pre_save, sender=MemberProfile)
def pre_save_profile_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.user.get_username())

#pre_save.connect(pre_save_category_receiver, sender=Category)


# # basically, we never need to address the Profile model
# # e.g. save it, but do as usual everything through the User model
