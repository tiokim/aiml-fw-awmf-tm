# ==================================================================================
#
#       Copyright (c) 2022 Samsung Electronics Co., Ltd. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ==================================================================================
import json
import requests
from unittest import mock
from mock import patch
import pytest
import flask
from requests.models import Response
from threading import Lock
import os
import sys
import datetime
from flask_api import status
from dotenv import load_dotenv
from threading import Lock
from trainingmgr import trainingmgr_main 
from trainingmgr.common import trainingmgr_operations
from trainingmgr.common.tmgr_logger import TMLogger
from trainingmgr.common.exceptions_utls import TMException
from trainingmgr.common.trainingmgr_util import MIMETYPE_JSON
from trainingmgr.common.trainingmgr_config import TrainingMgrConfig
trainingmgr_main.LOGGER = pytest.logger
trainingmgr_main.LOCK = Lock()
trainingmgr_main.DATAEXTRACTION_JOBS_CACHE = {}

class DummyVariable:
    kf_adapter_ip = "localhost"
    kf_adapter_port = 5001
    logger = trainingmgr_main.LOGGER

class Test_training_start:
    def setup_method(self): 
        self.client = trainingmgr_main.APP.test_client(self)
        self.logger = trainingmgr_main.LOGGER

    ts_result = Response()
    ts_result.status_code = status.HTTP_200_OK
    ts_result.headers={'content-type': MIMETYPE_JSON}
    @patch('trainingmgr.common.trainingmgr_operations.requests.post', return_value = ts_result)
    def test_success(self, mock1):
        trainingjob_name = "usecase12"
        dict_data = {
            "pipeline_name": "qoe",
            "experiment_name": "default",
            "arguments": "{epoches : 1}",
            "pipeline_version": 1
        }
        training_config_obj =  DummyVariable()
        try:
            response = trainingmgr_operations.training_start(training_config_obj,dict_data,trainingjob_name)
            assert response.headers['content-type'] == MIMETYPE_JSON
            assert response.status_code == status.HTTP_200_OK
        except Exception:
            assert False

    def test_fail(self):
        trainingjob_name = "usecase12"
        dict_data = {
            "pipeline_name": "qoe",
            "experiment_name": "default",
            "arguments": "{epoches : 1}",
            "pipeline_version": 1
        }
        training_config_obj =  DummyVariable()
        try:
            response = trainingmgr_operations.training_start(training_config_obj,dict_data,trainingjob_name)
            assert False
        except requests.exceptions.ConnectionError:
            assert True
        except Exception:
            assert False

class Test_create_dme_filtered_data_job:

    the_response=Response()
    the_response.status_code=status.HTTP_201_CREATED
    @patch('trainingmgr.common.trainingmgr_operations.requests.put', return_value=the_response)
    def test_success(self, mock1):
        mocked_TRAININGMGR_CONFIG_OBJ=mock.Mock(name="TRAININGMGR_CONFIG_OBJ")
        attrs_TRAININGMGR_CONFIG_OBJ = {'kf_adapter_ip.return_value': '123', 'kf_adapter_port.return_value' : '100'}
        mocked_TRAININGMGR_CONFIG_OBJ.configure_mock(**attrs_TRAININGMGR_CONFIG_OBJ)
        source_name=""
        db_org=""
        bucket_name=""
        token=""
        features=[]
        feature_group_name="test"
        host="10.0.0.50"
        port="31840"
        response=trainingmgr_operations.create_dme_filtered_data_job(mocked_TRAININGMGR_CONFIG_OBJ, source_name, db_org, bucket_name, token, features, feature_group_name, host, port)
        assert response.status_code==status.HTTP_201_CREATED, "create_dme_filtered_data_job failed"

    def test_create_url_host_port_fail(self):
        mocked_TRAININGMGR_CONFIG_OBJ=mock.Mock(name="TRAININGMGR_CONFIG_OBJ")
        attrs_TRAININGMGR_CONFIG_OBJ = {'kf_adapter_ip.return_value': '123', 'kf_adapter_port.return_value' : '100'}
        mocked_TRAININGMGR_CONFIG_OBJ.configure_mock(**attrs_TRAININGMGR_CONFIG_OBJ)
        source_name=""
        db_org=""
        bucket_name=""
        token=""
        features=[]
        feature_group_name="test"
        host="url error"
        port="31840"
        try:
            response=trainingmgr_operations.create_dme_filtered_data_job(mocked_TRAININGMGR_CONFIG_OBJ, source_name, db_org, bucket_name, token, features, feature_group_name, host, port)
            assert False
        except TMException as err:
            assert "URL validation error: " in err.message
        except Exception:
            assert False

class Test_delete_dme_filtered_data_job:

    the_response=Response()
    the_response.status_code=status.HTTP_204_NO_CONTENT
    @patch('trainingmgr.common.trainingmgr_operations.requests.delete', return_value=the_response)
    def test_success(self, mock1):
        mocked_TRAININGMGR_CONFIG_OBJ=mock.Mock(name="TRAININGMGR_CONFIG_OBJ")
        attrs_TRAININGMGR_CONFIG_OBJ = {'kf_adapter_ip.return_value': '123', 'kf_adapter_port.return_value' : '100'}
        mocked_TRAININGMGR_CONFIG_OBJ.configure_mock(**attrs_TRAININGMGR_CONFIG_OBJ)
        feature_group_name="test"
        host="10.0.0.50"
        port="31840"
        response=trainingmgr_operations.delete_dme_filtered_data_job(mocked_TRAININGMGR_CONFIG_OBJ, feature_group_name, host, port)
        assert response.status_code==status.HTTP_204_NO_CONTENT, "delete_dme_filtered_data_job failed"

    def test_create_url_host_port_fail(self):
        mocked_TRAININGMGR_CONFIG_OBJ=mock.Mock(name="TRAININGMGR_CONFIG_OBJ")
        attrs_TRAININGMGR_CONFIG_OBJ = {'kf_adapter_ip.return_value': '123', 'kf_adapter_port.return_value' : '100'}
        mocked_TRAININGMGR_CONFIG_OBJ.configure_mock(**attrs_TRAININGMGR_CONFIG_OBJ)
        feature_group_name="test"
        host="url error"
        port="31840"
        try:
            response=trainingmgr_operations.delete_dme_filtered_data_job(mocked_TRAININGMGR_CONFIG_OBJ, feature_group_name, host, port)
            assert False
        except TMException as err:
            assert "URL validation error: " in err.message
        except Exception:
            assert False
