#!/usr/bin/python
# coding:utf-8

# Intern-Life - kcik_dic_file.py
# 2017/11/24 16:35
# 

__author__ = 'Benny <benny@bennythink.com>'

sample = {
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
        "test4": "hello",
        "test5": 1
    },
    "false_None": "None",
    "what": 2017,
    "delete3": {},
    "list1": {'hahah': 'hey', 'delete1': None},
    "list2": [],
    "list3": [1, 2, 3, 4, {'tobe': 'tobe', 'delete2': None}]
}


# value is list -> dict , wrong.



def parse(json_dict):
    # normally it would raise:
    # dictionary changed size during iteration
    # .keys() ONLY for Python 2
    for key in json_dict.keys():
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

    # print '?? ', json_dict
    return json_dict


if __name__ == '__main__':
    print parse(sample)
