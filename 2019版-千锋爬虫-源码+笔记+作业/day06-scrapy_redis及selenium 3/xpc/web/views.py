from web.models import Post
from django.shortcuts import render



def show_list(request):
    posts = Post.objects.order_by('-like_counts')[:24]
    return render(request, 'posts.html', locals())