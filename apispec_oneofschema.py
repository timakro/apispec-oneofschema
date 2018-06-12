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
