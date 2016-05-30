# import datetime
from haystack import indexes
from Excelinp.models import Item


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    code = indexes.CharField(model_attr='Code')
    Id = indexes.CharField(model_attr='ID')
    Description = indexes.CharField(model_attr='Description')
    # url = indexes.CharField()
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        # return self.get_model().objects.order_by('Id')
        # .filter(pub_date__lte=datetime.datetime.now())
    # def prepare_url(self, obj):
    #     return obj.get_absolute_url()    