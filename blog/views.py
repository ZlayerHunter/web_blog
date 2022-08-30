from email import contentmanager
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from glava1.settings import EMAIL_HOST_USER
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from haystack.query import SearchQuerySet

def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(status='published')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    #object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,""
                   'posts': posts,
                   'tag': tag,
                   })

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    #object_list = Post.objects.filter(status='published')
    similar_posts = Post.objects.filter(status='published').filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                 {'post': post,
                  'comments': comments,
                  'comment_form': comment_form,
                  'similar_posts': similar_posts})

class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, str(EMAIL_HOST_USER), [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
    
class PostAdd(CreateView):
    model = Post
    fields = ["title", "slug", "author", "body", "publish", "status", "tags"]
    
def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
    #if request.GET['query']:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            #C:\Users\Slaye\AppData\Local\Programs\Python\Python310\Lib\site-packages\haystack\backends\solr_backend.py
            # 541 app_label, model_name = raw_result[DJANGO_CT][0].split(".")
            # 584 result = result_class(app_label, model_name, raw_result[DJANGO_ID][0], raw_result['score'], **additional_fields)
            # count total results
            total_results = results.count()
        return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results})
    return render(request, 'blog/post/search.html', {'form': form})
