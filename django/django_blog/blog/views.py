from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.views import View
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from .models import Post, Comment
from .forms import RegistrationForm, SignInForm, FeedbackForm, CommentForm
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.db.models import Q
from taggit.models import Tag
from django.forms import ValidationError

class MainView(View):
    def get(self, request, *args, **kwargs):

        posts = Post.objects.order_by('created_at')

        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }

        return render(request=request, template_name='blog/index.html', context=context)
    

class PostView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        last_posts = Post.objects.order_by('-id')[:5]
        comment_form = CommentForm()
        context = {
            'post': post,
            'last_posts': last_posts,
            'comment_form': comment_form,
        }
        return render(request=request, template_name='blog/article.html', context=context)
    
    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = request.POST['text']
            username = self.request.user
            post = get_object_or_404(Post, url=slug)
            comment = Comment.objects.create(post=post, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request=request, template_name='blog/article.html', context={'comment_form': comment_form})
    

class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request=request, template_name='blog/registration.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request=request, user=user)
                return HttpResponseRedirect('/')
        return render(request=request, template_name='blog/registration.html', context={'form': form})
    

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request=request, template_name='blog/login.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                return HttpResponseRedirect('/')
            else:
                error = "Your username or password didn't match. Please try again."
        return render(request=request, template_name='blog/login.html', context={'form': form, 'error': error})
    

class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedbackForm()
        return render(request=request, template_name='blog/contact.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # name = request.POST['name']
            subject = request.POST['subject']
            message = request.POST['message']
            email = request.POST['email']
            try:
                send_mail(subject=f'From {email} | {subject}', message=message, from_email=email, recipient_list=[settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header')
            return HttpResponseRedirect('success')
        return render(request=request, template_name='blog/contact.html', context={'form': form})


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='blog/success.html')
    

class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        results = ''
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )

            paginator = Paginator(results, 4)
            page_numb = request.GET.get('page')
            page_obj = paginator.get_page(page_numb)

            return render(request=request, template_name='blog/search.html', context={
                'results': page_obj,
                'results_count': len(results),
            })
        else:
            return render(request=request, template_name='blog/search.html')
        

class TagsView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()

        paginator = Paginator(posts, 6)
        page_num = request.GET.get('page_num')
        page_obj = paginator.get_page(page_num)

        return render(request=request, template_name='blog/tag.html', context={
            'posts': page_obj,
            'common_tags': common_tags,
            'tag': tag,
        })