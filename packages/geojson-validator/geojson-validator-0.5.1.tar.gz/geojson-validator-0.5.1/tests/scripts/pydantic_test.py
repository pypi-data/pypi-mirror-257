# from geojson_pydantic import Feature, FeatureCollection, Geometry
# import pytest
# from pathlib import Path
# from tests.fixtures import read_geojson
#
#
# @pytest.fixture(scope="module")
# def geojson_invalid_schema():
#     base_path = Path("tests/data/valid")
#     return list(base_path.rglob("valid_featurecollection_*.geojson"))
#
#
# def test_schema_validation_all_invalid_schema_files(geojson_invalid_schema):
#     ### All invalid schema test files
#     for file_path in geojson_invalid_schema:
#         print(file_path.name)
#         if file_path.name not in [
#             "valid_featurecollection_empty_features.geojson"
#             "invalid_geometry_geometrycollection_nested.geojson",  # TODO, but is should not be
#             "invalid_geometry_geometrycollection_single.geojson",  # TODO, but is should
#         ]:
#             fc = read_geojson(file_path)
#             fcc = Geometry(**fc)
