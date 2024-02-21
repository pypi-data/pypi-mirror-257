# coding: utf-8

# Copyright 2024 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from typing import Tuple

from ibm_cloud_sdk_core import BaseService
from ibm_watson_openscale.supporting_classes.enums import TargetTypes

from ibm_watson_openscale.utils.utils import *
from ibm_watson_openscale.utils.client_errors import *

class WOS():
    """
    Manages Utility methods at the Watson OpenScale level.
    """

    def __init__(self, ai_client: 'WatsonOpenScaleV2Adapter', service_url: str) -> None:
        validate_type(ai_client, 'ai_client', BaseService, True)        
        self._ai_client = ai_client  
        self.service_url = service_url
    
    def get_instance_mapping(self, project_id: str = None, space_id: str  = None):
        
        """
        Get all instance mappings specified by the parameters filtered by either of project_id or space_id
        
        Note: This operation is applicable only for Cloud Pack for Data env

        :param str project_id: (optional) Project id with which mapping has to be done
        :param str space_id: (optional) Space id with which mapping has to be done
        :rtype: dict

        A way you might use me is:

        >>> from ibm_watson_openscale import *
        >>> client.wos.get_instance_mapping(                
                project_id=project_id                
             )
        """
        
        if self._ai_client.is_cp4d is not True:
            raise AuthorizationError("This operation is allowed only on CP4D environment")
                
        if project_id == None and space_id == None:
            raise ParameterError("Provide value for either project_id or space_id")
        
        if project_id is not None and space_id is not None:
            raise ParameterError("Provide value for project_id or space_id but not both")
        
        url = '{0}/openscale/v2/instance_mappings'.format(self.service_url)        
        if project_id is not None:
            url = '{0}?project_id={1}'.format(url, project_id)
        
        if space_id is not None:
            url = '{0}?space_id={1}'.format(url, space_id)        
            
        headers = {
            'Accept': 'application/json',
            'Authorization': "Bearer {}".format(self._ai_client.authenticator.token_manager.get_token())
        }
        
        response =  requests.get(url, headers=headers,verify=False)
        return response.json()
            
    def add_instance_mapping(self, service_instance_id: str = None, project_id: str = None, space_id: str  = None):
        
        """
        Create instance mapping between OpenScale service instance and with either space or project.
        
        Note: This operation is applicable only for Cloud Pack for Data env

        :param str service_instance_id: Service instance id.
        :param str project_id: (optional) Project id with which mapping has to be done
        :param str space_id: (optional) Space id with which mapping has to be done
        :rtype: dict

        A way you might use me is:

        >>> from ibm_watson_openscale import *
        >>> client.wos.add_instance_mapping(                
                service_instance_id=service_instance_id,
                project_id=project_id                
             )
        """
        
        if self._ai_client.is_cp4d is not True:
            raise AuthorizationError("This operation is allowed only on CP4D environment")
        
        validate_type(service_instance_id, 'service_instance_id', str, True)
        
        if project_id == None and space_id == None:
            raise ParameterError("Provide value for either project_id or space_id")
        
        if project_id is not None and space_id is not None:
            raise ParameterError("Provide value for project_id or space_id but not both")
        
        target = {
            "target_type" : TargetTypes.PROJECT if project_id is not None else TargetTypes.SPACE,
            "target_id": project_id if project_id is not None else space_id
        }

        url = '{}/openscale/v2/instance_mappings'.format(self.service_url)
        headers = {
            'Content-type': 'application/json',
            'Authorization': "Bearer {}".format(self._ai_client.authenticator.token_manager.get_token())
        }                 
        payload = {
            "service_instance_id": service_instance_id,
            "target": target
        }
        
        response = requests.post(url, json=payload, headers=headers, verify=False)   
        
        if response.status_code!=201:
            raise ApiRequestFailure("Failed to create instance mapping. Error {}".format(response.text),response)  
        
        return response.json()
        