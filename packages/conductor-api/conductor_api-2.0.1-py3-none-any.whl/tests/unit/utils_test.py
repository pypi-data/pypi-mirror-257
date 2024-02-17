from conductor_api.utils import week_number


def test_week_number():
    number = week_number("2018-04-12")
    assert number == 455
