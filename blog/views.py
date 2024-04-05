from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post, Review
from .forms import ReviewForm
from django.views import View
from django.shortcuts import redirect

# Create your views here.


class Starting_pageView(View):
    def get(self, request):
        latest_posts = Post.objects.all().order_by('-created_at')[:3]

        return render(request, "blog/index.html", {'posts': latest_posts})


def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, "blog/all-posts.html", {'all_posts': all_posts})


def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST, initial={'post': identified_post})
        if form.is_valid():
            review = form.save()
            review.identified_post = identified_post
            review.save()
            return redirect('post-detail-page', slug=slug)

    else:
        form = ReviewForm(initial={'post': identified_post})

    review_card = Review.objects.filter(
        identified_post=identified_post).order_by('-date')
    return render(request, "blog/post-detail.html", {'post': identified_post, "tags": identified_post.tags.all(), "form": form, "review_card": review_card})
