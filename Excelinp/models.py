from django.db import models
from django.core.urlresolvers import reverse

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.CharField(max_length=10, unique=True,
                            default="question")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Item(models.Model):
    ID = models.SmallIntegerField(primary_key=True)
    Code = models.CharField(max_length=20)
    Description = models.CharField(max_length=200)
    Unit = models.TextField(max_length=5)
    Price3 = models.DecimalField(max_digits=14,decimal_places=2)

    def __str__(self):
        return self.Code 

    def __unicode__(self):
        return self.Code

    def get_absolute_url(self):
        return "/products/%s/" % self.ID  
        # return reverse('Item.views.details', args=[str(self.ID)])  


