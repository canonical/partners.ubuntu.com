import re

from django.db.models import QuerySet
from django.forms.models import model_to_dict


def serialize(data: QuerySet):
    """
    An easier way to serialize django querysets with ManyToManyField or
    ForeignKey fields.
    """
    serialized_data = []
    # Return if queryset is empty
    if len(data) == 0:
        return serialized_data

    # Get related fields
    related_fields = [
        field.name for field in data.first()._meta.local_many_to_many
    ]

    # Get reverse-relations i.e. *_set attribute models
    set_match = re.compile("[a-zA-Z]+_set")
    reverse_relations = [
        attr_name
        for attr_name in dir(data.first())
        if set_match.search(attr_name)
    ]

    for item in data:
        # Serialize the entire model instance.
        start_object = model_to_dict(item)

        for field in related_fields:
            field_list = start_object[field]
            # Serialize the related field objects.
            serialized_field = [model_to_dict(obj) for obj in field_list]
            start_object[field] = serialized_field

        for relation in reverse_relations:
            queryset = getattr(item, relation).all()
            serialized_relation = [
                model_to_dict(instance) for instance in queryset
            ]
            start_object[relation] = serialized_relation

        serialized_data.append(start_object)

    return serialized_data
