from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    # This will be the home page with a list of all the posts.
    # Connected to the Post model.

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # By get_queryset, we are doing a query set on our model, like sql query in python.
    # we are saying, that grab the Post model,all the objects there, filter out
    # based on these conditions, grab the published date that are less than or equal
    # to the current time, and then order them by descending order of
    # published date ('-published_date'), which means show the latest post first.
    # more info at : https://docs.djangoproject.com/en/2.0/topics/db/queries/
    # (__lte is a field condition which means 'less than or equal to')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    # When using function based views, to get automated login required functionality, we use decorators
    # When using class based views, to get automated login required functionality, we use Mixins.
    # LoginRequiredMixin are classes that we mix in to the classes we are inheriting with ie CreateView.
    # So now we can inherit methods from both of the above classes in ().
    # To create a post, login is required.
    login_url = '/login/'
    # Incase user is not logged in, where should they go....to /login/
    redirect_field_name = 'blog/post_detail.html'
    # means redirect user to the detail view.
    form_class = PostForm
    # connect the post form here.
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    # Everything same from the above class CreatePostView.


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


# CREATING A VIEW FOR UNPUBLISHED DRAFTS:
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
    # grab the Post model, all the objects there, filter out based on these conditions,
    # where the drafts doesnt have a published date ie __isnull=True.
    # and then order by created date.
    # means it lists all the drafts that have not been published yet.


##########################################################################
##########################################################################

# This def will allow us to publish a post.
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)



# This def will allow us to add a comment to a post.
@login_required
def add_comment_to_post(request, pk): #pk is the primary key which links the comment to the actual post
    post = get_object_or_404(Post, pk=pk)
    # have the post object inside this function equal to get_objects_
    # means either get the object or give 404 ie you couldnt find the object.
    # which will take in the Post model n pk=pk
    # this is required loging in, so using decorator at top @login-required
    if request.method == 'POST':
        #if the request is POST, ie someone has filled in the form and hit enter
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            # In models, Comment has attribute post which is connect with Foriegn key with Post model.
            # we are making comment.post equal to post here here.
            comment.save()
            return redirect('post_detail', pk=post.pk)
            #Once you have saved, redirect to the post_detail page
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})



# This def will allow us to approve a comment.
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    # called the approve() method in the Comment models which makes the approved_comment attribute
    # True, which was initially False by default.
    return redirect('post_detail', pk=comment.post.pk)
    # pk=comment.post.pk because the comment is linked to a particular post
    # and we have to take the pk of that particular post on which there is comment made.



# This def will allow us to remove a comment.
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
    # pk-post_pk => since after you delete the comment, comment.post.pk will not be there.
    # So we first save that post pk to a variable post_pk and later after deleting we can use that variable.














