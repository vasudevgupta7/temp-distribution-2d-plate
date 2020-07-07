"""Convert npy files into tf dataset

@author: vasudevgupta
"""
import tensorflow as tf
import numpy as np
from sklearn.utils import shuffle

from dataloader.dataset_utils import load_array

def make_dataset(config, configuration_ls= [7,8,9,10]):
    
    arr= np.zeros(shape= (1,51,51,3))
    for i in configuration_ls:
        configuration= load_array(f'/Users/vasudevgupta/Desktop/GitHub/Prof_Prabhu_project/dataset/arr_format/config{i}')
        arr= np.concatenate([arr, configuration], axis= 0)
    arr= arr[1:]
    
    conditions= arr[:,:,:,:-1]
    real_data= arr[:,:,:,-1:]
    conditions, real_data= shuffle(conditions, real_data)
    
    conditions= np.pad(conditions, ((0,0),(7,6),(7,6),(0,0)), constant_values= -1)
    real_data= np.pad(real_data, ((0,0),(7,6),(7,6),(0,0)), constant_values= -1)
    
    conditions= tf.convert_to_tensor(conditions, dtype= tf.float32)
    real_data= tf.convert_to_tensor(real_data, dtype= tf.float32)
    
    val_size= config['cgan'].get('validation_size', 200)
    
    train_dataset= tf.data.Dataset.from_tensor_slices((conditions[:-val_size], real_data[:-val_size])).shuffle(config['cgan'].get('buffer_size', 400)).batch(config['cgan'].get('batch_size', 32))
    val_conditions= conditions[-val_size:]
    val_real_data= real_data[-val_size:]
    
    return train_dataset, (val_conditions, val_real_data)
