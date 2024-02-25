import project
import pytest
import pandas as pd


def test_type_of_restaurant():
    assert project.type_of_restaurant('cafe') == 'cafe'
    assert project.type_of_restaurant('liquor') == 'liquor_store'
    assert project.type_of_restaurant('club') == 'night_club'
    assert project.type_of_restaurant('clubbing') == 'night_club'
    with pytest.raises(SystemExit):
        project.type_of_restaurant('abc')


def test_get_geocode():
    with pytest.raises(SystemExit):
        project.get_geocode('sdasdadsad')
    lat1,lng1 = project.get_geocode('b13el')
    lat1 = round(lat1, 2)
    lng1 = round(lng1, 2)
    assert lat1,lng1 == (52.49, -1.91)
    lat,lng = project.get_geocode('big ben london')
    lat = round(lat, 2)
    lng = round(lng, 2)
    assert lat,lng == (51.50, -0.12)




def test_pick_3():
    df = pd.DataFrame({'Name': ['Alice', 'Bob', 'Charlie', 'Dave', 'Eric', 'Fred', 'George'],
                   'Age': [25, 30, 35, 40, 50, 60, 55],
                   'City': ['New York', 'Paris', 'London', 'Tokyo', 'Hong Kong', 'Osaka', 'Los Angles']})
    ran_num = project.pick_3(df)
    assert len(ran_num) == 3