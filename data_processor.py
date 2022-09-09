from distutils.debug import DEBUG
import pandas as pd
import numpy as np
import re, os, logging
import radipy
import yaml


logging.basicConfig(level=logging.INFO)

def header_parser(columns):
    for i in range(1, len(columns)):
        columns[i] = re.sub(" \(.+", "", columns[i])
    return columns

def cal_helper_func(model, args, organ, df):
    args['volume'] = df[organ]
    args['dose'] = df.index.astype(float)
    return model(**args).val

def preprocess_data():
    df = pd.read_csv('data.csv')
    df.rename(columns=header_parser(df.iloc[0]), inplace=True)
    df.drop(df.index[0], inplace=True)
    df.replace(np.NaN, 0.0, inplace=True)
    df.set_index('Absolute Dose(Gy)', inplace=True)
    df = df.astype(float)

    df = df - df.shift(-1)
    df.replace(np.NaN, 0.0, inplace=True)
    logging.debug(df)

    df = df.loc[:,~df.columns.duplicated()].copy()
    return df

def get_all_keys(d):
    for key, value in d.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_keys(value)


if __name__ == '__main__':
    df = preprocess_data()
    logging.debug(df)
    with open('./config/constants.yml', 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
            for organ in cfg:
                for model in cfg[organ]:
                    idx = 1
                    for arg_set in cfg[organ][model]:
                        print(organ, model, idx, cal_helper_func(getattr(radipy.models, model), arg_set, organ, df))
                        idx += 1
                logging.info('==========================')
        except yaml.YAMLError as exc:
            logging.error(exc)

    # radipy.models.RS
    # print(result)
    # heart_LKB = radipy.models.LKB(D50=48, m=0.1, gEUD_model=radipy.models.gEUD(df['Heart'], df.index.astype(float), 1/0.35))
    # print(heart_LKB.val)
