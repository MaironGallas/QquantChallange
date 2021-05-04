# Creating a Serializer class
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from ris.base.models import Articles, Article_Complete


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['id', 'dados']


class ArticleFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article_Complete
        fields = '__all__'

    def to_representation(self, instance):
            """
                Object instance -> Dict of primitive datatypes.
                """
            ret = OrderedDict()
            fields = self._readable_fields

            for field in fields:
                    try:
                        attribute = field.get_attribute(instance)
                    except SkipField:
                            continue

                    # KEY IS HERE:
                    if attribute in [None, '']:
                            continue

                    # We skip `to_representation` for `None` values so that fields do
                    # not have to explicitly deal with that case.
                    #
                    # For related fields with `use_pk_only_optimization` we need to
                    # resolve the pk value.
                    check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
                    if check_for_none is None:
                            ret[field.field_name] = None
                    else:
                            ret[field.field_name] = field.to_representation(attribute)

            return ret