from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    # This is a single-user application
    # Linking author to authorisation User,
    # So when creating superuser, that will be someone who can author new post.
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # SETTING A PUBLICATION DATE METHOD, WHEN THE POST IS ACTUALLY BEING PUBLISHED.
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
        # Eventually we'll be having a list of comments,
        # some approved and some not.
        # In this method, we grab those comments and filter them by saying,
        # is this a truely approved comment and show them along the post.

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})
    # After you create a post, go to the post_detail page matching the primary key(pk)
    # of the post you just created.

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    # above line connects each comment to the blog application post.
    author =models.CharField(max_length=200)
    # Note that above author is not the same as author in class Post.
    # this author is the name of any person writing a comment.
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    # this approved_comment should be the same name as
    # (approved_comment=True) ....as in the function approved_comments above.


    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")
    # after you write in the comment, go to the list of all the posts.
    # post_list will be the home page with the list of all the posts.
    # depends on you, where you want to take it to.

    def __str__(self):
        return self.text