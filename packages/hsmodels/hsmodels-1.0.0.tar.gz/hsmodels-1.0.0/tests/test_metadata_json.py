import json
import os

import pytest

from hsmodels.schemas.aggregations import (
    FileSetMetadataIn,
    GeographicFeatureMetadataIn,
    GeographicRasterMetadataIn,
    ModelInstanceMetadataIn,
    ModelProgramMetadataIn,
    MultidimensionalMetadataIn,
    ReferencedTimeSeriesMetadataIn,
    SingleFileMetadataIn,
    TimeSeriesMetadataIn,
)
from hsmodels.schemas.resource import ResourceMetadataIn


def sorting(item):
    if isinstance(item, dict):
        return sorted((key, sorting(values)) for key, values in item.items())
    if isinstance(item, list):
        return sorted(sorting(x) for x in item)
    else:
        return item


@pytest.fixture()
def res_md():
    with open("data/json/resource.json", 'r') as f:
        return ResourceMetadataIn(**json.loads(f.read()))


def test_resource_additional_metadata_dictionary(res_md):
    assert res_md.additional_metadata == {"key1": "value1", "key2": "value2", "key_empty": ""}
    res_md_in = ResourceMetadataIn(**res_md.model_dump())
    assert res_md_in.additional_metadata == {"key1": "value1", "key2": "value2", "key_empty": ""}

    assert res_md_in.model_dump()["additional_metadata"] == {"key1": "value1", "key2": "value2", "key_empty": ""}


metadata_json_input = [
    (ResourceMetadataIn, 'resource.json'),
    (GeographicRasterMetadataIn, 'geographicraster.json'),
    (GeographicFeatureMetadataIn, 'geographicfeature.json'),
    (MultidimensionalMetadataIn, 'multidimensional.json'),
    (ReferencedTimeSeriesMetadataIn, 'referencedtimeseries.refts.json'),
    (FileSetMetadataIn, 'fileset.json'),
    (SingleFileMetadataIn, 'singlefile.json'),
    (TimeSeriesMetadataIn, 'timeseries.json'),
    (ModelProgramMetadataIn, 'modelprogram.json'),
    (ModelInstanceMetadataIn, 'modelinstance.json'),
    (ResourceMetadataIn, 'collection.json'),
]


@pytest.mark.parametrize("metadata_json_input", metadata_json_input)
def test_metadata_json_serialization(metadata_json_input):
    in_schema, metadata_file = metadata_json_input
    metadata_file = os.path.join('data', 'json', metadata_file)
    with open(metadata_file, 'r') as f:
        json_file_str = f.read()
    md = in_schema.model_validate_json(json_file_str)
    from_schema = sorting(json.loads(md.model_dump_json()))
    from_file = sorting(json.loads(json_file_str))
    for i in range(1, len(from_file)):
        assert from_file[i] == from_schema[i]
