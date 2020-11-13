"""
 store format is:
 "category" : { "subcategory1" : {sub categories of subcategory1},
                "subcategory2" : {sub categories of subcategory2},
                "subcategory3" : None,
                ...
               }
 if one category does not have subdivision,then it's value is None,
 for example 耕地面积 Cultivated Area doesn't have subcategories, this was stored as "耕地面积 Cultivated Area": None.
"""

CATEGORIES = {}

CATEGORIES['economyCategory_经济类'] = {

    "总产值 Gross Output Value": {
        '总 Total': None,
        '第一产业 Raw Materials': None,
        '第二产业 Secondary Industry': None,
        '第三产业 Service': {'商饮 Grocery': None, '服务业 Hospitality and Service': None},
        '种植业 Agriculture': {'粮食 Grain': None,'水果 Fruit': None, '蔬菜 Vegetables': None},
        '林业 Forestry': None,
        '牧业 Animal Husbandry': None,
        '副业 Miscellaneous': {'运输业 Shipping': None, '仓储业 Warehouse': None, '建筑业 Construction': None},
        '渔业 Fishery': None},

    "集体经济收入 Collective Economic Income": {
        '总 Total': None,
        '第一产业 Raw Materials': None,
        '第二产业 Secondary Industry': None,
        '第三产业 Service': {'商饮 Grocery': None, '服务业 Hospitality and Service': None},
        '种植业 Agriculture': {'粮食 Grain': None, '水果 Fruit': None, '蔬菜 Vegetables': None},
        '林业 Forestry': None,
        '牧业 Animal Husbandry': None,
        '副业 Miscellaneous': {'运输业 Shipping': None, '仓储业 Warehouse': None, '建筑业 Construction': None},
        '渔业 Fishery': None},

    "耕地面积 Cultivated Area": None,
    "粮食总产量 Total Grain Output": None,
    "人均收入 Per Capita Income": None,
    "人均居住面积 Per Capita Living Space": None,

    "电价 Electricity Price": {
        'General': None,
        '生活 Household': None,
        '农业 Agricultural': None,
        '工业 Industrial': None,
        '商业 Commercial': None},
    "用电量 Electricity Consumption": {
        'General': None,
        '生活 Household': {'全村 village': None, '每户 per household': None, '每人 per person': None},
        '农业 Agricultural': None,
        '工业 Industrial': None,
        '商业 Commercial': None},

    "水价 Water Price": {
        'General': None,
        '生活 Household': None,
        '农业 Agricultural': None,
        '工业 Industrial': None,
        '商业 Commercial': None},
    "用水量 Water Consumption": {
        'General': None,
        '生活 Household': None,
        '农业 Agricultural': None,
        '工业 Industrial': None,
        '商业 Commercial': None}
}


CATEGORIES["educationCategory_教育类"] = {
    "受教育程度 Highest Level of Education": {
        "中专高中 High School": {'人数 number of people': None, '百分比 (%) percentage': None},
        '初中 Junior High School': {'人数 number of people': None, '百分比 (%) percentage': None},
        '大专以上 College/University or Higher': {'人数 number of people': None, '百分比 (%) percentage': None},
        '小学 Elementary School': {'人数 number of people': None, '百分比 (%) percentage': None},
        '文盲 Illiterate': {'人数 number of people': None, '百分比 (%) percentage': None}
    },
    '小学在校生 Elementary School Students': None,
    '小学老师 Elementary School Teachers': None,
    '新入学生 - 大学 Initial Student Enrollment - College/University': None
}

# 人数 Number of People, 户数 Number of Households, 百分比 Percentage are recorded as unit in ethnicGroupUnit_民族单位 table
CATEGORIES["ethnicGroupsCategory_民族类"] = {
    "汉族 Han": None,
    "壮族 Zhuang": None,
    "回族 Hui": None,
    "满族 Manchu": None,
    "维吾尔族 Uyghur": None,
    "苗族 Miao": None,
    "彝族 Yi": None,
    "土家族 Tujia": None,
    "藏族 Tibetan": None,
    "蒙古族 Mongolian": None,
    "侗族 Dong": None,
    "布依族 Bouyei": None,
    "瑶族 Yao": None,
    "白族 Bai": None,
    "朝鲜族 Korean/Choson": None,
    "哈尼族 Ho /Hani": None,
    "黎族 Li": None,
    "哈萨克族 Kazakh": None,
    "傣族 Dai": None,
    "畲族 She": None,
    "傈僳族 Lisu": None,
    "东乡族 Dongxiang": None,
    "仡佬族 Gelao": None,
    "拉祜族 Lahu": None,
    "佤族 Wa": None,
    "水族 Sui": None,
    "纳西族 Nakhi/Naxi": None,
    "羌族 Qiang": None,
    "土族 Tu": None,
    "仫佬族 Mulao": None,
    "锡伯族 Xibe": None,
    "柯尔克孜族 Kyrgyz": None,
    "景颇族 Jingpo": None,
    "达斡尔族 Daur": None,
    "撒拉族 Salar": None,
    "布朗族 Blang": None,
    "毛南族 Maonan": None,
    "塔吉克族 Tajik": None,
    "普米族 Pumi": None,
    "阿昌族 Achang": None,
    "怒族 Nu": None,
    "鄂温克族 Evenki/Ewenki": None,
    "京族 Gin": None,
    "基诺族 Jino": None,
    "德昂族 De'ang/Deang": None,
    "保安族 Bonan": None,
    "俄罗斯族 Russian": None,
    "裕固族 Yugur": None,
    "乌兹别克族 Uzbek": None,
    "门巴族 Monba": None,
    "鄂伦春族 Oroqen": None,
    "独龙族 Dereng": None,
    "赫哲族 Hezhen": None,
    "高山族 Gaoshan": None,
    "珞巴族 Lhoba": None,
    "塔塔尔族 Tatar": None,
    "少数民族 (总) Ethnic Minorities (total)": None
}

# categories that exist in Natural Disasters.csv(2020 version)
CATEGORIES["naturalDisastersCategory_自然灾害类"] = {
    "冰凌 Icestorm": None,
    "冰雹 Hailstorm": None,
    "台风 Typhoon": None,
    "地震 Earthquake": None,
    "寒潮 Cold Wave": None,
    "山火 Wildfire": None,
    "旱灾 Drought": None,
    "暴风雨 Severe Storm": None,
    "暴风雪 Blizzard": None,
    "水灾 Flood": None,
    "沙尘暴 Sandstorm": None,
    "海啸 Tsunami": None,
    "涝灾 Waterlogging": None,
    "滑坡和泥石流 Landslide and Debris Flow": None,
    "虫害 Pestilence": None,
    "雷雨 Thunderstorm": None,
    "霜冻 Frost Damage": None,
    "风灾 Windstorm": None,
    "龙卷风 Tornado": None,
    "雪崩 Avalanche": None
}