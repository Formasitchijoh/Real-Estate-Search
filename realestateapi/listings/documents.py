from django_elasticsearch_dsl import Document, Index, fields

from .models import Listing

listing_index = Index("listing")
listing_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@listing_index.doc_type
class ListingDocument(Document):
    town = fields.TextField(attr="town", fields={"suggest": fields.Completion()})
   #price = fields.IntegerField(attr="price", fields={"suggest":fields.CompletionField()})

    class Django:
        model = Listing
        fields = ['id', 'title', 'link', 'listing_type','price', 'bedroom', 'bathrooms', 'location', 'pricepermonth', 'views', 'reactions']