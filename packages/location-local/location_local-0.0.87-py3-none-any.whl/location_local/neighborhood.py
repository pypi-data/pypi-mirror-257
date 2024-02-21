from dotenv import load_dotenv
from .location_local_constants import LocationLocalConstants
from .neighborhood_ml import NeighborhoodMl
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


class Neighborhood(GenericCRUD):
    neighborhood_ml = NeighborhoodMl()

    def __init__(self):
        logger.start("start init Neighborhood")
        GenericCRUD.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.NEIGHBORHOOD_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.NEIGHBORHOOD_VIEW_NAME,  # noqa501
            default_id_column_name=LocationLocalConstants.NEIGHBORHOOD_ID_COLUMN_NAME)  # noqa501

        logger.end("end init Neighborhood")

    def insert(
            self, coordinate: Point,
            neighborhood: str, lang_code: LangCode = None,
            title_approved: bool = False, city_id: int = None,
            group_id: int = None) -> int:
        logger.start("start insert neighborhood",
                     object={'coordinate': coordinate,
                             'neighborhood': neighborhood,
                             'lang_code': lang_code,
                             'title_approved': title_approved,
                             'city_id': city_id,
                             'group_id': group_id})
        is_valid = LocationsUtil.validate_insert_args(
            name=neighborhood, lang_code=lang_code, title_approved=title_approved, coordinate=coordinate)
        if not is_valid:
            logger.end(log_message="Neighborhood was not inserted because no neighborhood name was provided")
            return None
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        neighborhood_json = {
                key: value for key, value in {
                    'coordinate': coordinate,
                    'city_id': city_id,
                    'group_id': group_id
                }.items() if value is not None
            }
        neighborhood_id = GenericCRUD.insert(self, data_json=neighborhood_json)

        neighborhood_ml_id = self.neighborhood_ml.insert(
            neighborhood=neighborhood, neighborhood_id=neighborhood_id,
            lang_code=lang_code, title_approved=title_approved)

        logger.end("end insert neighborhood",
                   object={'neighborhood_id': neighborhood_id,
                           'neighborhood_ml_id': neighborhood_ml_id})
        return neighborhood_id

    def read(self, location_id: int):
        logger.start("start read location",
                     object={'location_id': location_id})
        result = GenericCRUD.select_one_dict_by_id(
            self,
            id_column_value=location_id,
            select_clause_value=LocationLocalConstants.NEIGHBORHOOD_TABLE_COLUMNS)  # noqa501

        result = LocationsUtil.extract_coordinates_and_replace_by_point(
            data_json=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    @staticmethod
    def get_neighborhood_id_by_neighborhood_name(neighborhood_name: str, city_id: int = None,
                                                 lang_code: LangCode = None) -> int:
        # TODO should return also the city_id if known
        logger.start("start get_neighborhood_id_by_neighborhood_name",
                     object={'neighborhood_name': neighborhood_name,
                             'city_id': city_id})
        if neighborhood_name is None:
            logger.end(log_message="end get_neighborhood_id_by_neighborhood_name",
                       object={'neighborhood_id': None})
            return None
        LangCode.validate(lang_code)
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        where_clause = f"title='{neighborhood_name}' AND lang_code='{lang_code.value}'"
        # TODO: Shall we add city_id to neighborhood_ml_table and neighborhood_ml_view?
        # if city_id is not None:
        #     where_clause += f" AND city_id={city_id}"

        neighborhood_id_json = Neighborhood.neighborhood_ml.select_one_dict_by_where(  # noqa501
            select_clause_value=LocationLocalConstants.NEIGHBORHOOD_ID_COLUMN_NAME,  # noqa501
            where=where_clause,
            order_by="neighborhood_id DESC")
        neighborhood_id = neighborhood_id_json.get(
            LocationLocalConstants.NEIGHBORHOOD_ID_COLUMN_NAME)

        logger.end("end get_neighborhood_id_by_neighborhood_name",
                   object={'neighborhood_id': neighborhood_id})
        return neighborhood_id
