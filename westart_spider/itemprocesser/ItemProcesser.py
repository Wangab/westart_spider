from westart_spider.items import WestartSpiderItem


def parse_item(dict_obj):
    item = WestartSpiderItem()
    item["avatarUrl"] = "https:" + dict_obj.get("avatarUrl")
    item["cardUrl"] = "https:" + dict_obj.get("cardUrl")
    # item["avatarUrl_jk"] = "https:" + dict_obj.get("")
    # item["cardUrl_jk"] = "https:" + dict_obj.get("")
    item["city"] = dict_obj.get("city")
    item["height"] = dict_obj.get("height")
    item["identityUrl"] = dict_obj.get("identityUrl")
    item["modelUrl"] = dict_obj.get("modelUrl")
    item["realName"] = dict_obj.get("realName")
    item["totalFanNum"] = dict_obj.get("totalFanNum")
    item["totalFavorNum"] = dict_obj.get("totalFavorNum")
    item["userId"] = dict_obj.get("userId")
    item["viewFlag"] = dict_obj.get("viewFlag")
    item["weight"] = dict_obj.get("weight")
    item["_id"] = dict_obj.get("userId")
    return item
