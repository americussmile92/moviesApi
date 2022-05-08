from abc import ABC

from django.db.models import Transform
from django.db.models import CharField


class SpaceRemovedValue(Transform, ABC):
    lookup_name = 'nospaces'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "REPLACE(%s, ' ', '')." % lhs, params


CharField.register_lookup(SpaceRemovedValue)