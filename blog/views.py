from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required 
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

""" Listagem principal dos posts publicados """
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

""" Detalhe do post """
def post_detail(request, post_id):
    #post = Post.objects.get(pk=post_id)
    post = get_object_or_404(Post, pk=post_id)    
    return render(request, 'blog/post_detail.html', {'post': post})

""" Novo post com botao save """
#Nota: esta parte serve para chamar o formulario
#Mas tambem cai aqui quando salvamos (POST) o formulario
@login_required
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

""" Editar post """
@login_required
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

""" Lista os posts ainda nao publicados """
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

""" Publica o post """
@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.publish()
    return redirect('blog.views.post_detail', post_id=post.pk)

""" Deleta o post """
@login_required
def post_delete(request, post_id):    
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog.views.post_list')

""" Adiciona comentarios ao post """
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', post_id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

""" Aprova comentarios """
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', post_id=comment.post.pk)

""" Deleta comentarios """
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', post_id=post_pk)

