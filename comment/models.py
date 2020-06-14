from django.db import models
from post.models import post
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# Create your models here.

class Comment(models.Model):
	post = models.ForeignKey(post, on_delete=models.CASCADE ,null=True ,related_name="comments")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')

	content = models.TextField(null=True ,blank=True)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-pk']


	def __str__(self):
		return self.user.username

	# def get_absolute_url(self):
	#     return reverse("Post:detail", kwargs={"pk": self.pk})  
