# coding=utf-8
import json
import os, sys
import hashlib
import hmac
import base64
import urllib
import time
import uuid
import requests


def get_iso8601_time():
    '''返回iso8601格式的时间'''
    TIME_ZONE = "GMT"
    FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%SZ"
    return time.strftime(FORMAT_ISO8601, time.gmtime())


def get_uuid():
    '''返回uuid'''
    return str(uuid.uuid4())


def get_parameters(user_param, Action, AccessKeyId, Version):
    '''
    拼接参数字典
    user_param: {"RegionId":"cn-beijing", "LoadBalancerName":"test-node1", "AddressType":"intranet", "VSwitchId":"vsw-2zevjlczuvp2mkhhch12x"}
    Action操作例如:CreateLoadBalancer
    AccessKeyId：access key ID
    Version: 接口的版本
    '''
    parameters = {}
    parameters['HTTPMethod'] = 'GET'
    parameters['AccessKeyId'] = AccessKeyId
    parameters['Format'] = 'json'
    parameters['Version'] = Version
    parameters['SignatureMethod'] = 'HMAC-SHA1'
    parameters['Timestamp'] = get_iso8601_time()
    parameters['SignatureVersion'] = '1.0'
    parameters['SignatureNonce'] = get_uuid()
    parameters['Action'] = Action
    for (k, v) in sorted(user_param.items()):
        parameters[k] = v
    return parameters


def get_param(parameters):
    '''把公共参数拼接成字符串'''
    param_str = ''
    for (k, v) in sorted(parameters.items()):
        param_str += "&" + urllib.quote(k, safe='') + "=" + urllib.quote(v, safe='')
    param_str = param_str[1:]
    return param_str


def get_StringToSign(parameters, param_str):
    '''拼接生成签名的字符串'''
    StringToSign = parameters['HTTPMethod'] + "&%2F&" + urllib.quote(param_str, safe='')
    return StringToSign


def get_signature(StringToSign, AccessKeySecret):
    '''构建签名'''
    h = hmac.new(AccessKeySecret, StringToSign, hashlib.sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def build_request(server_url, param_str, signature, AccessKeySecret):
    '''拼接url并进行请求'''
    Signature = "Signature=" + urllib.quote(signature)
    param = param_str + "&" + Signature
    request_url = server_url + param
    s = requests.get(request_url)
    print s.content
    print s
    return s

def get_regions(server_url, Action, user_param, AccessKeySecret, AccessKeyId, Version):
    '''对请求进行模块
    server_url： slb.aliyun.com
    Action = 'DescribeRegions'
    AccessKeySecret, AccessKeyId:也就是ak
    user_param = {'LoadBalancerId': 'lb-2zekxu2elibyexxoo9hlw'}
    Version:例如slb的版本是2014-05-15,每个服务都不相同
    '''
    server_url = 'https://' + server_url + '/?'
    AccessKeySecret = AccessKeySecret
    AccessKeyId = AccessKeyId
    parameters = get_parameters(user_param, Action, AccessKeyId, Version)
    param_str = get_param(parameters)
    StringToSign = get_StringToSign(parameters, param_str)
    signature = get_signature(StringToSign, AccessKeySecret + '&')
    Message = build_request(server_url, param_str, signature, AccessKeySecret)
    return Message

def describe_VServerGroups():
    Action = 'DescribeVServerGroups'
    user_param = {'RegionId': 'cn-shenzhen',
                  'LoadBalancerId': 'lb-wz9726knlldtqsdfu5oqu',
                  'IncludeRule': 'true',
                  'IncludeListener': 'true'
                  }
    server_url = 'slb.aliyuncs.com'
    Version = '2014-05-15'
    AccessKeySecret='hldIvCwDIgwg4Zc2lZimaaTL4AAZvK'
    AccessKeyId='LTAI4GAXUGonK6WtjG2dmjuA'
    message = get_regions(server_url, Action, user_param, AccessKeySecret, AccessKeyId, Version)
    print "======================%s" %message
    print json.dumps(message.content)
def modify_VServerGroupBackendServers(OldBackendServers,NewBackendServers):
    Action = 'ModifyVServerGroupBackendServers'
    user_param = {'RegionId': 'cn-shenzhen',
                  'VServerGroupId': 'rsp-wz9yagr8d02lu',
                  'OldBackendServers': OldBackendServers,
                  'NewBackendServers': NewBackendServers,
                  }
    server_url = 'slb.aliyuncs.com'
    Version = '2014-05-15'
    AccessKeySecret='hldIvCwDIgwg4Zc2lZimaaTL4AAZvK'
    AccessKeyId='LTAI4GAXUGonK6WtjG2dmjuA'
    message = get_regions(server_url, Action, user_param, AccessKeySecret, AccessKeyId, Version)
    print "======================%s" %message
    print json.dumps(message.content)

if __name__=='__main__':

    OldBackendServers=''
    OldBackendServers=''
    new_master_host='10.128.146.195'
    if new_master_host=='10.128.146.185':
        OldBackendServers = '[{ "ServerId": "i-wz949h0dw8516dvkwd2o",' \
                            '"Weight": "100",' \
                            '"Type": "ecs",' \
                            '"Port":"3306"}]'
        NewBackendServers = '[{ "ServerId": "i-wz96dai3e434sqzii3tb",' \
                            '"Weight": "100",' \
                            '"Type": "ecs",' \
                            '"Port":"3306"}]'
    elif new_master_host=='10.128.146.195':
        OldBackendServers = '[{ "ServerId": "i-wz96dai3e434sqzii3tb",' \
                            '"Weight": "100",' \
                            '"Type": "ecs",' \
                            '"Port":"3306"}]'
        NewBackendServers = '[{ "ServerId": "i-wz949h0dw8516dvkwd2o",' \
                            '"Weight": "100",' \
                            '"Type": "ecs",' \
                            '"Port":"3306"}]'
    modify_VServerGroupBackendServers(OldBackendServers,NewBackendServers)