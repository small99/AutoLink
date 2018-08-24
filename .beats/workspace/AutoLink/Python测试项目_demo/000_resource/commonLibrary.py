# -*- coding:utf-8 -*-

import random
import os
from datetime import *


class commonLibrary():

    def create_Phone(self):
        u'''调用create_Phone方法：创建随机手机号
                       '''
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153",
                   "155", "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(prelist) + "".join(random.choice('0123456789') for i in range(8))

    def create_Random_Number(self, length):
        u'''调用create_Random_Number方法：创建随机指定长度数字
                               '''
        length = int(length)
        return "".join(random.choice('0123456789') for i in range(length))

    def __getdistrictcode(self):
        filename = 'districtCode.txt'
        filepath =os.path.abspath(os.path.dirname(__file__)+os.path.sep+filename)
        print (filepath)
        if os.path.exists(filepath):
            with open(filepath) as file:
                data = file.read()
                districtlist = data.split('\n')
        else:
            with open(filepath) as file:
                data = file.read()
                districtlist = data.split('\n')

        for node in districtlist:
            if node[10:11] != ' ':
                state = node[10:].strip()
            if node[10:11] == ' ' and node[12:13] != ' ':
                city = node[12:].strip()
            if node[10:11] == ' ' and node[12:13] == ' ':
                district = node[14:].strip()
                code = node[0:6]
                self.codelist.append({'state': state, 'city': city, 'district': district, 'code': code})

    def gennerator(self):
        u'''调用gennerator方法：生成随机身份证号
                                       '''
        self.codelist = []
        if not self.codelist:
            self.__getdistrictcode()
        id = self.codelist[random.randint(0, len(self.codelist) - 1)]['code']  # 地区项
        id = id + str(random.randint(1930, 1999))  # 年份项
        da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
        id = id + da.strftime('%m%d')
        id = id + str(random.randint(100, 300))  # 顺序号简单处理

        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '4', '9': '3',
                     '10': '2'}  # 检验码映射
        for i in range(0, len(id)):
            count = count + int(id[i]) * weight[i]
        id = id + checkcode[str(count % 11)]  # 算出校验码
        return id

    def create_BankCard(self, bank_No):
        u'''调用create_BankCard方法：创建随机银行卡号，bank_No长度不超过19位。
                                       '''
        return str(bank_No) + "".join(random.choice('0123456789') for i in range(19 - len(str(bank_No))))

    def create_UserName(self):
        namelist = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
                    '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
                    '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
                    '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
                    '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
                    '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
                    '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
        # namelist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        return str(random.choice(namelist) + '' + random.choice(namelist) + '' + random.choice(namelist)).encode(
            'utf-8')
        # return 'saf'

if __name__ == '__main__':
    idcard="110101198001010010"
    test=commonLibrary()
    print(test.gennerator())




