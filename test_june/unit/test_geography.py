import pytest
import numpy as np
import pandas as pd
import numpy.testing as npt
from time import time

from june.demography import geography as g


@pytest.fixture()
def geography_example():
    return g.Geography.from_file(filter_key={"super_area": ["E02000140"]})


def test__create_geographical_hierarchy():
    hierarchy_df = pd.DataFrame(
        {
            "area": ["area_1", "area_2", "area_3", "area_4",],
            "super_area": [
                "super_area_1",
                "super_area_1",
                "super_area_1",
                "super_area_2",
            ],
            "region": ["region_1", "region_1", "region_1", "region_2"],
        }
    )
    area_coordinates_df = pd.DataFrame(
        {
            "area": ["area_1", "area_2", "area_3", "area_4"],
            "longitude": [0.0, 1.0, 2.0, 3.0],
            "latitude": [0.0, 1.0, 2.0, 3.0],
        }
    )
    area_coordinates_df.set_index("area", inplace=True)
    super_area_coordinates_df = pd.DataFrame(
        {
            "super_area": ["super_area_1", "super_area_2"],
            "longitude": [0.0, 1.0],
            "latitude": [0.0, 1.0],
        }
    )
    super_area_coordinates_df.set_index("super_area", inplace=True)
    areas, super_areas, regions = g.Geography.create_geographical_units(
        hierarchy=hierarchy_df,
        area_coordinates=area_coordinates_df,
        super_area_coordinates=super_area_coordinates_df,
    )

    assert len(areas) == 4
    assert len(super_areas) == 2
    assert len(regions) == 2

    assert regions[0].super_areas[0].name == super_areas[0].name
    assert regions[1].super_areas[0].name == super_areas[1].name

    assert super_areas[0].region == regions[0]
    assert super_areas[1].region == regions[1]

    assert super_areas[0].areas == [areas[0], areas[1], areas[2]]
    assert super_areas[1].areas == [areas[3]]


def test__nr_of_members_in_units(geography_example):
    assert len(geography_example.areas) == 26
    assert len(geography_example.super_areas) == 1


def test__area_attributes(geography_example):
    area = geography_example.areas.members[0]
    assert area.name == "E00003598"
    npt.assert_almost_equal(
        area.coordinates, [51.395954503652504, 0.10846483370388499], decimal=3,
    )
    assert area.super_area.name in "E02000140"


def test__super_area_attributes(geography_example):
    print(geography_example.super_areas.members)
    print(geography_example.super_areas.members[0].name)
    super_area = geography_example.super_areas.members[0]
    assert super_area.name == "E02000140"
    npt.assert_almost_equal(
        super_area.coordinates, [51.40340615262757, 0.10741193961090514], decimal=3,
    )
    assert "E00003595" in [area.name for area in super_area.areas]


def test__create_single_area():
    geography = g.Geography.from_file(filter_key={"area": ["E00120481"]})
    assert len(geography.areas) == 1


def test_create_ball_tree_for_super_areas():
    geo = g.Geography.from_file(filter_key={"super_area": ["E02004935", "E02000140"]})
    super_area = geo.super_areas.get_closest_super_areas(
        coordinates=[54.770512, -1.594221]
    )[0]
    assert super_area.name == "E02004935"
