from django.shortcuts import render ,reverse ,get_object_or_404 ,redirect
from django.urls import reverse_lazy
from  django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,FormMixin, UpdateView ,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import FormMessagesMixin
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin

from django.core.paginator import Paginator
from post import forms
from post import models
from post.models import post
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
# Create your views here.

class Home(TemplateView):
	template_name = 'base.html'


class SignupView(FormMessagesMixin,CreateView):
	template_name = 'registrations/signup.html'
	form_class = UserCreationForm
	form_valid_message = 'successfully login'
	form_invalid_message = 'something went wrong'
	success_url =reverse_lazy('home')



class PostList(ListView):
	context_data_name = 'post_list'
	template_name = 'post_list.html'
	model = models.post
	paginate_by = 5
	
	def get_queryset(self):
	    query = self.request.GET.get('q')
	    if query:
	        object_list = self.model.objects.filter(Q(title__icontains=query)|
	        	                                    Q(content__icontains=query)|
	        	                                    Q(publish__icontains=query)|
	        	                                    Q(user__username__icontains=query)
	        	                                    )
	    else:
	        object_list = self.model.objects.all().order_by('-creat_date')
	    return object_list




class PostDetail(FormMixin,DetailView):
	context_data_name  ='post_detail'
	template_name = 'post_detail.html'
	model = post
	form_class = CommentForm

	def get_success_url(self):
	    return reverse('Post:detail', kwargs={'pk' : self.kwargs.get('pk')})

	def get_context_data(self, **kwargs):
	    context = super(PostDetail, self).get_context_data(**kwargs)
	    context['form'] = CommentForm()
	    return context
	    
	def post(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    form = self.get_form()
	    if form.is_valid():
	        return self.form_valid(form)
	    else:
	        return self.form_invalid(form)

	def form_valid(self, form):
		Post = get_object_or_404(post , pk=self.kwargs.get('pk'))
		self.object = form.save(commit=False)
		self.object.post = Post
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)
  

	# def get_context_data(self, **kwargs):
	# 	content = super(PostDetail, self).get_context_data(**kwargs)
	# 	content_type = ContentType.objects.get_for_model(self.model)
	# 	post_obj = post.objects.get(pk=self.kwargs.get('pk'))
	# 	content['comment'] = Comment.objects.filter(content_type=content_type , object_id=post_obj.id)
	# 	return content





class PostCreat(FormMessagesMixin,CreateView):
	template_name='post_create.html'
	form_class = forms.PostForm
	success_url = reverse_lazy('Post:post_list')
	form_valid_message = "Blog post created!"
	form_invalid_message = " Failed to Blog post created!"

	def form_valid(self, form):
	    self.object = form.save(commit=False)
	    self.object.user = self.request.user
	    self.object.save()
	    return super().form_valid(form)


class PostUpdate(FormMessagesMixin,UpdateView):
	template_name = 'post_update.html'
	model = models.post
	fields = ['title','content','image']
	success_url = reverse_lazy('Post:post_list')
	form_valid_message = "Updated post successfully"
	form_invalid_message = "Unable to update post"
	
class PostDelete(SuccessMessageMixin,DeleteView):
	template_name = 'post_delete.html'
	model = models.post
	success_url = reverse_lazy('Post:post_list')
	success_message = "Post successfully deleted"

	def delete(self, request, *args, **kwargs):
	    messages.success(self.request, self.success_message)
	    return super(PostDelete, self).delete(request, *args, **kwargs)


def publish_post(request, pk):
	Post = get_object_or_404(models.post, pk=pk)
	Post.post_publish()
	return redirect('Post:post_list')
