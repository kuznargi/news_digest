from django.db import models

class News(models.Model):
    img=models.ImageField(upload_to='images/')
    title = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
  
class Category(models.Model):
    name = models.TextField()
    newsapi_mapping = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Corresponding NewsAPI category name (business, technology, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'