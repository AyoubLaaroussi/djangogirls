from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView



class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='login')


class PostListView(ListView):

    context_object_name = 'posts'

    def get_queryset(self):
        queryset =  Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return queryset
    

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('created_date')
        context['form'] = CommentForm
        return context
        
    def post(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
            post = self.get_object()
            if form.is_valid() :
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()  
                
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')   
        
   
class PostCreate(CreateView):
    model = Post
    fields = ['title','text']
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        post = form.instance
        post.published_date = timezone.now()
        post.author = self.request.user
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail',kwargs={'pk':self.object.pk})

class PostEdit(UpdateView):
    model = Post
    fields = ['title','text']
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse('post_detail',kwargs={'pk':self.object.pk})

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post_list')

def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.like()
    return redirect('post_detail', pk=comment.post.pk)

def comment_dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.dislike()
    return redirect('post_detail', pk=comment.post.pk)



#def post_list(request):
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #import ipdb; ipdb.set_trace()
#    return render(request, 'blog/post_list.html', {'posts': posts})

# def post_detail(request, pk): 
#     post = get_object_or_404(Post, pk=pk) 
#     comments = Comment.objects.filter(post=post).order_by('created_date')

#     if request.method == "POST":
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             if request.user.is_authenticated():
#                 comment = form.save(commit=False)
#                 comment.author = request.user
#                 comment.post = post
#                 comment.save()  
#                 return redirect('post_detail', pk=post.pk)
#             else:
#                 return redirect('login')   
#         return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()

#     return render(request, 'blog/post_detail.html', {'post': post, 'comments':comments,'form':form})

# @login_required(login_url='login')
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)

#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.publish()
            
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

# @login_required(login_url='login')
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

# @login_required(login_url='login')
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     return redirect('post_list')