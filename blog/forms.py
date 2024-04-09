from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(label='Your Rating', min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['user_name', 'review_text', 'rating']
        # exclude = ['identified_post']
        # fields = ['user_name', 'review_text', 'rating']
        labels = {
            "user_name": "User Name",
            "review_text": "Your Feedback",
            "rating": "Your Rating",
        }

        error_messages = {
            "user_name": {
                "required": "Your name must not be empty",
                "max_length": "Please enter a shorter name",
                "min_length": "Please enter a longer feedback"
            }

        }

class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(label='Your Rating', min_value=1, max_value=5)
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "text": "Your Feedback",
        }
