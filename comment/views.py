from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from comment.models import Comment
from post.models import post
# Create your views here.

class CreateComment(CreateView):
	template_name = 'comments/add_comment.html'
	model = Comment 
	fields=['content']
	queryset = Comment.objects.all().order_by('-id')

	def get_success_url(self):
	    return reverse('Post:detail', kwargs={'pk' : self.kwargs.get('pk')})

	def form_valid(self, form):
		Post = get_object_or_404(post , pk=self.kwargs.get('pk'))
		self.object = form.save(commit=False)
		self.object.post = Post
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

	



