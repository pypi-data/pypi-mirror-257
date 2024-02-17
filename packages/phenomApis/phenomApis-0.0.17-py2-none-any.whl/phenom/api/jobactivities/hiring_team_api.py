# coding: utf-8

"""
    jobs-activities-api

    These API's allows you to perform activities on Jobs  # noqa: E501

    OpenAPI spec version: 1.0.3
    
    Generated by: phenom
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from phenom.commons.api_client import ApiClient


class HiringTeamApi(object):
    base_path = "/jobs-api/activities"  # your base path

    def __init__(self, token, gateway_url, apikey, api_client=None):
        if api_client is None:
            api_client = ApiClient(gateway_url + self.base_path, apikey, token)
        self.api_client = api_client

    def get_hiring_team(self, job_id, x_ph_userid, **kwargs):  # noqa: E501
        """Get Hiring team  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_hiring_team(job_id, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: job id (required)
        :param str x_ph_userid: (required)
        :return: HiringTeam
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_hiring_team_with_http_info(job_id, x_ph_userid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_hiring_team_with_http_info(job_id, x_ph_userid, **kwargs)  # noqa: E501
            return data

    def get_hiring_team_with_http_info(self, job_id, x_ph_userid, **kwargs):  # noqa: E501
        """Get Hiring team  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_hiring_team_with_http_info(job_id, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: job id (required)
        :param str x_ph_userid: (required)
        :return: HiringTeam
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['job_id', 'x_ph_userid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_hiring_team" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `get_hiring_team`")  # noqa: E501
        # verify the required parameter 'x_ph_userid' is set
        if ('x_ph_userid' not in params or
                params['x_ph_userid'] is None):
            raise ValueError("Missing the required parameter `x_ph_userid` when calling `get_hiring_team`")  # noqa: E501

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
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/v1/jobs/{jobId}/hiring-team', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='HiringTeam',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_hiring_team(self, body, x_ph_userid, job_id, **kwargs):  # noqa: E501
        """Update Hiring Team  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_hiring_team(body, x_ph_userid, job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateJobsHiringTeamRequest body: update JobsHiringTeam (required)
        :param str x_ph_userid: (required)
        :param str job_id: jobId (required)
        :return: UpdateHiringTeamResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_hiring_team_with_http_info(body, x_ph_userid, job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_hiring_team_with_http_info(body, x_ph_userid, job_id, **kwargs)  # noqa: E501
            return data

    def update_hiring_team_with_http_info(self, body, x_ph_userid, job_id, **kwargs):  # noqa: E501
        """Update Hiring Team  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_hiring_team_with_http_info(body, x_ph_userid, job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param UpdateJobsHiringTeamRequest body: update JobsHiringTeam (required)
        :param str x_ph_userid: (required)
        :param str job_id: jobId (required)
        :return: UpdateHiringTeamResponse
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
                    " to method update_hiring_team" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `update_hiring_team`")  # noqa: E501
        # verify the required parameter 'x_ph_userid' is set
        if ('x_ph_userid' not in params or
                params['x_ph_userid'] is None):
            raise ValueError("Missing the required parameter `x_ph_userid` when calling `update_hiring_team`")  # noqa: E501
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `update_hiring_team`")  # noqa: E501

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
            '/v1/jobs/{jobId}/hiring-team', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateHiringTeamResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
