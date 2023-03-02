from django.shortcuts import render,redirect, get_object_or_404
from .models import Blog,BlogHeshtags,Comment_user
from users.models import CustomUser
from django.views.generic import DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from .forms import CreatePost, RelatedHashtags,Comment_form
from django.views.generic.edit import FormMixin
from django.urls import reverse
import datetime

COMENT = 1
PUBLICATION = 2
dt = datetime.datetime.now()

#Главная страница
class Home(ListView):
    model=Blog
    template_name ='navigation/home.html'
    context_object_name='DataBase'
    
    def get_queryset(self):
        return Blog.objects.values('blog_title','img','id').order_by('-date_public')[7:]
    
    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context['Shield'] = Blog.objects.values('blog_title','img','id').order_by('-date_public')[:7]
        return context
#Фильтр новостей по датам   
def news(request):
    DataBaseNWdate = Blog.objects.dates('date_public','day').values('date_public')
    AllNews = Blog.objects.all().values('blog_title','date_public')
    return render(request,'navigation/news.html',{'DataBaseNW':DataBaseNWdate,'AllNews':AllNews})

def filter_date(request):
    dateFilter = request.GET['filter']
    Date = Blog.objects.values('blog_title','date_public').filter(date_public__date=dateFilter)
    DataBaseNW = Blog.objects.dates('date_public', 'day').values('date_public')
    return render(request,'navigation/filter_date.html',{"Date":Date,'DataBaseNW':DataBaseNW,'dataFilter':dateFilter})


def filter_tag(request):
    tag = request.GET['tag']
    alltag = BlogHeshtags.objects.filter(hashtag=tag)
    return render(request,'navigation/tags.html',{"alltag":alltag,'tag':tag})

#Страничка с тегом "интервью"
class Interview(ListView):
    model=Blog
    template_name ='navigation/interview.html'
    context_object_name='interview'
    
    def get_queryset(self):
        return Blog.objects.filter(type="Интервью").values('blog_title','img')
#Страничка с тегом "Публикации"
class Public(ListView):
    model=Blog
    template_name ='navigation/public.html'
    context_object_name='blogDB'
    
    def get_queryset(self):
        return Blog.objects.filter(type='Публикация').values('blog_title','img')
#Страничка с тегом "Блог"
class BlogView(ListView):
    model=Blog
    template_name ='navigation/blog.html'
    context_object_name='posts'
    
    def get_queryset(self):
        return Blog.objects.filter(type="Блог").values('blog_title','img')
    
class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'navigation/user.html'
    context_object_name ='userinfo'
    def get_success_url(self):
        return reverse('user', kwargs={'pk': self.object.id})
    
    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment_user.objects.select_related('post').filter(user=self.kwargs['pk'])
        return context

#фун-ия создания поста
def create_post(request):
    login_user = request.user
    if request.method == 'POST':
        hashtag_form = RelatedHashtags(request.POST)
        post_form = CreatePost(request.POST, request.FILES)
        if post_form.is_valid() and hashtag_form.is_valid():
            post = post_form.save()
            hashtag = hashtag_form.cleaned_data.get('hashtag')
            post.date_public = dt.isoformat()
            post.author = request.user
            post.type = request.POST.get('type')
            print(request.POST.get('type'))
            for el in hashtag.split(','):
                sl_hashtag = RelatedHashtags(request.POST)
                i=sl_hashtag.save()
                i.blog_id=post.id
                i.hashtag = el
                i.save()
            post.save()
            login_user.reputation += PUBLICATION
            login_user.save()
            return redirect('home')
    else:
        hashtag_form = RelatedHashtags()
        post_form = CreatePost()
    context = {'post_form':post_form,
               'hashtag_form':hashtag_form}
    return render(request,'navigation/create_post.html',context)

#Просмотр поста
class Show_post(FormMixin,DetailView):
    model = Blog
    template_name = 'navigation/post.html'
    context_object_name = 'BlogDB'
    form_class = Comment_form

    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.object.id})

    def get_queryset(self):
        queryset = Blog.objects.select_related('author').filter(pk=self.kwargs['pk'])
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtags_list'] = BlogHeshtags.objects.filter(blog_id=self.kwargs['pk'])
        context['comment_list']= Comment_user.objects.select_related('user').filter(post_id = self.kwargs['pk'])
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form,request)
        else:
            return self.form_invalid(form)
        

    def form_valid(self,form,request,**kwargs):
        login_user = request.user
        comment_form = form.save(commit=False)
        comment_form.post = self.get_object()
        comment_form.date_time = dt.isoformat()
        comment_form.user = request.user
        login_user.reputation += COMENT
        login_user.save()
        comment_form.save()
        return super(Show_post,self).form_valid(comment_form)
    
    def form_invalid(self, form):
        return super(Show_post,self).form_invalid(form)

#добавления лайков
class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Blog.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True
                break


        if is_dislike:
            post.dislike.remove(request.user)

        is_like = False

        for like in post.like.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.like.add(request.user)

        if is_like:
            post.like.remove(request.user)

        return HttpResponseRedirect(reverse('show_post', args=[str(pk)]))



class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Blog.objects.get(pk=pk)

        is_like = False

        for like in post.like.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.like.remove(request.user)



        is_dislike = False

        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislike.add(request.user)

        if is_dislike:
            post.dislike.remove(request.user)

        return HttpResponseRedirect(reverse('show_post', args=[str(pk)]))

class AddLikeComment(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        comment = Comment_user.objects.get(pk=pk)
        is_like = False
        for like in comment.like.all():
            if like == request.user:
                is_like=True
                break

        if not is_like:
            comment.like.add(request.user)

        if is_like:
            comment.like.remove(request.user)
        
        return HttpResponseRedirect(reverse('show_post',args=[str(comment.post_id)]))