from django.urls import path
from blog.views import MainView, PostView, RegistrationView, SignInView, FeedBackView, SuccessView, SearchResultsView, TagsView
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/', PostView.as_view(), name='article'),
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('tag/<slug>', TagsView.as_view(), name="tag"),
]