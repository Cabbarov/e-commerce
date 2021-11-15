from blog.forms import CommentForm
from django.shortcuts import redirect, render, get_object_or_404   
from django.db.models import Q
from blog.models import *
from product.models import *
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView,ListView



class BlogsView(ListView):
    model = BlogPost
    template_name = 'blog/blog.html'
    paginate_by = 6


class BlogDetailView(FormMixin, DetailView):
    model = BlogPost
    form_class = CommentForm
    template_name = 'blog/single-blog.html'
    context_object_name = 'blog'

    
    def get_success_url(self):
        return reverse("single-blog", kwargs={"pk": self.object.pk})


    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        blog = BlogPost.objects.filter(id=self.object.pk).first()
        is_liked = False   
        if blog.like.filter(id=self.request.user.id).exists():
            is_liked = True
        recent_posts = BlogPost.objects.all().order_by('-created_at')[:3]
        comments = Comment.objects.filter(parent_comment=None, blog=blog)

        related_blogs = BlogPost.objects.all().filter(Q(category=blog.category) & (~Q(id=blog.id)))
        context["related_blogs"] = related_blogs
        context["comments"] = comments
        context["is_liked"] = is_liked
        context["recent_posts"] = recent_posts
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        blog = BlogPost.objects.filter(id=self.object.pk).first()

        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user
            reply_obj = None
            request.POST.get('reply_id')
            if request.POST.get('reply_id'):
                reply_id = request.POST.get('reply_id')
            else:
                reply_id = None
            if reply_id:
                reply_obj = Comment.objects.get(id=reply_id)
                if reply_obj:
                    Comment(content=content, parent_comment = reply_obj, blog=blog, user=user).save()
            else: 
                Comment(content=content, blog=blog, user=user).save()
            return redirect(f'/blogs/single-blog/{self.object.slug}')
        else:
            return self.form_invalid(form)

            
    
    def form_valid(self, form):
        form.instance.blog = self.get_object()
        form.save()
        return super().form_valid(form)



def like(request, slug):
    blog = get_object_or_404(BlogPost, id=request.POST.get('blog_id'))
    if blog.like.filter(id=request.user.id).exists(): #if user already liked remove user's like
        blog.like.remove(request.user)
        is_liked = False
    else:
        blog.like.add(request.user)
        is_liked = True
    return redirect('single-blog', blog.slug)





