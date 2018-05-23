import pandas as pd
import numpy as np
from Clawer_Base.db_io import get_filepath
from Clawer_Base.db_io import Excel_merger

def clean(raw_num):
    if isinstance(raw_num, str):
        try:
            cleaned_num = raw_num.strip()
            cleaned_num = cleaned_num.strip('.')
            cleaned_num = cleaned_num.strip('0.')
            cleaned_num = cleaned_num.replace('—', '-').replace('．', '.').replace(' ', '', 3).replace('，', ',', 3).replace('O', '0', 5).replace(',', '', 5)
            return float(cleaned_num)
        except:
            print(raw_num)
    elif raw_num == np.nan:
        print(raw_num)
    else:
        return raw_num

def remove_list(num1, num2):
    del_keys =[]
    confirm_keys = [np.nan,
                    u'城市',
                    'Population',
                    'Total Land Area and Population Density of Administrative Region'
                    ]
    del_keys.extend(confirm_keys)
    for i in range(10):
        iteration_key = ['%s-%s续表%s' % (num1, num2, i),
                         '%s--%s续表%s' % (num1, num2, i),
                         '%s—%s续表%s' % (num1, num2, i),
                         '%s-%s 续表%s' % (num1, num2, i),
                         '%s-%s 续表%s continued %s' % (num1, num2, i, i),
                         '%s-%s 续表%s continued' % (num1, num2, i),
                         '%s-%s 续表 %s continued' % (num1, num2, i)
                         ]
        del_keys.extend(iteration_key)
    return del_keys

def people_clean(year):
    dfs = pd.read_excel(r'D:\program_lib\yearbook\yearbook\result\2-12 土地资源\xlsx\%s.xlsx'%year, None)
    land_col_name =[
        '城市',
        'city',
        '城市建设用地面积(sq.km)',
        '居住用地面积面积(sq.km)',
        '城市建设用地占市区面积比重(%)'
        # '全市建成区面积区面积(sq.km)',
        # '建成区绿化覆盖面积（公顷）',
        # '建成区道路绿化覆盖（公顷）',
        # '市辖区城市建设用地面积(sq.km)',
        # '全市基建占用耕地面积（亩）',
        # '市区基建占用耕地面积（亩）',
        # '1992全市人口密度(person/sq.km)',
        # '1993全市人口密度(person/sq.km)',
        # '1992市辖区人口密度(person/sq.km)',
        # '1993市辖区人口密度(person/sq.km)'
        # '全市耕地总资源(千公顷)',
        # '市辖区耕地面积(千公顷)',
        # '园林绿地面积(公顷)',
        # '全市人均占自耕地面积额(亩）'
        # '基建占用耕地面积(亩)'
        # '建成区绿化覆盖率(%)'
        # '市辖区居住用地面积(sq.km)'
    ]
    peo_col_name = [
        '城市',
        'City',
        '全市总人口（万人）',
        '市辖区总人口（万人）',
        # '全市非农业人口（万人）',
        # '市辖区非农业人口（万人）',
        # '全市总户数（万户）',
        # '市辖区总户数（万户）'
        '全市年平均人口（万人）',
        '市辖区年平均人口（万人）',
        # '全市非农业人口比重(％)',
        # '市辖区非农业人口比重(％)',
        # '全市总户数（万户）',
        # '市辖区总户数（万户）'
        # '全市出生率（‰）',
        # '市辖区出生率（‰）',
        '全市自然增长率（‰）',
        '市辖区自然增长率（‰）'
    ]
    df_list = []
    del dfs['CNKI']
    for df in dfs.items():
        df = df[1]
        print(df)
        del_key = remove_list(2, 11)
        df.columns = land_col_name
        df = df[True-df[u'城市'].isin(del_key)]
        df[u'城市'] = df[u'城市'].map(str.strip)
        df = df[True-df[u'城市'].isin(del_key)]
        for i in land_col_name[1:]:
            df[i] = df[i].map(clean)
        df = df.set_index(u'城市')
        df['年份'] = year
        print(df)
        df_list.append(df)
    if len(df_list) > 1:
        df = pd.concat(df_list)
    df.to_excel(r'D:\program_lib\yearbook\yearbook\result\2-12 土地资源\cleaned\%s.xlsx'%year)

class Yearbook_merge(Excel_merger):
    def process(self):
        df = self.merge()
        self.saver(df)


if __name__ == "__main__":
    # print(remove_list(2, 11))
    people_clean(2016)
    # yearbook_merge = Yearbook_merge(r'D:\Downloads\2-1人口\cleaned')
    # trans_df = pd.read_excel(r'D:\Downloads\2-1人口\translate\transfile.xlsx', index_col='shortname')
    # res_df = pd.read_excel(r'D:\Downloads\2-1人口\cleaned\merged.xlsx')
    # def name_transform(raw_str):
    #     trans_df_index = trans_df.index
    #     if raw_str in trans_df_index:
    #         return trans_df.ix[raw_str, 'fullname']
    #     else:
    #         return raw_str
    # res_df[u'城市'] = res_df[u'城市'].map(name_transform)
    # res_df.to_excel(r'D:\Downloads\2-1人口\cleaned\name_transed.xlsx')

