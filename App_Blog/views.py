from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from App_Blog.models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid #unique id generate
from App_Blog.forms import CommentForm
from django.core.paginator import Paginator


#after using paginator
def home(request):
    blog_list = Blog.objects.order_by('-publish_date')
    paginator = Paginator(blog_list, 4)  # Display 3 blogs per page
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {'blogs': blogs}
    return render(request, 'App_Blog/home.html', context)

#BLOG LIST
class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')

# BLOG CREATE
class CreateBlog(CreateView, LoginRequiredMixin):
    model = Blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    # non mentioned items generate
    def form_valid(self,form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(' ', '-') + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('App_Blog:home'))

#BLOG DETAILS
@login_required
def blog_details(request,slug):
    blog = Blog.objects.get(slug=slug)  #// my slug = published slug
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user #comment form user
            comment.blog = blog #this blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':slug} ))

    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form, 'liked':liked})



#LIKED
@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user) #new object create
        liked_post.save()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug} ))

#UNLIKED
@login_required
def unliked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug} ))


#MY BLOGS
class MyBlogs(LoginRequiredMixin,TemplateView):
    # context_object_name= 'myblogs'
    template_name = "App_Blog/my_blogs.html"
    
class UpdateBlog(LoginRequiredMixin, UpdateView):
    model= Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name= 'App_Blog/edit_blog.html'
    
    def get_success_url(self, **kwargs):
           return reverse_lazy('App_Blog:blog_details', kwargs={'slug':self.object.slug})

def contact(request):
    return render(request, 'App_Blog/contact.html', context={})    