from django.contrib import admin
from .models import Post, Author, Tag, Review, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date")
    list_display = ("title", "author", "date")
    prepopulated_fields = {"slug": ("title",)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'review_text', 'rating', 'identified_post', 'date')

    def save_model(self, request, obj, form, change):
        obj.identified_post = Post.objects.get(slug=form.cleaned_data['post'])
        obj.save()


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'text', 'rating', 'post')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Review, ReviewAdmin)


