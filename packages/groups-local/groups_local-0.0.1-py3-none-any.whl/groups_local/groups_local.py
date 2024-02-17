from typing import Dict
from .groups_local_constants import GroupsLocalConstants
from database_mysql_local.generic_crud_ml import GenericCRUDML  # noqa: E402
from database_infrastructure_local.number_generator import NumberGenerator  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=GroupsLocalConstants.GROUPS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)
user_context = UserContext()

DEFAULT_SCHEMA_NAME = "group"
DEFAULT_TABLE_NAME = "group_table"
DEFAULT_VIEW_TABLE_NAME = "group_view"
DEFAULT_ID_COLUMN_NAME = "group_id"


class GroupsLocal(GenericCRUDML):

    def __init__(self, is_test_data: bool = False):
        GenericCRUDML.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME, default_table_name=DEFAULT_TABLE_NAME,
                               default_id_column_name=DEFAULT_ID_COLUMN_NAME, is_test_data=is_test_data)

    def insert(self, group_dict: Dict[str, any]) -> tuple[int, int]:
        """
            Returns the new group_id
            group_dict has to include the following
            for group_ml_table:
            title: str, title_lang_code: str = None,
            is_main: bool = True
            for group_table:
            name: str,
            hashtag: str = None,
            parent_group_id: str = None,
            is_interest: bool = None,
            non_members_visibility_id: int = 1, members_visibility_id: int = 1
            example of group_dict:
            {
                "title": "title",
                "title_lang_code": "en",
                "name": "name",
                "hashtag": "hashtag",
                "parent_group_id": 1,
                "is_interest": True,
                "non_members_visibility_id": 1,
                "members_visibility_id": 1
            }
        """
        logger.start(object={'data': str(group_dict)})
        number = NumberGenerator.get_random_number(
            schema_name=DEFAULT_SCHEMA_NAME, view_name=DEFAULT_VIEW_TABLE_NAME)
        identifier = NumberGenerator.get_random_identifier(
            schema_name=DEFAULT_SCHEMA_NAME, view_name=DEFAULT_VIEW_TABLE_NAME,
            identifier_column_name="identifier")
        group_data_json = {
            "number": number,
            "identifier": identifier,
            "name": group_dict.get('name'),
            "hashtag": group_dict.get('hashtag'),
            "parent_group_id": group_dict.get('parent_group_id'),
            "is_interest": group_dict.get('is_interest'),
            "non_members_visibility_id": group_dict.get('non_members_visibility_id', 1),
            "members_visibility_id": group_dict.get('members_visibility_id', 1)
        }
        # TODO: We can't use GenericCRUDML's add_value method because the is main column in the ml table
        # is named "is_main" and not "is_main"
        group_id = GenericCRUDML.insert(self, data_json=group_data_json)

        lang_code = group_dict.get('title_lang_code') or user_context.get_effective_profile_preferred_lang_code_string()
        group_ml_data_json = {
            "group_id": group_id,
            "lang_code": lang_code,
            "title": group_dict.get('title'),
            "is_main": group_dict.get('is_main', False)
        }
        group_ml_id = GenericCRUDML.insert(self, table_name="group_ml_table", data_json=group_ml_data_json)

        logger.end(object={'group_id': group_id, 'group_ml_id': group_ml_id})
        return group_id, group_ml_id

    def upsert(self, group_dict: Dict[str, any]) -> tuple[int, int]:
        """
            Returns the new group_id
            group_dict has to include the following
            for group_ml_table:
            title: str, title_lang_code: str = None,
            is_main: bool = True
            for group_table:
            name: str,
            hashtag: str = None,
            parent_group_id: str = None,
            is_interest: bool = None,
            non_members_visibility_id: int = 1, members_visibility_id: int = 1
            example of group_dict:
            {
                "title": "title",
                "title_lang_code": "en",
                "name": "name",
                "hashtag": "hashtag",
                "parent_group_id": 1,
                "is_interest": True,
                "non_members_visibility_id": 1,
                "members_visibility_id": 1
            }
        """
        logger.start(object={'data': str(group_dict)})
        number = NumberGenerator.get_random_number(
            schema_name=DEFAULT_SCHEMA_NAME, view_name=DEFAULT_VIEW_TABLE_NAME)
        identifier = NumberGenerator.get_random_identifier(
            schema_name=DEFAULT_SCHEMA_NAME, view_name=DEFAULT_VIEW_TABLE_NAME,
            identifier_column_name="identifier")
        group_data_json = {
            "number": number,
            "identifier": identifier,
            "name": group_dict.get('name'),
            "hashtag": group_dict.get('hashtag'),
            "parent_group_id": group_dict.get('parent_group_id'),
            "is_interest": group_dict.get('is_interest'),
            "non_members_visibility_id": group_dict.get('non_members_visibility_id', 1),
            "members_visibility_id": group_dict.get('members_visibility_id', 1)
        }
        group_id = GenericCRUDML.upsert(self, data_json=group_data_json)

        lang_code = group_dict.get('title_lang_code') or user_context.get_effective_profile_preferred_lang_code_string()
        group_ml_data_json = {
            "group_id": group_id,
            "lang_code": lang_code,
            "title": group_dict.get('title'),
            "is_main": group_dict.get('is_main', False)
        }
        group_ml_id = GenericCRUDML.upsert(self, table_name="group_ml_table", data_json=group_ml_data_json)

        logger.end(object={'group_id': group_id, 'group_ml_id': group_ml_id})
        return group_id, group_ml_id

    def update(self, group_id: int, group_dict: Dict[str, any]) -> None:
        logger.start(object={'group_id': group_id, 'data': str(group_dict)})
        group_data_json = {
            "name": group_dict.get('name'),
            "hashtag": group_dict.get('hashtag'),
            "parent_group_id": group_dict.get('parent_group_id'),
            "is_interest": group_dict.get('is_interest'),
            "non_members_visibility_id": group_dict.get('non_members_visibility_id', 1),
            "members_visibility_id": group_dict.get('members_visibility_id', 1)
        }
        GenericCRUDML.update_by_id(self, id_column_value=group_id, data_json=group_data_json)

        group_ml_data_json = {
            "group_id": group_id,
            "lang_code": group_dict.get('title_lang_code'),
            "title": group_dict.get('title'),
            "is_main": group_dict.get('is_main', True)
        }
        GenericCRUDML.update_by_id(self, table_name="group_ml_table",
                                   id_column_value=group_id, data_json=group_ml_data_json,
                                   id_column_name="group_ml_id")
        logger.end()

    def get_group_dict_by_group_id(self, group_id: int, group_ml_id: int = None) -> Dict[str, any]:
        logger.start(object={'group_id': group_id})
        group_ml_dict = {}
        if group_ml_id:
            group_ml_dict = self.select_one_dict_by_id(view_table_name="group_ml_view", id_column_value=group_ml_id,
                                                       id_column_name="group_ml_id")
        group_dict = self.select_one_dict_by_id(view_table_name="group_view", id_column_value=group_id,
                                                id_column_name="group_id")
        logger.end(object={'group_ml_dict': str(group_ml_dict), 'group_view': str(group_dict)})
        return {**group_dict, **group_ml_dict}

    def delete_by_group_id(self, group_id: int, group_ml_id: int = None) -> None:
        logger.start(object={'group_id': group_id})
        # Delete from group_table
        self.delete_by_id(table_name="group_table", id_column_name="group_id", id_column_value=group_id)
        # Delete from group_ml_table
        if group_ml_id:
            self.delete_by_id(table_name="group_ml_table", id_column_name="group_ml_id", id_column_value=group_ml_id)
        logger.end()
