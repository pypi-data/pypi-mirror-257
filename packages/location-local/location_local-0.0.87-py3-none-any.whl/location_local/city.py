from dotenv import load_dotenv
from .city_ml import CityMl
from .location_local_constants import LocationLocalConstants
from .point import Point
from .util import LocationsUtil
load_dotenv()
from database_mysql_local.generic_crud import GenericCRUD  # noqa402
from logger_local.Logger import Logger  # noqa: E402
from language_remote.lang_code import LangCode  # noqa: E402
from user_context_remote.user_context import UserContext  # noqa: E402


logger = Logger.create_logger(
    object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class City(GenericCRUD):
    city_ml = CityMl()

    def __init__(self):
        logger.start("start init City")

        GenericCRUD.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.CITY_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.CITY_VIEW_NAME,
            default_id_column_name=LocationLocalConstants.CITY_ID_COLUMN_NAME)

        logger.end("end init City")

    def insert(
            self, city: str, lang_code: LangCode = None,
            title_approved: bool = False, coordinate: Point = None,
            group_id: int = None, phonecode: int = None,
            is_main: int = None) -> int:
        logger.start("start insert city",
                     object={'coordinate': coordinate, 'city': city,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'is_main': is_main})
        is_valid = LocationsUtil.validate_insert_args(
            name=city, lang_code=lang_code, title_approved=title_approved, coordinate=coordinate)
        if not is_valid:
            logger.end(log_message="City was not inserted because no city name was provided")
            return None
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        city_json = {
            key: value for key, value in {
                'coordinate': coordinate,
                'name': city,
                'phonecode': phonecode,
                'group_id': group_id
            }.items() if value is not None
        }

        city_id = GenericCRUD.insert(self, data_json=city_json)

        city_ml_id = self.city_ml.insert(city_id=city_id,
                                         city=city,
                                         lang_code=lang_code,
                                         title_approved=title_approved,
                                         is_main=is_main)

        logger.end("end insert city",
                   object={'city_id': city_id,
                           'city_ml_id': city_ml_id})
        return city_id

    def read(self, location_id: int):
        logger.start("start read city",
                     object={'location_id': location_id})
        result = GenericCRUD.select_one_dict_by_id(
            self,
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.CITY_TABLE_COLUMNS)
        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_city_id_by_city_name_state_id(city_name: str, country_id: int = None,
                                          lang_code: LangCode = None) -> int:
        logger.start("start get_city_id_by_city_name_state_id",
                     object={'city_name': city_name, 'country_id': country_id})
        if city_name is None:
            logger.end(log_message="end get_city_id_by_city_name_state_id",
                       object={'city_id': None})
            return None
        LangCode.validate(lang_code)
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        where_clause = f"title='{city_name}' AND lang_code='{lang_code.value}'"
        # TODO: Shall we add country_id to city_ml_view?
        # if country_id is not None:
        #    where_clause += f" AND country_id={country_id}"

        city_id_json = City.city_ml.select_one_dict_by_where(
            select_clause_value=LocationLocalConstants.CITY_ID_COLUMN_NAME,
            where=where_clause,
            order_by="city_id DESC")
        city_id = city_id_json.get(LocationLocalConstants.CITY_ID_COLUMN_NAME)

        logger.end("end get_city_id_by_city_name_state_id",
                   object={'city_id': city_id})
        return city_id
