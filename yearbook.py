import pandas as pd
import numpy as np

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

def people_clean(year):
    dfs = pd.read_excel(r'D:\Downloads\2-1人口\xlsx\%s.xlsx'%year, None)
    col_name = [
        '城市',
        '全市总人口（万人）',
        '市辖区总人口（万人）',
        '全市非农业人口（万人）',
        '市辖区非农业人口（万人）',
        # '全市总户数（万户）',
        # '市辖区总户数（万户）'
        # '全市年平均人口（万人）',
        # '市辖区年平均人口（万人）',
        # '全市非农业人口比重(％)',
        # '市辖区非农业人口比重(％)',
        # '全市总户数（万户）',
        # '市辖区总户数（万户）'
        '全市出生率（‰）',
        '市辖区出生率（‰）',
        '全市自然增长率（‰）',
        '市辖区自然增长率（‰）'
    ]
    df_list = []
    del dfs['CNKI']
    for df in dfs.items():
        df = df[1]
        print(df)
        del_key1 = ['2-1续表%s' % i for i in range(10)]
        del_key2 = ['2—1续表%s' % i for i in range(10)]
        del_key3 = ['2--1续表%s' % i for i in range(10)]
        del_key4 = ['2-1 续表%s' % i for i in range(10)]
        del_key5 = ['2-1 续表%s continued %s' %(i, i) for i in range(10)]
        del_key6 = [np.nan, u'城市', 'Population']
        del_key = del_key1 + del_key2 + del_key3 + del_key4 + del_key5 + del_key6
        df.columns = col_name
        df = df[True-df[u'城市'].isin(del_key)]
        df[u'城市'] = df[u'城市'].map(str.strip)
        df = df[True-df[u'城市'].isin(del_key)]
        for i in col_name[1:]:
            df[i] = df[i].map(clean)
        df = df.set_index(u'城市')
        df['年份'] = year
        print(df)
        df_list.append(df)
    if len(df_list) > 1:
        df = pd.concat(df_list)
    df.to_excel(r'D:\Downloads\2-1人口\cleaned\%s.xlsx'%year)

if __name__ == "__main__":
    people_clean('1995-1')