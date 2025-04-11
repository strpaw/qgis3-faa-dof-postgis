"""Helper for getting primary key database table value based on human friendly values"""
from .db_utils import DBUtils


class DBValuesMapping:

    """Handle database mapping values between 'human' friendly values and database primary keys"""


    def __init__(self,
                 db_utils: DBUtils):
        self.db_utils = db_utils
        self.oas = {}
        self.hor_acc = {}
        self.vert_acc = {}
        self.obstacle_type = {}
        self.marking = {}
        self.lighting = {}
        self.verification_status = {}

    def _set_mapping(self,
                    query: str,
                    mapping: dict) -> None:
        """Set mapping between database 'human' friendly values and database primary keys

        :param query: SQL query based on which mapping will be set
        :param mapping: mapping to be set
        """
        data = self.db_utils.select(query=query)
        for value, primary_key in data:
            mapping[value] = primary_key

    def set_all_mapping(self) -> None:
        """Set mapping between database 'human' friendly values and database primary keys
        for all control in the plugin UI"""
        self._set_mapping(
            query="select name, code from dof.oas;",
            mapping=self.oas
        )
        self._set_mapping(
            query="select accuracy, code from dof.vw_horizontal_acc;",
            mapping=self.hor_acc
        )
        self._set_mapping(
            query="select accuracy, code from dof.vw_vertical_acc;",
            mapping=self.vert_acc
        )
        self._set_mapping(
            query="select type, id from dof.obstacle_type;",
            mapping=self.obstacle_type
        )
        self._set_mapping(
            query="select description, code from dof.marking",
            mapping=self.marking
        )
        self._set_mapping(
            query="select description, code from dof.lighting;",
            mapping=self.lighting
        )
        self._set_mapping(
            query="select description, code from dof.verif_status;",
            mapping=self.verification_status
        )
