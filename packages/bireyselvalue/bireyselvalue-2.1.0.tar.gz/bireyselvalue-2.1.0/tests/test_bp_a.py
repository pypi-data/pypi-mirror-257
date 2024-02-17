from bireyselvalue.bireyselvalue import BireyselValue

import pandas as pd
import numpy as np
import os 

def prepare_ds(path):
    ''''this function is just a carton, you should be preparing the dataset and cls on your own'''
    ds_pd = pd.read_csv(path)
    ds_np = ds_pd.to_numpy()
    # *****************************************************
    # create test and train set
    ds_c1 = ds_np[6:69,:]
    ds_c2 = ds_np[76:139,:]
    ds_c3 = ds_np[146:,:]
    # **********************************
    arr = np.vstack((ds_c1, ds_c2))
    # ************************************
    train_ds = np.vstack((arr, ds_c3))
    # **********************************

    t_ds_c1 = ds_np[:6,:]
    t_ds_c2 = ds_np[69:76,:]
    t_ds_c3 = ds_np[140:146,:]

    arr_t = np.vstack((t_ds_c1, t_ds_c2))
    # ************************************
    test_ds = np.vstack((arr_t, t_ds_c3))
    # ************************************
    ds = train_ds[:,:7]
    cls = train_ds[:,-1]
    ds_test = test_ds[:,:7]
    cls_test = test_ds[:,-1]

    return [ds, cls, ds_test, cls_test]

def train_bp_a(ds, cls, radius, report_num):
    '''this is the first main function on using this package, it expects the ds, cls, and radius, and how many report
        you wish to see from the neighbors parameter. it basically return the model for saving purpos
    '''
    inst = BireyselValue()
    inst.input_feature(ds=ds, cls=cls)
    inst.report_input()
    inst.build(radius=radius)
    inst.build_report(num=report_num)
    inst.train()
    inst.model_summary()

    return inst

def save_model(inst,path_save):
    '''this function basically save the bp_a.v.1.0 model, requrist two args:
        1. the model to save that should be bp_a model instance
        2. the path of saving the model
    '''
    inst.save_model(file_name=path_save)

def load_model(path_load):
    '''this function basically load the bp_a.v.1.0 model and return it, requires the path of the model to load'''
    model_path = path_load
    model = BireyselValue()
    model.load_model(model_path=model_path)
    model.loaded_model_summary()
    return model

def test_bp_a(model, ds_test, cls_test):
    '''this function execute the test on bp_a. requires:
        1. ds test
        2. cls test
        both must be following the loaded model summary
    '''
    model.predict_test(input_test_feature=ds_test, cls_test_feature=cls_test)


# EXECUTE THE SCRIPT TEST

# (1) get the ds,cls for train and test. I will use the ds in Bireysel official published paper reference [1] 

path = os.getcwd() + "\essential_ds_final.csv"
path_to_save = os.getcwd() + "/train_ds_model"
path_to_load = os.getcwd() + "/train_ds_model.hdf5"


ready_set = prepare_ds(path=path)
# train set
ds = ready_set[0]
cls = ready_set[1]
# test set
ds_test = ready_set[2]
cls_test = ready_set[3]

# train model
inst = train_bp_a(ds=ds, cls=cls, radius=0.2, report_num=5)

# save the model
save_model(path_save=path_to_save, inst=inst)

# load model
model = load_model(path_load=path_to_load)

# test model
test_bp_a(ds_test=ds_test, cls_test=cls_test, model=model)



