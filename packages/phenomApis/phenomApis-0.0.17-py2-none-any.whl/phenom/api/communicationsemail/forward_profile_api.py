# coding: utf-8

"""
    communications-email

    These APIs ensures an easy integration process of email management for developers to send, read, and track email histories within applications.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: phenom
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from phenom.commons.api_client import ApiClient


class ForwardProfileApi(object):
    base_path = "/communications/email"  # your base path

    def __init__(self, token, gateway_url, apikey, api_client=None):
        if api_client is None:
            api_client = ApiClient(gateway_url + self.base_path, apikey, token)
        self.api_client = api_client

    def forward_candidate_profile(self, body, x_ph_userid, **kwargs):  # noqa: E501
        """Forward Candidate Profile  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forward_candidate_profile(body, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ForwardProfileRequest body: (required)
        :param str x_ph_userid: (required)
        :return: ForwardProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forward_candidate_profile_with_http_info(body, x_ph_userid, **kwargs)  # noqa: E501
        else:
            (data) = self.forward_candidate_profile_with_http_info(body, x_ph_userid, **kwargs)  # noqa: E501
            return data

    def forward_candidate_profile_with_http_info(self, body, x_ph_userid, **kwargs):  # noqa: E501
        """Forward Candidate Profile  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forward_candidate_profile_with_http_info(body, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ForwardProfileRequest body: (required)
        :param str x_ph_userid: (required)
        :return: ForwardProfileResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'x_ph_userid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forward_candidate_profile" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `forward_candidate_profile`")  # noqa: E501
        # verify the required parameter 'x_ph_userid' is set
        if ('x_ph_userid' not in params or
                params['x_ph_userid'] is None):
            raise ValueError("Missing the required parameter `x_ph_userid` when calling `forward_candidate_profile`")  # noqa: E501

        collection_formats = {}

        path_params = {}

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
            '/v1/forward-profile', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ForwardProfileResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_forward_profile_activities(self, email, x_ph_userid, **kwargs):  # noqa: E501
        """Forward Profile Activity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_forward_profile_activities(email, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str email: (required)
        :param str x_ph_userid: (required)
        :param int offset:
        :param int limit:
        :param str communication_id:
        :return: ForwardProfileActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_forward_profile_activities_with_http_info(email, x_ph_userid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_forward_profile_activities_with_http_info(email, x_ph_userid, **kwargs)  # noqa: E501
            return data

    def get_forward_profile_activities_with_http_info(self, email, x_ph_userid, **kwargs):  # noqa: E501
        """Forward Profile Activity  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_forward_profile_activities_with_http_info(email, x_ph_userid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str email: (required)
        :param str x_ph_userid: (required)
        :param int offset:
        :param int limit:
        :param str communication_id:
        :return: ForwardProfileActivity
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['email', 'x_ph_userid', 'offset', 'limit', 'communication_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_forward_profile_activities" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'email' is set
        if ('email' not in params or
                params['email'] is None):
            raise ValueError("Missing the required parameter `email` when calling `get_forward_profile_activities`")  # noqa: E501
        # verify the required parameter 'x_ph_userid' is set
        if ('x_ph_userid' not in params or
                params['x_ph_userid'] is None):
            raise ValueError("Missing the required parameter `x_ph_userid` when calling `get_forward_profile_activities`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'communication_id' in params:
            query_params.append(('communicationId', params['communication_id']))  # noqa: E501
        if 'email' in params:
            query_params.append(('email', params['email']))  # noqa: E501

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
            '/v1/forward-profile/activity', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ForwardProfileActivity',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
