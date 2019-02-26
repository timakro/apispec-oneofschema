# apispec-oneofschema

Plugin for apispec providing support for Marshmallow-OneOfSchema schemas

Can only be used with OpenAPI version 3.0.0 or greater which introduced a
name to definition mapping for the discriminator.

## Example

```python
from apispec import APISpec
from marshmallow import Schema, fields
from marshmallow_oneofschema import OneOfSchema
from apispec_oneofschema import MarshmallowPlugin

class TreeSchema(Schema):
    leaves = fields.Int(required=True)

class FlowerSchema(Schema):
    blooming = fields.Bool(required=True)

class PlantSchema(OneOfSchema):
    type_schemas = {
        'tree': TreeSchema,
        'flower': FlowerSchema
    }

    # def get_obj_type(self, obj):
    #   ...

spec = APISpec(
    title='Botany',
    version='1.0.0',
    openapi_version='3.0.0',
    plugins=[
        MarshmallowPlugin(),
    ]
)
spec.components.schema('Plant', schema=PlantSchema)
print(spec.to_yaml())
```

Resulting OpenAPI spec:

```yaml
components:
  parameters: {}
  responses: {}
  schemas:
    Flower:
      properties:
        blooming: {type: boolean}
      required: [blooming]
      type: object
    Plant:
      discriminator:
        mapping: {flower: '#/components/schemas/Flower', tree: '#/components/schemas/Tree'}
        propertyName: type
      oneOf:
      - {$ref: '#/components/schemas/Flower'}
      - {$ref: '#/components/schemas/Tree'}
    Tree:
      properties:
        leaves: {format: int32, type: integer}
      required: [leaves]
      type: object
  securitySchemes: {}
info: {title: Botany, version: 1.0.0}
openapi: 3.0.0
paths: {}
tags: []
```

## Installation

    pip install apispec-oneofschema

## License

Copyright (C) 2019 Tim Schumacher

License LGPLv3+: GNU LGPL version 3 or later <http://gnu.org/licenses/lgpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent per‐mitted by law.
