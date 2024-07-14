from django_elasticsearch_dsl import Document, Index, fields

from .models import Listing,Image

listing_index = Index("listing")
listing_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)

class ImageDocument(Document):
    id = fields.IntegerField(attr='id')
    image = fields.TextField(attr='image')
    listing = fields.IntegerField(attr='listing')

    class Index:
        name = 'image'

    class Django:
        model = Image
        fields = ['id', 'image', 'listing']


@listing_index.doc_type
class ListingDocument(Document):
    town = fields.TextField(attr="town", fields={"suggest": fields.Completion()})
    listing_images = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'image': fields.TextField(),
    })
    class Index:
        name = 'listings'

    class Django:
        model = Listing
        fields = ['id', 'title', 'link', 'listing_type','price', 'bedroom', 'bathrooms', 'location', 'pricepermonth', 'views', 'reactions']
        related_models = [Image]

    def get_queryset(self):
        return super(ListingDocument, self).get_queryset().prefetch_related('listing_images')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Image):
            return related_instance.listing
        return None