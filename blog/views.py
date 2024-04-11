from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post, Review
from django.urls import reverse
from .forms import ReviewForm, CommentForm
from django.views import View
from django.views.generic import ListView
from django.shortcuts import redirect

# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"



class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
    

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context) 
    

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")




# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST, initial={'post': identified_post})
#         if form.is_valid():
#             review = form.save()
#             review.identified_post = identified_post
#             review.save()
#             return redirect('post-detail-page', slug=slug)

#     else:
#         form = ReviewForm(initial={'post': identified_post})

#     review_card = Review.objects.filter(
#         identified_post=identified_post).order_by('-date')
#     return render(request, "blog/post-detail.html", {'post': identified_post, "tags": identified_post.tags.all(), "form": form, "review_card": review_card})
