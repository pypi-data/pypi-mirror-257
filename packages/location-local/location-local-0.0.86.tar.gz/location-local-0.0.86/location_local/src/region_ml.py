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


class RegionMl(GenericCRUDML):

    def __init__(self):
        logger.start("start init RegionMl")
        GenericCRUDML.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.REGION_TABLE_NAME,
            default_id_column_name=LocationLocalConstants.REGION_ML_ID_COLUMN_NAME)  # noqa501
        logger.end("end init RegionMl")

    def insert(self, region_id: int, region: str,
               lang_code: LangCode = None, title_approved: bool = False):
        logger.start("start insert region_ml",
                     object={'region_id': region_id,
                             'region': region,
                             'lang_code': lang_code,
                             'title_approved': title_approved})
        LangCode.validate(lang_code)
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        region_ml_json = {
                key: value for key, value in {
                    'region_id': region_id,
                    'lang_code': lang_code.value,
                    'title': region,
                    'title_approved': title_approved
                }.items() if value is not None
            }
        region_ml_id = GenericCRUDML.insert(
            self,
            table_name=LocationLocalConstants.REGION_ML_TABLE_NAME,
            data_json=region_ml_json)
        logger.end("end insert region_ml",
                   object={'region_ml_id': region_ml_id})

        return region_ml_id
