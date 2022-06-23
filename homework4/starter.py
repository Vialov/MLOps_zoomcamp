#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd


categorical = ['PUlocationID', 'DOlocationID']

def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)
    return dv, lr


def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.dropOff_datetime - df.pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def run(year, month):

    df = read_data(f'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{year:04d}-{month:02d}.parquet')

    dv, lr = load_model()
    
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('Mean predicted ride', y_pred.mean())


    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


    df_result = pd.DataFrame()

    df_result['ride_id'] = df['ride_id']
    df_result['pred_time'] = y_pred

    output_file = f'fhv_pred_{year:04}-{month:02}.parquet'

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

if __name__=='__main__':
    year = 2021
    month = 2
    run(year, month)