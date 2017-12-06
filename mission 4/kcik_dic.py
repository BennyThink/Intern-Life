#!/usr/bin/python
# coding:utf-8

# Intern-Life - kcik_dic_file.py
# 2017/11/24 16:35
# kick boolean false key-value in dict. Recursive.

__author__ = 'Benny <benny@bennythink.com>'

sample = {
    "delete_final": {},
    "delete01": 0,
    "data": {
        "ip": "210.75.225.254",
        "country": "\u4e2d\u56fd",
        "area": "\u534e\u5317",
        "region": "\u5317\u4eac\u5e02",
        "city": "\u5317\u4eac\u5e02",
        "county": "",
        "isp": "\u7535\u4fe1",
        "country_id": "86",
        "area_id": "100000",
        "region_id": "110000",
        "city_id": "110000",
        "county_id": "-1",
        "isp_id": "100017",
        "delete7": None
    },
    "note": {
        "delete0": '',
        "delete5": {},
        "no delete5": [1, 2],
        "test4": "hello",
        "test5": 1
    },
    "false_None": "None",
    "what": 2017,
    "delete3": {},
    "list1": {'hahah': 'hey', 'delete1': None},
    "list2": [],
    "list3": [1, 2, 3, 4, {'tobe': 'tobe', 'delete2': None, '099': [{'321': '222', 'delete99': ''}]}]
}

qcloud = {
    "codeDesc": "Success",
    "totalCount": 14,
    "message": "",
    "code": 0,
    "instanceSet": [
        {
            "lanIp": "10.104.37.58",
            "instanceId": "qcvmfd57f3113bc6fd6f0c8ce381f5433539",
            "unImgId": "img-0vbqvzfn",
            "imageId": 6,
            "autoRenew": 0,
            "bandwidth": 1,
            "vpcId": 0,
            "deviceClass": "VSELF",
            "diskInfo": {
                "rootType": 2,
                "rootId": "disk-4rnslbwq",
                "rootSize": 50
            },
            "subnetId": 0,
            "isVpcGateway": 0,
            "uuid": "9bd7331d-fb7d-4013-bcb1-65a0d4b46873",
            "wanIpSet": [
                "123.207.32.83"
            ],
            "projectId": 0,
            "deadlineTime": "2017-01-02 00:22:48",
            "cvmPayMode": 1,
            "zoneId": 100002,
            "instanceName": "3日测试镜像",
            "imageType": "公有镜像",
            "status": 4,
            "mem": 1,
            "Region": "gz",
            "networkPayMode": 2,
            "unInstanceId": "ins-gsbuwc26",
            "createTime": "2016-12-02 00:22:40",
            "zoneName": "广州二区",
            "statusTime": "2016-12-02 12:28:09",
            "os": "Xserver V8.1_64",
            "cpu": 1
        },
        {
            "lanIp": "10.104.249.153",
            "instanceId": "qcvm0c7dca6b0244fde9b36d7cbc986274a5",
            "unImgId": "img-31tjrtph",
            "imageId": 53,
            "autoRenew": 0,
            "bandwidth": 1,
            "vpcId": 0,
            "deviceClass": "VSELF_2",
            "diskInfo": {
                "rootId": "disk-hq2agvi8",
                "storageSize": 100,
                "rootType": 2,
                "storageType": 2,
                "storageId": "disk-fegdogdg",
                "rootSize": 50
            },
            "subnetId": 0,
            "isVpcGateway": 0,
            "uuid": "a952c786-a1ee-4d0a-8c45-2640ea70e704",
            "wanIpSet": [
                "123.207.115.47"
            ],
            "projectId": 0,
            "deadlineTime": "2017-01-24 09:22:25",
            "cvmPayMode": 1,
            "zoneId": 100003,
            "instanceName": "jupyter",
            "imageType": "公有镜像",
            "status": 2,
            "mem": 16,
            "Region": "gz",
            "networkPayMode": 1,
            "unInstanceId": "ins-r8hr2upy",
            "createTime": "2016-11-24 09:22:18",
            "zoneName": "广州三区",
            "statusTime": "2016-11-30 10:48:24",
            "os": "centos7.2x86_64",
            "cpu": 8
        }
    ]
}


def parse(json_dict):
    # normally it would raise: dictionary changed size during iteration
    # .keys() ONLY for Python 2
    for key in json_dict.keys():
        # okay, no choice, comparing to another `if` inside of `if`, fine...
        if json_dict[key] == {}:
            json_dict.pop(key)
        elif isinstance(json_dict[key], dict):
            parse(json_dict[key])
        elif isinstance(json_dict[key], list):
            for item in json_dict[key]:
                if isinstance(item, dict):
                    parse(item)
        elif not json_dict[key]:
            json_dict.pop(key)

    return json_dict


if __name__ == '__main__':
    with open('result.json', 'w') as f:
        f.write(str(parse(sample)))
