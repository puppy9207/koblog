from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog,Portfolio
from django.core.paginator import Paginator
from django.utils import timezone
from .form import BlogPost

def home(request):
    blogs = Blog.objects
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list,3) #블로그 객체 세개를 한 페이지로 자르기
    page = request.GET.get('page') #request된 페이지가 무엇인지 알아내기
    posts = paginator.get_page(page)
    return render(request,'home.html',{'blogs':blogs,'posts':posts})

def detail(request,blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request,'detail.html',{'blog':blog_detail})

def portfolio(request):
    portfolios = Portfolio.objects
    return render(request,"portfolio.html",{'portfolios':portfolios})

def create(request):
    return render(request,'new.html')

def new(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body= request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/'+str(blog.id))

def blogpost(request):
    # 1. 입력된 내용을 처리하는 기능 -> POST
    # 2. 빈 페이지를 띄워주는 기능 -> GET
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid(): #입력 된 값들이 잘 입력됬는지 안되었는지 검사하는 메소드
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request,'new.html', {'form':form})