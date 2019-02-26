# apispec-oneofschema - Plugin for apispec providing support for
#                       Marshmallow-OneOfSchema schemas
# Copyright (C) 2019  Tim Schumacher

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from apispec.ext import marshmallow
from marshmallow_oneofschema import OneOfSchema

class OneofOpenAPIConverter(marshmallow.OpenAPIConverter):
    def schema2jsonschema(self, schema):
        if self.openapi_version.major < 3 or not is_oneof(schema):
            return super(OneofOpenAPIConverter, self).schema2jsonschema(schema)
        mapping = {}
        oneof = []
        for name, type_schema in schema.type_schemas.items():
            component_name = self.schema_name_resolver(type_schema) or name
            self.spec.components.schema(component_name, schema=type_schema)
            ref = '#/components/schemas/{}'.format(component_name)
            mapping.update({name: ref})
            oneof.append({'$ref': ref})

        return {
            'oneOf': oneof,
            'discriminator': {
                'propertyName': schema.type_field,
                'mapping': mapping
            }
        }


def is_oneof(schema):
    return (
        (isinstance(schema, type) and issubclass(schema, OneOfSchema))
        or
        isinstance(schema, OneOfSchema)
    )


class MarshmallowPlugin(marshmallow.MarshmallowPlugin):
    def init_spec(self, spec):
        super(MarshmallowPlugin, self).init_spec(spec)
        self.openapi = OneofOpenAPIConverter(
            openapi_version=spec.openapi_version,
            schema_name_resolver=self.schema_name_resolver,
            spec=spec,
        )
