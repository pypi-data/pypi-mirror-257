import pytest

from cringelord.app.cringe_config.util.list_to_dict import list_to_dict


class TestSettingListToDict:
    def test_transform_single_dict_list(self):
        # Arrange
        setting_list = [
            {'key1': 'value1'},
            {'key2': 'value2'},
            {'key3': 'value3'}
        ]
        expected_result = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }

        # Act
        result = list_to_dict(setting_list)

        # Assert
        assert result == expected_result

    def test_empty_list(self):
        # Arrange
        setting_list = []
        expected_result = {}

        # Act
        result = list_to_dict(setting_list)

        # Assert
        assert result == expected_result

    def test_single_dict(self):
        # Arrange
        setting_list = [{'key1': 'value1'}]
        expected_result = {'key1': 'value1'}

        # Act
        result = list_to_dict(setting_list)

        # Assert
        assert result == expected_result

    def test_item_not_dict(self):
        # Arrange
        setting_list = [{'key1': 'value1'}, 'not a dictionary']
        expected_result = {"key1": "value1", "not a dictionary": None}

        result = list_to_dict(setting_list)
        assert result == expected_result

    def test_dict_multiple_key_value_pairs(self):
        # Arrange
        setting_list = [{'key1': 'value1', 'key2': 'value2'}]

        result = list_to_dict(setting_list)
        assert result == {'key1': 'value1', 'key2': 'value2'}

    def test_already_dict(self):
        # Arrange
        setting_list = {'key1': 'value1'}
        expected_result = {'key1': 'value1'}

        # Act
        result = list_to_dict(setting_list)

        # Assert
        assert result == expected_result

    @pytest.mark.parametrize(
        "not_a_list",
        [
            'not a list',
            10,
            1.0
        ]
    )
    def test_raises_type_error_no_dict_or_list(self, not_a_list):
        with pytest.raises(TypeError):
            list_to_dict(not_a_list)

    def test_raises_type_error_non_dict_list_items(self):
        with pytest.raises(TypeError):
            list_to_dict([1, 2, 3])

    def test_list_contains_string(self):
        string_element = "not a dict"
        setting_list = [string_element]

        result = list_to_dict(setting_list)

        assert result == {string_element: None}
