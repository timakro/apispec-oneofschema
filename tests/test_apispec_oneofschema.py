import pytest
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

class ForestSchema(Schema):
    plant = fields.Nested(PlantSchema)

@pytest.fixture()
def spec():
    return APISpec(
        title='Botany',
        version='1.0.0',
        openapi_version='3.0.0',
        plugins=[
            MarshmallowPlugin(),
        ]
    )

def test_top_level(spec):
    spec.components.schema('Plant', schema=PlantSchema)

    schemas = spec.to_dict()['components']['schemas']
    plant = schemas['Plant']
    discriminator = plant['discriminator']
    oneof = plant['oneOf']

    assert discriminator['mapping']['flower'] ==  '#/components/schemas/Flower'
    assert discriminator['propertyName'] == 'type'
    assert {'$ref': '#/components/schemas/Flower'} in oneof
    assert {'$ref': '#/components/schemas/Tree'} in oneof

    assert 'Tree' in schemas
    assert 'Flower' in schemas


def test_type_schema_already_in_spec(spec):
    spec.components.schema('Flower', schema=FlowerSchema)
    spec.components.schema('Plant', schema=PlantSchema)

    schemas = spec.to_dict()['components']['schemas']
    assert 'Tree' in schemas
    assert 'Flower' in schemas
    assert 'Plant' in schemas


def test_nested(spec):
    spec.components.schema('Forest', schema=ForestSchema)

    schemas = spec.to_dict()['components']['schemas']

    forest = schemas['Forest']
    assert forest['properties']['plant'] == {'$ref': '#/components/schemas/Plant'}

    plant = schemas['Plant']
    discriminator = plant['discriminator']
    oneof = plant['oneOf']

    assert discriminator['mapping']['flower'] ==  '#/components/schemas/Flower'
    assert discriminator['propertyName'] == 'type'
    assert {'$ref': '#/components/schemas/Flower'} in oneof
    assert {'$ref': '#/components/schemas/Tree'} in oneof

    assert 'Tree' in schemas
    assert 'Flower' in schemas


def test_resolver_returns_none():
    def resolver(schema):
        return None

    spec = APISpec(
        title='Botany',
        version='1.0.0',
        openapi_version='3.0.0',
        plugins=[
            MarshmallowPlugin(schema_name_resolver=resolver),
        ]
    )

    spec.components.schema('Plant', schema=PlantSchema)

    schemas = spec.to_dict()['components']['schemas']
    plant = schemas['Plant']
    discriminator = plant['discriminator']
    oneof = plant['oneOf']

    assert discriminator['mapping']['flower'] ==  '#/components/schemas/flower'
    assert 'flower' in schemas


def test_in_operations(spec):
    spec.path(
        path="/pet",
        operations={
            "get": {
                "responses": {
                    200: {
                        "content": {"application/json": {"schema": 'PlantSchema'}},
                        "description": "successful operation",
                    }
                }
            }
        },
    )

    schemas = spec.to_dict()['components']['schemas']
    plant = schemas['Plant']
    discriminator = plant['discriminator']
    oneof = plant['oneOf']

    assert discriminator['mapping']['flower'] ==  '#/components/schemas/Flower'
    assert discriminator['propertyName'] == 'type'
    assert {'$ref': '#/components/schemas/Flower'} in oneof
    assert {'$ref': '#/components/schemas/Tree'} in oneof

    assert 'Tree' in schemas
    assert 'Flower' in schemas


def test_v2():
    spec = APISpec(
        title='Botany',
        version='1.0.0',
        openapi_version='2.0',
        plugins=[
            MarshmallowPlugin(),
        ]
    )

    spec.components.schema('Plant', schema=PlantSchema)

    schemas = spec.to_dict()['definitions']
    plant = schemas['Plant']
    assert plant['type'] == 'object'

    assert 'Tree' not in schemas
