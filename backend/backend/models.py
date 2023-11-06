from djongo import models

class InvertedIndex(models.Model):
    word = models.CharField(max_length=100)
    postings = models.JSONField()

    class Meta:
        abstract = True

class PageRank(models.Model):
    filename = models.CharField(max_length=100)
    rank = models.FloatField()

    class Meta:
        abstract = True