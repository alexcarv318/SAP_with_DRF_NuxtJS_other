from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from .models import Post

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
