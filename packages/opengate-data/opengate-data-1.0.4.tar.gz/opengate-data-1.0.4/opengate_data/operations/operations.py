'''  OperationsBuilder '''

import requests
from typing import Callable, Union, List, Dict, Any


class OperationsBuilder:
    ''' Builder operations'''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.default_sorted: bool = False
        self.case_sensitive: bool = False
        self.filter_data: Dict[str, Any] = {}
        self.url: str = None
        self.method: str = None
        self.requires: Dict[str, Any] = {}
        self.headers: Dict[str, Any] = self.client.headers

    def with_filter(self, filter_data: Dict[str, Any]) -> 'OperationsBuilder':
        ''' Filter '''
        self.filter_data = filter_data
        return self

    def with_default_sorted(self, default_sorted: bool) -> 'OperationsBuilder':
        ''' default sorted'''
        self.default_sorted = default_sorted
        return self
    
    def with_case_sensitive(self, case_sensitive: bool) -> 'OperationsBuilder':
        ''' default sorted'''
        self.case_sensitive = case_sensitive
        return self
    
    def add_header(self, key: str, value: str) -> 'OperationsBuilder':
        self.headers[key] = value
    
    def search(self) -> 'OperationsBuilder':
        ''' Searching '''
        self.requires = {
            'default_sorted': self.default_sorted,
            'case_sensitive': self.case_sensitive,
            'filter_data': self.filter_data
        }
        self.method = 'search'
        self.url = f'{self.client.url}/north/v80/search/entities/operations/history?utc=true&defaultSorted={self.default_sorted}&caseSensitive={self.case_sensitive}'
        return self
    
    def build(self) -> 'OperationsBuilder':
        ''' Check if any parameter is missing. '''
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    def execute(self) -> Union[int, List[Dict[str, Any]]]:
        ''' Execute and return the responses '''
        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'search': self._execute_searching
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_searching(self) -> Union[int, List[Dict[str, Any]]]:
        response = self._send_request()
        return response.text
    

    def _send_request(self) -> requests.Response:
        body = {}
        
        if(self.filter_data is not None):
          body['filter'] = self.filter_data
          
        return requests.post(self.url, headers=self.headers, json=body, verify=False, timeout=3000)
