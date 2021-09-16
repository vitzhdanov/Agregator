from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class News(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    site = models.URLField()
    title = models.CharField(max_length=300)
    picture = models.URLField()
    logo = models.URLField()
    description = models.TextField()
    date = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.date.strftime("%d-%m-%Y | %H:%M")
