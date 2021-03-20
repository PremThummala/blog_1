from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import EmailForm, CommentForm
from django.core.mail import send_mail

# Create your views here.
def list_view(request, tag_slug = None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'post_list': post_list, 'tag':tag})

def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post, status = 'published', publish__year = year, publish__month = month, publish__day = day)
    comments = post.comments.filter(active = True)
    csubmit = False
    if request.method== "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form':form, 'csubmit': csubmit, 'comments':comments})

def post_email_view(request, id):
    post = get_object_or_404(Post, id=id, status ="published")
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            send_mail = ('subject','message', 'prem@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/sharebymail.html', {'form': form, 'post':post, 'sent': sent} )
