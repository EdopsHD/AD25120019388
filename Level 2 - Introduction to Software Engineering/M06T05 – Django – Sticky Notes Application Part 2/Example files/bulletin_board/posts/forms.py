# posts/forms.py
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post objects.

    Fields:
    - title: CharField for the post title.
    - content: TextField for the post content.

    Meta class:
    - Defines the model to use (Post) and the fields to include in the form.

    :param forms.ModelForm: Django's ModelForm class.
    """

    class Meta:
        model = Post
        fields = ["title", "content", "author"]