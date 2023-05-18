from django.db.models import QuerySet
from django.forms.models import model_to_dict


def serialize(data: QuerySet):
    """
    An easier way to serialize django querysets with ManyToManyField or ForeignKey
    fields. 
    """
    serialized_data = []

    # Get related fields
    related_fields = [field.name for field in data[0]._meta.local_many_to_many]

    # Need to add support for foreign keys
    
    for item in data:
        # Serialize the entire model instance.
        start_object = model_to_dict(item)

        for field in related_fields:
            field_list = start_object[field]
            # Serialize the related field objects.
            serialized_field = [model_to_dict(obj) for obj in field_list]
            start_object[field] = serialized_field
   
        serialized_data.append(start_object)

    return serialized_data