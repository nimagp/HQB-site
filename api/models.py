from django.db import models

class Pack(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        ordering=['title']

    def __str__(self):
        return self.title

class Question(models.Model):
    question = models.CharField(max_length=200)
    Pack = models.ForeignKey(Pack,on_delete=models.DO_NOTHING)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['question']

    def __str__(self):
        return self.question
class Server(models.Model):
    name=models.CharField(max_length=200)
    giuld=models.CharField(max_length=200)
    pack=models.IntegerField(default=1)
    class Meta: 
        ordering=['name']

    def __str__(self):
        return self.name
