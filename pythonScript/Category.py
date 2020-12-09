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
        "中专高中 High School": None,
        '初中 Junior High School': None,
        '大专以上 College/University or Higher': None,
        '小学 Elementary School': None,
        '文盲 Illiterate': None
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

# categories that exist in population.csv(2020 version)
CATEGORIES["populationcategory_人口类"] = {
    "人口 Population": {
        "总人口 Total Population": None,
        "男性人口 Male Population": None,
        "女性人口 Female Population": None
    },
    "农转非 Agricultural to Non-Agricultural Hukou / Change of Residency Status": {
        "户数 number of households": None,
        "人数 number of people": None
    },
    "出生人数 Number of Births": None,
    "户数 Number of Households": None,
    "死亡人数 Number of Deaths": None,
    "死亡率 Death Rate (%)": None,
    "死亡率 Death Rate (‰)": None,
    "残疾人数 Disabled Population": {
        "精神残疾 Mental Disabilities": None,
        "听力语言残疾 Hearing and Speech Disabilities": None,
        "残疾人总数 Total Disabled Population": None,
        "肢体残疾 Amputation and/or Paralysis": None,
        "智力残疾 Intellectual Disabilities": None,
        "视力残疾 Blindness": None,
    },
    "流动人口/暂住人口 Migratory/Temporary Population": None,
    "自然出生率 Birth Rate (%)": None,
    "自然出生率 Birth Rate (‰)": None,
    "自然增长率 Natural Population Growth Rate (%)": None,
    "自然增长率 Natural Population Growth Rate (‰)": None,
    "迁入 Migration In": {
        "知识青年 Educated Youth": None,
        "户数 number of households": None,
        "人数 number of people": None
    },
    "迁出 Migration Out": {
        "知识青年 Educated Youth": None,
        "户数 number of households": None,
        "人数 number of people": None
    }

}

# categories that exist in military.csv(2020 version)
CATEGORIES["militarycategory_军事类"] = {
    "村民纠纷 Number of Civil Mediations": None,
    "共产党员 CCP Membership": {
        "女 Female": None,
        "总 Total": None,
        "男 Male": None,
        "少数民族 Ethnic Minorities": None
    },
    "阶级成分 Class Status": {
        "中农 Middle Peasant": None,
        "地主 Landlord": None,
        "富农 Rich Peasant": None,
        "贫下中农 Poor and Lower Middle Peasant": None

    },
    "入伍 Military Enlistment": None,
    "新党员 New CCP Membership": {
        "女 Female": None,
        "总 Total": None,
        "男 Male": None,
        "少数民族 Ethnic Minorities": None
    },
    "刑事案件 Number of Reported Crimes": None
}

# categories that exist in military.csv(2020 version)
CATEGORIES["militarycategory_军事类"] = {
    "村民纠纷 Number of Civil Mediations": None,
    "共产党员 CCP Membership": {
        "女 Female": None,
        "总 Total": None,
        "男 Male": None,
        "少数民族 Ethnic Minorities": None
    },
    "阶级成分 Class Status": {
        "中农 Middle Peasant": None,
        "地主 Landlord": None,
        "富农 Rich Peasant": None,
        "贫下中农 Poor and Lower Middle Peasant": None

    },
    "入伍 Military Enlistment": None,
    "新党员 New CCP Membership": {
        "女 Female": None,
        "总 Total": None,
        "男 Male": None,
        "少数民族 Ethnic Minorities": None
    },
    "刑事案件 Number of Reported Crimes": None
}

# categories that exist in familyplanning.csv(2020 version)
CATEGORIES["famliyplanningcategory_计划生育类"] = {
    "计划生育率 (%) Planned Birth Rate (%)": None,
    "节育率 (%) Rate of Contraception": None,
    "结扎总数 Total Number of Vasectomies and Tubal Ligations": None,
    "领取独生子女证 (人数) Certified Commitment to One Child Policy (number of people)": None,
    "男性结扎 Vasectomies": None,
    "女性结扎 Tubal Ligations": None,
    "人工流产 Abortions": None,
    "上环 Use of Intrauterine Device (IUD)": None,
    "引产 Late-term Abortions": None,
    "育龄妇女人口 Number of Women of Childbearing Age": None,
    "绝育手术 Sterilization Surgeries": None
}

# categories that exist in military.csv(2020 version)
CATEGORIES["militarycategory_军事类"] = {
    "村民纠纷 Number of Civil Mediations": None,
    "共产党员 CCP Membership": {
        "女 Female": None,
        "总 Total": None,
        "男 Male": None,
        "少数民族 Ethnic Minorities": None
    },
    "阶级成分 Class Status": {
        "中农 Middle Peasant": None,
        "地主 Landlord": None,
        "富农 Rich Peasant": None,
        "贫下中农 Poor and Lower Middle Peasant": None

    },
    "入伍 Military Enlistment": None,
    "新党员 New CCP Membership": {
        "女 Female": None,
        "总 Total": None,
        "男 Male": None,
        "少数民族 Ethnic Minorities": None
    },
    "刑事案件 Number of Reported Crimes": None
}

# categories that exist in Natural Environment.csv(2020 version)
CATEGORIES["naturalenvironmentcategory_自然环境类"] = {
    "海拔 (米) Altitude": None,
    "平均降水量 Average Yearly Precipitation Amount": None,
    "平均温度 Average Yearly Temperature": None
}

# geography categories that exist in Village Information.csv(2020 version)
CATEGORIES["villagegeographycategory_村庄地理类"] = {
    "村庄总面积 Total Area": None,
    "纬度 Latitude": None,
    "经度 Longitude": None,
    "距隶属县城距离 Distance to Affiliated to the county town": None,
}