# coding: utf-8

"""
    jobs-questionnarie-api

    These APIs streamline question management, providing tools to create, delete, and update questions. Additionally, they offer functionality to attach question lists to specific job profiles.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from phenom.commons.api_client import ApiClient


class JobQuestionnaireApi(object):
    base_path = "/jobs-api/questionnarie"  # your base path

    def __init__(self, token, gateway_url, apikey, api_client=None):
        if api_client is None:
            api_client = ApiClient(gateway_url + self.base_path, apikey, token)
        self.api_client = api_client

    def create_job_questionnarie(self, body, x_ph_userid, job_id, **kwargs):  # noqa: E501
        """Creates Job Questionnaire  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_job_questionnarie(body, x_ph_userid, job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateJobQuestionnarieRequest body: Create Job Questionnarie. (required)
        :param str x_ph_userid: (required)
        :param str job_id: jobId (required)
        :return: JobQuestionnarieCreationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_job_questionnarie_with_http_info(body, x_ph_userid, job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_job_questionnarie_with_http_info(body, x_ph_userid, job_id, **kwargs)  # noqa: E501
            return data

    def create_job_questionnarie_with_http_info(self, body, x_ph_userid, job_id, **kwargs):  # noqa: E501
        """Creates Job Questionnaire  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_job_questionnarie_with_http_info(body, x_ph_userid, job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateJobQuestionnarieRequest body: Create Job Questionnarie. (required)
        :param str x_ph_userid: (required)
        :param str job_id: jobId (required)
        :return: JobQuestionnarieCreationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_ph_userid', 'job_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_job_questionnarie" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_job_questionnarie`")  # noqa: E501
        # verify the required parameter 'x_ph_userid' is set
        if ('x_ph_userid' not in params or
                params['x_ph_userid'] is None):
            raise ValueError("Missing the required parameter `x_ph_userid` when calling `create_job_questionnarie`")  # noqa: E501
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `create_job_questionnarie`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'job_id' in params:
            path_params['jobId'] = params['job_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_ph_userid' in params:
            header_params['x-ph-userid'] = params['x_ph_userid']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/jobs/{jobId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='JobQuestionnarieCreationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_job_questionnaire(self, job_id, template_id, x_ph_userid, **kwargs):  # noqa: E501
        """Delete Job-Questionnarie  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_job_questionnaire(job_id, template_id, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: jobId (required)
        :param str template_id: (required)
        :param str x_ph_userid: (required)
        :return: QuestionnarieDeletionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_job_questionnaire_with_http_info(job_id, template_id, x_ph_userid, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_job_questionnaire_with_http_info(job_id, template_id, x_ph_userid, **kwargs)  # noqa: E501
            return data

    def delete_job_questionnaire_with_http_info(self, job_id, template_id, x_ph_userid, **kwargs):  # noqa: E501
        """Delete Job-Questionnarie  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_job_questionnaire_with_http_info(job_id, template_id, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: jobId (required)
        :param str template_id: (required)
        :param str x_ph_userid: (required)
        :return: QuestionnarieDeletionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['job_id', 'template_id', 'x_ph_userid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_job_questionnaire" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `delete_job_questionnaire`")  # noqa: E501
        # verify the required parameter 'template_id' is set
        if ('template_id' not in params or
                params['template_id'] is None):
            raise ValueError("Missing the required parameter `template_id` when calling `delete_job_questionnaire`")  # noqa: E501
        # verify the required parameter 'x_ph_userid' is set
        if ('x_ph_userid' not in params or
                params['x_ph_userid'] is None):
            raise ValueError("Missing the required parameter `x_ph_userid` when calling `delete_job_questionnaire`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'job_id' in params:
            path_params['jobId'] = params['job_id']  # noqa: E501
        if 'template_id' in params:
            path_params['templateId'] = params['template_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_ph_userid' in params:
            header_params['x-ph-userid'] = params['x_ph_userid']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/jobs/{jobId}/{templateId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='QuestionnarieDeletionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
