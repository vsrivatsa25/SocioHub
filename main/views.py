from django.views.generic import TemplateView, DetailView, FormView, View, ListView
from django.contrib.auth.models import User
from .models import Post
from django.contrib import messages
from .models import Post, UserInterests, ProfilePic, Like, Comment, Friend
from .forms import PostForm, ProfilePictureForm, InterestForm, LikeSubmit, CommentSubmit
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from .filtering import content_check
import datetime

class Liked(LoginRequiredMixin,TemplateView):
    model = Post
    template_name = 'main/liked.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['object_list'] = Post.objects.all()
        context['liked_list'] = Like.objects.filter(user_id=self.request.user.id).order_by('-id')
        context['profilepics'] = ProfilePic.objects.all()
        context['comments_list'] = Comment.objects.all()
        context['users'] = User.objects.all()

        return context

class Follow(LoginRequiredMixin,TemplateView):
    template_name = 'main/follow.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('userid')
        model = Friend(user1=self.request.user,user2=query,accepted=1,time=datetime.datetime.now())
        if not Friend.objects.filter(user1=self.request.user,user2=query,accepted=1).count():
            model.save()
            messages.success(self.request,'User has been followed.')
            redirect('index')
        else:
            messages.warning(self.request,'User already followed')
            redirect('index')
        if self.request.method=='POST':
            redirect('index')

class FriendList(LoginRequiredMixin,TemplateView):
    model = Friend
    template_name = 'main/friends.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['following_list'] = Friend.objects.filter(user1=self.request.user.id)
        context['follower_list'] = Friend.objects.filter(user2=self.request.user.id)
        context['users'] = User.objects.all()
        context['profilepics'] = ProfilePic.objects.all()
        return context


class SearchPage(TemplateView):
    model = Post
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('search')
        context = {}
        context['all_posts'] = Post.objects.all().order_by('-id')
        context['object_list'] = Post.objects.filter(Q(text__icontains=query)).order_by('-id')
        context['location_list'] = Post.objects.filter(Q(location__icontains=query)).order_by('-id')
        context['profile_list'] = User.objects.filter(Q(first_name__icontains=query) or Q(last_name__icontains=query) or Q(username__icontains=query))
        context['profilepics'] = ProfilePic.objects.all()
        context['users'] = User.objects.all()
        context['comments_list'] = Comment.objects.all().order_by('-id')
        return context


class IndexPageView(View):
    template_name = 'main/index.html'
    form_class1 = LikeSubmit
    form_class2 = CommentSubmit

    def get(self, request):
        like_form = self.form_class1(None)
        comment_form = self.form_class2(None)
        context = {}
        context['user_count'] = User.objects.all().count()
        context['myinterests'] = UserInterests.objects.filter(user_id=self.request.user.id).values('interest')
        context['recommended'] = UserInterests.objects.filter(interest__in=context['myinterests']).filter(~Q(user_id=self.request.user.id)).values('user_id','interest')[:5]
        context['recommendedusers'] = User.objects.filter(id__in=context['recommended'].values('user_id')).order_by('?')
        context['post_count'] = Post.objects.all().count()
        context['comments'] = Comment.objects.all()
        context['connections'] = Friend.objects.all().count()
        context['users'] = User.objects.all()
        context['following'] = Friend.objects.filter(user1=self.request.user.id).values('user2')
        context['profilepics'] = ProfilePic.objects.all()
        context['myprofilepic'] = ProfilePic.objects.filter(user_id=self.request.user.id)
        context['userinterests'] = UserInterests.objects.all()
        context['posts'] = Post.objects.filter(Q(user_id__in=context['following']) | Q(user_id=self.request.user.id)).order_by('-time')[:30]
        return render(request, self.template_name, {'like_form': like_form, 'comment_form': comment_form,'context':context})


    def post(self, request):
        if self.request.method == 'POST':
            form1 = self.form_class1(request.POST)
            form2 = self.form_class2(request.POST)
            try:
                newform = form2.save(commit=False)
                check = content_check(newform.text)
                if not check:
                    newform.user_id = request.user.id
                    newform.time = datetime.datetime.now()
                    newform.save()
                else:
                    messages.warning(request,check)
                return redirect('index')
            except:
                newform = form1.save(commit=False)
                newform.user_id = request.user.id
                if not Like.objects.filter(user_id=request.user.id).filter(post_id=newform.post_id):
                    newform.save()
                return redirect('index')

def post_image(LoginRequiredMixin,request):
    if request.method == 'GET':
        context = {}
        context['interests'] = UserInterests.objects.filter(user_id=request.user.id)
        context['profilepics'] = ProfilePic.objects.filter(user_id=request.user.id)

        return render(request, 'main/addPost.html', {'context': context})

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)


        if form.is_valid():
            newform = form.save(commit=False)
            newform.user_id = request.user.id
            newform.time = datetime.datetime.now()
            check = content_check(newform.text)
            if not check:
                newform.save()
                messages.success(request,'Your post has been uploaded successfully.')
            else:
                messages.warning(request,check)
            return redirect('index')
    else:
        form = PostForm()
    messages.warning(request,'Please Complete all fields')
    return render(request, 'main/addPost.html', {'form': form})

def post_interest(LoginRequiredMixin,request):
    if request.method == 'GET':
        context = {}
        context['interests'] = UserInterests.objects.filter(user_id=request.user.id).order_by('interest')
        context['trending'] = UserInterests.objects.all().order_by('-id').values('interest').distinct()[:10]
        context['profilepics'] = ProfilePic.objects.filter(user_id=request.user.id)
        return render(request, 'main/addInterest.html', {'context': context})

    if request.method == 'POST':
        form = InterestForm(request.POST, request.FILES)

        if form.is_valid():
            newform = form.save(commit=False)
            newform.user_id = request.user.id
            newform.save()
            messages.success(request,'Interest Added')
            return redirect('interests')
        else:
            messages.warning(request,'Invalid Input')
            return redirect('interests')
    else:
        form = InterestForm()
    return render(request, 'main/addInterest.html', {'form': form})

def profile_picture(LoginRequiredMixin,request):
    if request.method == 'GET':
        context2 = {}
        context2['existing'] = ProfilePic.objects.all()
        return render(request, 'main/profilepicture.html', {'context': context2})

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.user_id = request.user.id
            newform.time = datetime.datetime.now()
            old = ProfilePic.objects.filter(user_id=request.user.id)
            old.delete()
            newform.save()
            return redirect('index')
    else:
        form = ProfilePictureForm()
    return render(request, 'main/profilepicture.html', {'form': form})

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
