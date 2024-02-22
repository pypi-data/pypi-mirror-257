from jmenu.classes import Marker, Restaurant, MenuItem, MARKERS, RESTAURANTS


def test_rest():
    rest = Restaurant("test", 1, 2, 3, ["test"])
    assert rest is not None
    assert rest.name == "test"
    assert rest.client_id == 1
    assert rest.kitchen_id == 2
    assert rest.menu_type == 3
    assert rest.relevant_menus == ["test"]


def test_marker():
    mark = Marker("t", "test")
    assert mark is not None
    assert mark.letters == "t"
    assert mark.explanation == "test"


def test_menu_item():
    item = MenuItem("test", "t")
    assert item is not None
    assert item.diets == "t"
    assert item.name == "test"


def test_restaurants():
    assert RESTAURANTS is not None
    assert len(RESTAURANTS) == 6
    for rest in RESTAURANTS:
        assert rest is not None
        assert rest.name is not None


def test_markers():
    assert MARKERS is not None
    assert len(MARKERS) == 10
    for mark in MARKERS:
        assert mark is not None
        assert mark.letters is not None
