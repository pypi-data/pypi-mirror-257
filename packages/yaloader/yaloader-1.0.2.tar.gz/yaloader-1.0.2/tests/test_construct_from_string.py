import pytest
from yaml.parser import ParserError

from yaloader import YAMLValueError


def test_load_list(config_loader, AConfig):
    config_list = config_loader.construct_from_string(
        """
        - !A {attribute: 1}
        - !A {attribute: 2}
        - !A {attribute: 3}
        """
    )
    assert config_list == [AConfig(attribute=1), AConfig(attribute=2), AConfig(attribute=3)]


def test_raise_on_not_a_mapping(config_loader, AConfig):
    with pytest.raises(ParserError) as error:
        config_loader.construct_from_string("!A 2")


def test_raise_on_additional_attribute(config_loader, AConfig):
    with pytest.raises(YAMLValueError) as error:
        config_loader.construct_from_string("!A {xyz: 1}")


def test_raise_on_wrong_attribute_type(config_loader, AConfig):
    with pytest.raises(YAMLValueError) as error:
        config_loader.construct_from_string('!A {attribute: "Some text"}')


def test_multi_load_list(config_loader, AConfig):
    config_list = config_loader.construct_from_string(
        """
        - !A {attribute: 2}
        - !A {attribute: 3}
        - !ConfigVarABC {attribute: 1, _tag: "!A"}
        """
    )
    assert config_list == [AConfig(attribute=2), AConfig(attribute=3), AConfig(attribute=1)]
