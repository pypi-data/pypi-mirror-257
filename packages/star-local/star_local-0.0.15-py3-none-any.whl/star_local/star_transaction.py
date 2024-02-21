from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger

# from api_management_local.Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,NotEnoughStarsForActivityException,PassedTheHardLimitException
from .entity_constants import StarLocalConstants

object1 = StarLocalConstants.STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT
logger = Logger.create_logger(object=object1)


class StarTransaction(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="star_transaction", default_table_name="star_transaction_table")

    # def insert_stars(self,data_json: dict):
    #     self.insert(data_json=data_json)
