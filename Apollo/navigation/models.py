from django.db import models
from users.models import CustomUser


class Blog(models.Model):
    blog_title = models.CharField('Название',
                                  max_length=300)
    type = models.CharField("Тип статьи",max_length=20, null = True)
    img = models.ImageField("Заставка",null=True)
    full_text = models.TextField('Полный текст')
    like = models.ManyToManyField(CustomUser,blank=True,related_name='Like')
    dislike = models.ManyToManyField(CustomUser,blank=True,related_name='dislike')
    date_public = models.DateTimeField('Дата', null=True)
    author = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True)
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural ='Blog Data Base'
    def __str__(self):
        return str(self.blog_title)

class Comment_user(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.PROTECT,null=True)
    comment = models.CharField(max_length = 250,
                            null = True)
    date_time = models.DateTimeField(null=True)
    like = models.ManyToManyField(CustomUser,blank=True,related_name='Likes')
    post = models.ForeignKey(Blog,on_delete=models.PROTECT,null=True)

class BlogHeshtags(models.Model):
    blog = models.ForeignKey(Blog,
                             default=None,
                             on_delete=models.CASCADE,
                             null=True)
    hashtag=models.CharField('Хештег',
                             max_length=150,
                             null='Без темы')
    def __str__(self):
        return str(self.hashtag)
