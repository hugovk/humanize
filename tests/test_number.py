#!/usr/bin/env python

"""Number tests."""

import pytest
from humanize import number


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1", "1st"),
        ("2", "2nd"),
        ("3", "3rd"),
        ("4", "4th"),
        ("11", "11th"),
        ("12", "12th"),
        ("13", "13th"),
        ("101", "101st"),
        ("102", "102nd"),
        ("103", "103rd"),
        ("111", "111th"),
        ("something else", "something else"),
        (None, None),
    ],
)
def test_ordinal(test_input, expected):
    assert number.ordinal(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (100, "100"),
        (1000, "1,000"),
        (10123, "10,123"),
        (10311, "10,311"),
        (1000000, "1,000,000"),
        (1234567.25, "1,234,567.25"),
        ("100", "100"),
        ("1000", "1,000"),
        ("10123", "10,123"),
        ("10311", "10,311"),
        ("1000000", "1,000,000"),
        ("1234567.1234567", "1,234,567.1234567"),
        (None, None),
    ],
)
def test_intcomma(test_input, expected):
    assert number.intcomma(test_input) == expected


def test_intword_powers():
    # make sure that powers & human_powers have the same number of items
    assert len(number.powers) == len(number.human_powers)


@pytest.mark.parametrize(
    "test_args, expected",
    [
        (["100"], "100"),
        (["1000000"], "1.0 million"),
        (["1200000"], "1.2 million"),
        (["1290000"], "1.3 million"),
        (["1000000000"], "1.0 billion"),
        (["2000000000"], "2.0 billion"),
        (["6000000000000"], "6.0 trillion"),
        (["1300000000000000"], "1.3 quadrillion"),
        (["3500000000000000000000"], "3.5 sextillion"),
        (["8100000000000000000000000000000000"], "8.1 decillion"),
        ([None], None),
        (["1230000", "%0.2f"], "1.23 million"),
        ([10 ** 101], "1" + "0" * 101),
    ],
)
def test_intword(test_args, expected):
    assert number.intword(*test_args) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1, "one"),
        (2, "two"),
        (4, "four"),
        (5, "five"),
        (9, "nine"),
        (10, "10"),
        ("7", "seven"),
        (None, None),
    ],
)
def test_apnumber(test_input, expected):
    assert number.apnumber(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (1, "1"),
        (2.0, "2"),
        (4.0 / 3.0, "1 1/3"),
        (5.0 / 6.0, "5/6"),
        ("7", "7"),
        ("8.9", "8 9/10"),
        ("ten", "ten"),
        (None, None),
    ],
)
def test_fractional(test_input, expected):
    assert number.fractional(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (0, "midnight"),
        (1, "one"),
        (9, "nine"),
        (10, "10"),
        (11, "11"),
        (12, "noon"),
        (13, "one"),
        (23, "11"),
        (24, "midnight"),
        (25, ValueError),
    ],
)
def test_hour(test_input, expected):
    assert number.hour(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (0, ValueError),
        (5, "five"),
        (10, "10"),
        (15, "quarter"),
        (20, "20"),
        (25, "25"),
        (30, "half"),
        (35, "25"),
        (40, "20"),
        (45, "quarter"),
        (50, "10"),
        (55, "five"),
        (60, ValueError),
    ],
)
def test_minute(test_input, expected):
    assert number.minute(test_input) == expected
