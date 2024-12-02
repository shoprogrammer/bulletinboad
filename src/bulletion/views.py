from django.shortcuts import render,redirect,get_object_or_404
from .forms import BoardForm,SignUpForm,CommentForm,FavoriteForm,ContactForm
from .models import BoardModel,Comment,Favorite
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.db.models import Count
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

def user_owns_boards(view_func):
    @wraps(view_func)
    def wrapper(request,pk):
        board = get_object_or_404(BoardModel,pk=pk)
        if board.user == request.user:
            return view_func(request,pk)
        else:
            return redirect('board-list')
    return wrapper









def listboard(request):
    template_name = "bulletion/board-list.html"
    user = request.user
    if user.is_authenticated:
        obj_query = BoardModel.objects.annotate(is_favorite=Count('favorite',filter=models.Q(favorite__user=user))).order_by('-update_at')
    else:
        obj_query = BoardModel.objects.all().order_by('-update_at')

    paginator = Paginator(obj_query,3)
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)

    ctx={}
    ctx["object"]=obj
   
    return render(request,template_name,ctx)







@login_required
def createboard(request):
    template_name = "bulletion/board-create.html"

   
   
    if request.POST:
        form = BoardForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request,"掲示板の投稿に成功しました.")
            return redirect('board-list')
        else:
            messages.error(request,'掲示板の投稿に失敗しました.')

    else:
        form = BoardForm(request.POST)
          
    return render(request,template_name,{'form':form})

@login_required
@user_owns_boards
def detailboard(request,pk):
    template_name='bulletion/board-detail.html'
    obj=BoardModel.objects.get(pk=pk)
    comments = Comment.objects.filter(board = pk).order_by('-created_at')
    comment_form = CommentForm()
    ctx={}
    ctx["object"]=obj
    ctx["comment_form"]=comment_form
    ctx["comments"]=comments
    return render(request,template_name,ctx)

@login_required
@user_owns_boards
def updateboard(request,pk):
    template_name="bulletion/board-edit.html"
    obj=BoardModel.objects.get(pk=pk)

    if request.POST:
        form = BoardForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('board-list')
    else:
        form = BoardForm(instance=obj)
    
    return render(request,template_name,{'form':form,'object':obj})

@login_required
@user_owns_boards
def deleteboard(request,pk):
    obj=BoardModel.objects.get(pk=pk)
    if request.POST:
        obj.delete()
        return redirect('board-list')
    
    return redirect('board-list')

@login_required
def my_boards(request):
    
    user = request.user
    boards = user.boards.all()
    return render(request,"bulletion/my_boards.html",{'boards':boards})

@login_required
def comment_create(request,pk):
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.board_id = pk
            comment_form.save()


           

            
    return redirect('board-detail',pk=pk)

@login_required
def comment_delete(request,board_pk,comment_pk):
    comment = get_object_or_404(Comment,pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('board-detail',pk=board_pk)


def board_search(request):
    template_name='bulletion/board-list.html'
    
    query = request.GET.get('query')
    search_type = request.GET.get('search_type')
    boards = BoardModel.objects.all()

    if search_type == 'partial':
        boards = boards.filter(title__icontains = query)
    elif search_type == 'prefix':
        boards = boards.filter(title__startswith = query)

    elif search_type == 'suffix':
        boards = boards.filter(title__endswith = query)

    else:
        boards = boards.filter(title__icontains = query)

    return render(request,template_name,{'object':boards})

def board_sort(request):
    template_name = 'bulletion/board-list.html'
    sort_by = request.GET.get('sort')
    direction = request.GET.get('direction')

    if direction == 'asc':
        next_direction = 'desc'
    else:
        next_direction = 'asc'

    if sort_by:
        if direction == 'desc':
            boards = BoardModel.objects.all().order_by(f'-{sort_by}')
        else:
            boards = BoardModel.objects.all().order_by(sort_by)
    else:
        boards = BoardModel.objects.all()
    
    ctx = {
        'object':boards,
        'sort_by':sort_by,
        'direction':direction,
        'next_direction':next_direction,

    }

    return render(request,template_name,ctx)

@login_required
def add_favorite(request):
    if request.method == 'POST':
        form = FavoriteForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('board-list')
    return redirect('board-list')
@login_required
def remove_favorite(request):
    if request.POST:
        favorite = Favorite.objects.get(user=request.user,board=request.POST.get('board'))
        favorite.delete()
        return redirect('board-list')
    return redirect('board-list')




def contact(request):
    template_name = 'bulletion/contact.html'
    
    ctx = {}
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            #ユーザーへのメール
            user_subject = 'お問い合わせを受け付けました'
            user_message = 'お問い合わせ内容:¥n¥n{}'.format(contact.message)
            send_mail(user_subject,user_message,settings.EMAIL_HOST_USER,[contact.email])
            return redirect('contact_success')
    else:
        form = ContactForm()

    ctx['form'] = form
    return render(request,template_name,ctx)
    

def contact_success(request):
    template_name = 'bulletion/contact_success.html'
    return render(request,template_name)






def contact_success(request):
    pass




#ログイン
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


#ログアウト
def logout_view(request):
    logout(request)
    return redirect('board-list')

#サインアップ
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request,'registration/signup.html',{'form':form})




#プロフィール
@login_required
def profile(request):
    template_name='accounts/profile.html'
    user = request.user
    return render(request,template_name,{'user':user})