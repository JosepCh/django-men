from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404

# Create your views here.
def post_list(request):
    #Renderizamos el html que queramos y los parametros
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts' : posts
    })

def post_new(request):
    success = False
    # Renderizamos lo que queremos mostrar
    form = PostForm()
    # Rellenamos el formulario con el POST del usuario
    if request.method ==  'POST' : 
        form = PostForm(request.POST)
    # Validamos que los datos son válidos
    if form.is_valid():
        # Guardamos la info del formulario en la base de datos
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        success = True
        return redirect('post_list')
    return render(request,'blog/post_edit.html',{
        'form' : form,
        'success' : success
    })

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request,pk):
    Post.objects.filter(pk=pk).delete()
    return redirect('post_list')