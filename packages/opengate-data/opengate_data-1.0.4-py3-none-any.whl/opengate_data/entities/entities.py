'''  EntitiesBuilder '''

import requests
import pandas as pd
from typing import Callable, Union, List, Dict, Any


class EntitiesBuilder:
    ''' Builder entities'''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.filter_data: Dict[str, Any] = {}
        self.format_data: str = None
        self.default_sorted: bool = False
        self.case_sensitive: bool = False
        self.organization_name: str = None
        self.bulk_action: str = None
        self.bulk_type: str = None
        self.csv_data: str = None
        self.url: str = None
        self.method: str = None
        self.requires: Dict[str, Any] = {}
        self.select_data: Dict[str, Any] = {}
        self.headers: Dict[str, Any] = self.client.headers

    def with_filter(self, filter_data: Dict[str, Any]) -> 'EntitiesBuilder':
        ''' Filter '''
        self.filter_data = filter_data
        return self
      
    def with_select(self, select_data: Dict[str, Any]) -> 'EntitiesBuilder':
        ''' Select '''
        self.select_data = select_data
        return self

    def with_format(self, format_data: str) -> 'EntitiesBuilder':
        ''' Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas'). '''
        self.format_data = format_data
        return self

    def with_default_sorted(self, default_sorted: bool) -> 'EntitiesBuilder':
        ''' default sorted'''
        self.default_sorted = default_sorted
        return self
    
    def with_case_sensitive(self, case_sensitive: bool) -> 'EntitiesBuilder':
        ''' case sensitive'''
        self.case_sensitive = case_sensitive
        return self

    def search(self) -> 'EntitiesBuilder':
        ''' searching '''
        self.requires = {
            'default sorted': self.default_sorted,
            'filter_data': self.filter_data,
            'select_data': self.select_data
        }
        self.method = 'search'
        self.url = f'{self.client.url}/north/v80/search/entities?defaultSorted={self.default_sorted}'
        return self
    
    def with_organization_name(self, organization_name: str) -> 'EntitiesBuilder':
        ''' organization_name '''
        self.organization_name = organization_name
        return self
    
    def with_bulk_action(self, bulk_action: str) -> 'EntitiesBuilder':
        ''' bulk_action '''
        self.bulk_action = bulk_action
        return self
    
    def with_bulk_type(self, bulk_type: str) -> 'EntitiesBuilder':
        ''' bulk_type '''
        self.bulk_type = bulk_type
        return self
    
    def with_csv_data(self, csv_data: str) -> 'EntitiesBuilder':
        ''' csv_data '''
        self.csv_data = csv_data
        return self
    
    def bulk_provisioning(self) -> 'EntitiesBuilder':
        ''' bulk provisioning '''
        self.requires = {
            'organization_name': self.organization_name,
            'action': self.bulk_action,
            'type': self.bulk_type,
            'data': self.csv_data
        }
        self.method = 'bulk_provisioning'
        self.url = f'{self.client.url}/north/v80/provision/organizations/{self.organization_name}/bulk/async?action={self.bulk_action}&type={self.bulk_type}'
        return self

    def build(self) -> 'EntitiesBuilder':
        ''' Check if any parameter is missing. '''
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    def execute(self) -> Union[int, List[Dict[str, Any]]]:
        ''' Execute and return the responses '''
        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'search': self._execute_searching,
            'bulk_provisioning': self._execute_bulk_provisioning
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()
      
    def add_header(self, key: str, value: str) -> 'EntitiesBuilder':
        self.headers[key] = value

    def _execute_searching(self) -> Union[int, List[Dict[str, Any]]]:
        response = self._send_request()
        if response.status_code == 200:
          if self.format_data is 'csv':
            return response.text
          else:
            data = response.json()
            flat_entities = self._flatten_entities(data['entities'])
            return self._format_data(flat_entities)
        return response

    def _execute_bulk_provisioning(self) -> Union[int, List[Dict[str, Any]]]:
        print(self.csv_data)
        response = requests.post(self.url, headers=self.headers, data=self.csv_data, verify=False, timeout=3000)
        return response

    def _send_request(self) -> requests.Response:
        body = {}
        
        if(self.filter_data is not None):
          body['filter'] = self.filter_data
          
        if(self.select_data is not None):
          body['select'] = self.select_data
          
        return requests.post(self.url, headers=self.headers, json=body, verify=False, timeout=3000)

    def _flatten_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        flat_entities = []
        for entity in entities:
            flat_entity = self._flatten_entity(entity)
            flat_entities.append(flat_entity)
        return flat_entities

    def _flatten_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        flat_entity = {}
        for entity_key, entity_value in entity.items():
            for key_level_1, value_level_1 in entity_value.items():
                self._process_entity(entity_key, key_level_1, value_level_1, flat_entity)
        return flat_entity

    def _process_entity(self, entity_prefix: str, key_prefix: str, value_dict: Any, flat_entity: Dict[str, Any]) -> None:
        if isinstance(value_dict, list):
            for i, item in enumerate(value_dict):
                for sub_key, sub_value in item.items():
                    new_key = f'{entity_prefix}_{key_prefix}_{i}_{sub_key}'
                    self._assign_value(new_key, sub_value, flat_entity)
        else:
            for sub_key, sub_value in value_dict.items():
                new_key = f'{entity_prefix}_{key_prefix}_{sub_key}'
                self._assign_value(new_key, sub_value, flat_entity)

    def _assign_value(self, key: str, value: Any, flat_entity: Dict[str, Any]) -> None:
        if isinstance(value, dict) and '_current' in value:
            flat_entity[key] = value['_current']['value']
        else:
            flat_entity[key] = value

    def _format_data(self, flat_entities: List[Dict[str, Any]]) -> Union[str, List[Dict[str, Any]], pd.DataFrame]:
        if self.format_data == 'csv':
            return self._format_as_csv(flat_entities)
        elif self.format_data == 'dict':
            return flat_entities
        elif self.format_data == 'pandas':
            return pd.DataFrame(flat_entities)
        else:
            raise ValueError('Format not valid')

    def _format_as_csv(self, flat_entities: List[Dict[str, Any]]) -> str:
        columnas = flat_entities[0].keys()
        csv_string = ','.join(columnas) + '\n'
        for flat_entity in flat_entities:
            fila = list(flat_entity.values())
            csv_string += ','.join(map(str, fila)) + '\n'
        return csv_string
