from .location_local_constants import LocationLocalConstants
from .point import Point
from language_remote.lang_code import LangCode


class LocationsUtil:
    @staticmethod
    def extract_coordinates_and_replace_by_point(
            data_json: dict,
            point_column_name: str = None) -> dict:
        point_column_name = point_column_name or LocationLocalConstants.DEFAULT_POINT_COLUMN_NAME  # noqa501

        # Extract longitude and latitude values
        longitude = data_json.pop(f'ST_X({point_column_name})', None)
        latitude = data_json.pop(f'ST_Y({point_column_name})', None)

        if longitude is not None and latitude is not None:
            # Create Point object
            point = Point(longitude=longitude, latitude=latitude)

            # Add 'point' key to the dictionary
            data_json['point'] = point

        return data_json

    @staticmethod
    def validate_insert_args(name: str, lang_code: LangCode, title_approved: bool, coordinate: Point) -> bool:
        LangCode.validate(lang_code)
        if not name:
            return False
        elif title_approved is not None and not isinstance(title_approved, bool):
            raise ValueError('title_approved must be an instance of bool or None')
        elif coordinate is not None and not isinstance(coordinate, Point):
            raise ValueError('coordinate must be an instance of Point or None')
        return True
