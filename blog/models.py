from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.urls.base import reverse_lazy
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage


User = get_user_model()



class BlogCategory(models.Model):
    title = models.CharField(max_length=50)

    #moderations
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('blog-blog')
    
    class Meta:
        verbose_name_plural = 'BlogCategories'


class BlogPost(models.Model):
    """
    this model is to save all blogs on main page example: Fashion, Women Fashion,
    """
    
    #relations
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               db_index=True, related_name='blogs')
    category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE,
                               db_index=True, related_name='blogs')
    like = models.ManyToManyField(User, related_name='likes', blank=True)

    # informations
    slug = models.CharField(verbose_name='Slug', max_length=140,null=True, blank=True)
    title = models.CharField(max_length=40)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/')
    

    # moderations
    is_published = models.BooleanField('Should it get published?', default=False)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy('single-blog', kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.content


    
class Comment(models.Model):
    """
        This model shows comments under particular blog
    """

    # relations
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                               db_index=True, related_name='comments')
    parent_comment = models.ForeignKey('self', db_index=True, null=True, blank=True,
                                    related_name='replies', on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, on_delete=CASCADE, db_index=True, related_name="comments",
                                                                            null=True, blank=True,)
    content = models.TextField(max_length=500)

    # moderations
    is_published = models.BooleanField('Should it get published?', default=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return  self.user.username 




 
    
