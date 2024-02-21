from .location_local_constants import LocationLocalConstants
from dotenv import load_dotenv
load_dotenv()
from database_mysql_local.generic_crud_ml import GenericCRUDML   # noqa402
from language_remote.lang_code import LangCode  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402

logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class StateMl(GenericCRUDML):

    def __init__(self):
        logger.start("start init StateMl")
        GenericCRUDML.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.STATE_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.STATE_ML_ID_COLUMN_NAME)  # noqa501
        logger.end("end init StateMl")

    def insert(self, state_id: int, state: str,
               lang_code: LangCode = None, title_approved: bool = False):
        logger.start("start insert state_ml",
                     object={'state_id': state_id,
                             'state': state,
                             'lang_code': lang_code,
                             # TODO Please give default value of False to all *_approved parameters
                             'title_approved': title_approved})
        LangCode.validate(lang_code)
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        state_ml_json = {
                key: value for key, value in {
                    'state_id': state_id,
                    'lang_code': lang_code.value,
                    'state_name': state,
                    'state_name_approved': title_approved
                }.items() if value is not None
            }
        state_ml_id = GenericCRUDML.insert(
            self,
            table_name=LocationLocalConstants.STATE_ML_TABLE_NAME,
            data_json=state_ml_json)
        logger.end("end insert state_ml",
                   object={'state_ml_id': state_ml_id})

        return state_ml_id
