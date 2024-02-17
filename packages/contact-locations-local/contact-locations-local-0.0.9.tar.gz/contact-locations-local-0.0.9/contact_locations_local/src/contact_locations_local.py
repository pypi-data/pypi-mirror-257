from .contact_locations_local_constants import CONTACT_LOCATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from database_mysql_local.generic_mapping import GenericMapping
from location_local.locations_local_crud import LocationsLocal
from language_remote.lang_code import LangCode
from user_context_remote.user_context import UserContext
from logger_local.LoggerLocal import Logger
from location_local.city import City
from location_local.state import State
from location_local.country import Country
from location_local.county import County
from location_local.region import Region
from location_local.neighborhood import Neighborhood
import pycountry
import phonenumbers


DEFAULT_SCHEMA_NAME = "contact_location"
DEFAULT_ENTITY_NAME1 = "contact"
DEFAULT_ENTITY_NAME2 = "location"
DEFAULT_ID_COLUMN_NAME = "contact_location_id"
DEFAULT_TABLE_NAME = "contact_location_table"
DEFAULT_VIEW_TABLE_NAME = "contact_location_view"
# TODO Move those to group_category.py in group-local-python-package, we'll generate this file using sql2code
# TODO develop file group_category.py in group-local-python-package
STATE_THEY_LIVE_IN_GROUP_CATEGORY = 501
CITY_THEY_LIVE_IN_GROUP_CATEGORY = 201

logger = Logger.create_logger(
    object=CONTACT_LOCATIONS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

user_context = UserContext.login_using_user_identification_and_password()


class ContactLocationsLocal(GenericMapping):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2, default_id_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME, default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 lang_code: LangCode = None, is_test_data: bool = False) -> None:

        GenericMapping.__init__(
            self, default_schema_name=default_schema_name, default_entity_name1=default_entity_name1,
            default_entity_name2=default_entity_name2, default_id_column_name=default_id_column_name,
            default_table_name=default_table_name, default_view_table_name=default_view_table_name,
            is_test_data=is_test_data)
        self.locations_local = LocationsLocal()
        self.lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        self.is_test_data = is_test_data
        self.profile_id = user_context.get_effective_profile_id()


    def insert_contact_and_link_to_location(self, location_information: dict, contact_id: int) -> dict:
        """
        Process city information create city group if not exist and add city to city group
        and linking the contact to the city
        :param location_info: location information: dict
        dict keys:
        - coordinate : Point
        - city : dict
        - state : dict
        - country : dict
        - region : dict
        - neighborhood : dict
        :param contact_id: contact id

        """
        logger.start("process_location", object={
                     'location_information': location_information, 'contact_id': contact_id})
        city_name = location_information['city']
        state_name = location_information['state']
        county_name = location_information['county']
        country_name = location_information['country']
        region_name = location_information['region']
        neighborhood_name = location_information['neighborhood']
        coordinate = location_information['coordinate']

        # insert to database temporary ignore duplicate entry exception
        try:
            country_data = {}
            country_id = Country().get_country_id_by_country_name(country_name=country_name)
            if country_id is None:
                country_information = self.get_country_information(
                    country_name=country_name)
                country_data.update({
                    'coordinate': coordinate,
                    'iso': country_information.get("alpha_2"),
                    'name': country_name,
                    'iso3': country_information.get("alpha_3"),
                    'numcode': country_information.get("numeric"),
                    'plus_code': country_information.get("plus_code"),
                })
                country_id = Country().insert(country=country_name,
                                              lang_code=self.lang_code,
                                              new_country_data=country_data, coordinate=coordinate)

            state_id = State().get_state_id_by_state_name(
                state_name=state_name, country_id=country_id)
            if state_id is None:
                group_id = self.select_one_dict_by_where(schema_name='group', view_table_name='group_ml_view',
                                                         select_clause_value='group_id',
                                                         where='title = %s', params=(state_name,))
                if group_id is None:
                    group_json = {
                        'is_state': True,
                        'group_category_id': STATE_THEY_LIVE_IN_GROUP_CATEGORY,
                        'is_test_data': self.is_test_data,
                        'profile_id': self.profile_id,
                    }
                    group_id = self.insert(
                        schema_name='group', table_name='group_table', data_json=group_json)
                state_id = State().insert(state=state_name,
                                          lang_code=self.lang_code,
                                          country_id=country_id,
                                          group_id=group_id)

            city_id = City().get_city_id_by_city_name_state_id(
                city_name=city_name, state_id=state_id)
            if city_id is None:
                group_id = self.select_one_dict_by_where(schema_name='group', view_table_name='group_ml_view',
                                                         select_clause_value='group_id',
                                                         where='title = %s', params=(city_name,))
                if group_id is None:
                    group_json = {
                        'is_city': True,
                        'group_category_id': CITY_THEY_LIVE_IN_GROUP_CATEGORY,
                        'is_test_data': self.is_test_data,
                        'profile_id': self.profile_id,
                    }
                    group_id = self.insert(
                        schema_name='group', table_name='group_table', data_json=group_json)
                city_id = City().insert(city=city_name, lang_code=self.lang_code,
                                        coordinate=coordinate, group_id=group_id)

            county_id = County().get_county_id_by_county_name_state_id(
                county_name=county_name, state_id=state_id)
            if county_id is None:
                group_id = self.select_one_dict_by_where(schema_name='group', view_table_name='group_ml_view',
                                                         select_clause_value='group_id',
                                                         where='title = %s', params=(county_name,))
                if group_id is None:
                    group_json = {
                        'is_county': True,
                        'group_category_id': None,  # TODO: add group category for county
                        'is_test_data': self.is_test_data,
                        'profile_id': self.profile_id,
                    }
                    group_id = self.insert(
                        schema_name='group', table_name='group_table', data_json=group_json)
                county_id = County().insert(county=county_name,
                                            lang_code=self.lang_code,
                                            coordinate=coordinate,
                                            group_id=group_id)

            region_id = Region().get_region_id_by_region_name(
                region_name=region_name, country_id=country_id)
            if region_id is None:
                group_id = self.select_one_dict_by_where(schema_name='group', view_table_name='group_ml_view',
                                                         select_clause_value='group_id',
                                                         where='title = %s', params=(region_name,))
                if group_id is None:
                    group_json = {
                        'is_region': True,
                        'group_category_id': None,  # TODO: add group category for region
                        'is_test_data': self.is_test_data,
                        'profile_id': self.profile_id,
                    }
                    group_id = self.insert(
                        schema_name='group', table_name='group_table', data_json=group_json)
                region_id = Region().insert(region=region_name,
                                            lang_code=self.lang_code,
                                            coordinate=coordinate,
                                            country_id=country_id,
                                            group_id=group_id)

            neighborhood_id = Neighborhood().get_neighborhood_id_by_neighborhood_name(
                neighborhood_name=neighborhood_name, city_id=city_id)
            if neighborhood_id is None:
                group_id = self.select_one_dict_by_where(schema_name='group', view_table_name='group_ml_view',
                                                         select_clause_value='group_id',
                                                         where='title = %s', params=(neighborhood_name,))
                if group_id is None:
                    group_json = {
                        'is_neighborhood': True,
                        'group_category_id': None,  # TODO: add group category for neighborhood
                        'is_test_data': self.is_test_data,
                        'profile_id': self.profile_id,
                    }
                    group_id = self.insert(
                        schema_name='group', table_name='group_table', data_json=group_json)
                neighborhood_id = Neighborhood().insert(neighborhood=neighborhood_name,
                                                        lang_code=self.lang_code,
                                                        coordinate=coordinate,
                                                        city_id=city_id,
                                                        group_id=group_id)

            location_info = {
                'coordinate': coordinate,
                'city_id': city_id,
                'state_id': state_id,
                'county_id': county_id,
                'country_id': country_id,
                'region_id': region_id,
                'neighborhood_id': neighborhood_id,
                'is_test_data': self.is_test_data,
                'plus_code': country_data.get('plus_code'),
            }

            location_id = self.locations_local.insert(data=location_info,
                                                      lang_code=self.lang_code,
                                                      is_test_data=self.is_test_data)

            contact_location_id = self.insert_mapping(schema_name='contact_location',
                                                      entity_name1=self.default_entity_name1,
                                                      entity_name2=self.default_entity_name2,
                                                      entity_id1=contact_id,
                                                      entity_id2=location_id,
                                                      data_json={'contact_id': contact_id, 'location_id': location_id})
            location_result = {
                'location_id': location_id,
                'contact_location_id': contact_location_id,
            }
            logger.end(log_message="location successfully processed",
                       object={"location_result": location_result})
            return location_result
        except Exception as e:
            logger.exception("error in process_location" + str(e))
            raise e

    def get_country_information(country_name: str) -> dict:
        """
        Get country information by country name
        :param country_name: country name
        :return: country information: dict
        example:
        {
            "alpha_2(iso2)": "IL",  :str
            "name": "Israel", :str 
            "alpha_3(iso3)": "ISR", :str
            "flag": "🇮🇱", :str
            "numeric": 376, :str
            "plus_code": 972 :int
        }
        """
        try:
            # Check if input is a country name
            country = pycountry.countries.get(
                name=country_name).__dict__.get('_fields')
            if country:
                country_alpha_2 = country.get('alpha_2')
                country_code = phonenumbers.COUNTRY_CODE_TO_REGION_CODE.keys()
                for code in country_code:
                    if country_alpha_2 in phonenumbers.COUNTRY_CODE_TO_REGION_CODE[code]:
                        country['plus_code'] = code
                        break
                return country
        except Exception as exception:
            logger.exception("error in get_country_information" + str(exception))
            logger.exception(str(exception))
            raise exception
        return None
