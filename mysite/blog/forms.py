from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        # Connects to Post model
        fields = ('author', 'title', 'text')
        # Enter the fields of the Post model that we want to edit
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
        # connect specific widgets to CSS styling.
        # create a widgets attribute which is a dictionary, where 1st key is a field ie here it is 'title'.
        # TextInput and Textarea is the widgets actual name
        # attrs stands for attributes which equals to a sub-dictionary of class
        # where 'textinputclass' and postcontent' are our own class names, which go in our css file.
        # 'text' is connected to 3 css classes : 1st is 'editable', which means we can edit it.
        # 2nd is 'medium-editor-textarea', which gives the styling of the medium editor
        # 3rd is postcontent, which is our own class




class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        # Connects to Comment model
        fields = ('author', 'text')
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
        # author has the same class as title in the post formmodel, so both will have the same css styling.
        # here the 'text' has only the default css editor medium class, and 'postcontent' is only kept
        # for 'text' of the Post form
