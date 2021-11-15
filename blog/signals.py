from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from blog.models import BlogPost


@receiver(post_save, sender=BlogPost)
def story_set_slug(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = f"{slugify(instance.title)}-{instance.id}"
        instance.save()

