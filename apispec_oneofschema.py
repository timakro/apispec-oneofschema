# apispec-oneofschema - Plugin for apispec providing support for
#                       Marshmallow-OneOfSchema schemas
# Copyright (C) 2018  Tim Schumacher

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

from apispec.ext.marshmallow import swagger
from marshmallow_oneofschema import OneOfSchema


def oneofschema_definition_helper(spec, name, schema, definition, **kwargs):
    """Definition helper that allows using a Marshmallow-OneOfSchema schema to
    provide OpenAPI metadata. Uses the `schema` parameter.
    """
    if not OneOfSchema in schema.__bases__:
        return
    ref_path = swagger.get_ref_path(spec.openapi_version.version[0])
    try:
        refs = {name: '#/{}/{}'.format(ref_path,
                spec.plugins['apispec.ext.marshmallow']['refs'][schema_cls])
                for name, schema_cls in schema.type_schemas.items()}
    except KeyError:
        raise ValueError("Schemas from `type_schemas` must be added to the "
                         "spec before the Marshmallow-OneOfSchema schema")
    definition.clear()
    return {
        'oneOf': [{'$ref': ref} for ref in refs.values()],
        'discriminator': {
            'propertyName': schema.type_field,
            'mapping': refs
        }
    }


def setup(spec):
    spec.register_definition_helper(oneofschema_definition_helper)
