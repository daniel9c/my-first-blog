from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    #post = Post.objects.get(pk=post_id)
    post = get_object_or_404(Post, pk=post_id)    
    return render(request, 'blog/post_detail.html', {'post': post})

#Nota: esta parte serve para chamar o formulario
#Mas tambem cai aqui quando salvamos (POST) o formulario
def post_new(request):
    if request.method == "POST":
        #Quando o form eh salvo
        form = PostForm(request.POST) #pega os dados do form
        if form.is_valid(): #verifica se os campos estao preenchidos
            post = form.save(commit=False) #salvo com commit false para conseguir pegar o objeto Post
            post.author = request.user # e adicionamos o author que eh obrigatorio
            post.save()
            #Apos salvar, redirecionamos para os detalhes
            return redirect('blog.views.post_detail', post_id=post.pk)
    else:
        #Quando eh um novo form
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id) # pegamos o objeto post que queremos editar
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) #passamos ele na instancia para salvar a edicao
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post) #passamos ele na instancia para o novo formulario
    return render(request, 'blog/post_edit.html', {'form': form})