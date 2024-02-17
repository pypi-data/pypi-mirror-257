
# Copyright (c) 2024 Dr. Deniz Dahman's <denizdahman@gmail.com>
 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# denizdahman@gmail.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# Support the author of this package on:.#
# https://patreon.com/user?u=118924481
# https://www.youtube.com/@dahmansphi 


import matplotlib.pyplot as plt
from collections import Counter
from numpy import asarray
from os import listdir
from sys import flags
from PIL import Image
import pandas as pd
import numpy as np
import math
import h5py
import os

np.random.seed(41)
class BireyselValue:
  def __init__(self) -> None:

    self.__cls_names_img_input = None
    self.__numcls_input_feature_image = None
    self.__numcls_img = None
    self.__input_feature_img = None
    self.__radius_img = None
    self.__ds = None
    self.__cls = None
    self.__numcls = None
    self.__radius = None
    self.__main_norm = None
    self.__inner_radius_based_on_dist = None
    self.__zone_val_borders_list = None
    self.__trainDS = None
    self.__list_avg_input_feature_by_cls = None
    self.__list_err_in_train_by_cls = None
    self.__model_acc = None
    self.__img_cls_representatives_list = None
    self.__zone_dist_percents = None
    self.__ds_transformed_separet_by_cls = None
    self.__input_feature = None
    self.__input_feature_img = None
    self.__neighbour_ready = None
    self.__train_done = None
    self.__zone_done = None
    # *********************************************************
    self.__history_X_ds = None
    self.__history_y_cls = None
    self.__loaded_model_zone_summary = None
    self.__loaded_model_acc = None
    self.__loaded_model_main_norm = None
    self.__cls_name_and_code = None
    self.__loaded_model_list_input_avg = None
    self.__loaded_model_list_err_avg = None
    self.__loaded_img_cls_representatives_list = None
    self.__loaded_zone_val_borders_list = None
    self.__predict_X_ds_test = None
    self.__predict_y_cls_test = None
    self.__radius_test = None
    self.__numcls_test = None
    self.__predictDS_test = None
    self.__predict_X_ds_predict = None
    self.__radius_predict = None
    self.__numcls_predict = None
    self.__predictDS_predict = None
    self.__loaded_model_verification = None
    self.__predict_test_verification = None
    self.__predict_predict_verification = None

  # ************ Image section construction ***************************************
  def __input_feature_img(self, path):
    '''This function to prepare the input ds of images into a shape for build and train'''

    __folder_cls_names = []
    for folder_names in listdir(path):
      __dot = '.'
      isValidName = __dot in folder_names

      if isValidName == False:
        __folder_cls_names.append(folder_names)

    self.__numcls_input_feature_image = len(__folder_cls_names)
    self.__cls_names_img_input = __folder_cls_names

    if self.__numcls_input_feature_image >= 2:

      __number_of_img_per_cls_list = []

      for folder_name_index in range(len(__folder_cls_names)):
        folder_name = __folder_cls_names[folder_name_index]

        __last_char_in_path = '/'
        isLastLaterinPath = path[-1] == __last_char_in_path
        if isLastLaterinPath:
          __last_char_in_path = ''
        else:
          __last_char_in_path = __last_char_in_path

        __path = path + __last_char_in_path + folder_name + '/'
        __counter = 0
        for imgName in listdir(__path):

          isNameImage = imgName.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
          if isNameImage:
            __counter +=1
        __number_of_img_per_cls_list.append(__counter)


      __number_of_img_per_cls_min = min(__number_of_img_per_cls_list)

      if __number_of_img_per_cls_min > 1300:

        __progress_bar_num = 0
        print("Progress on images ds prepareation starts, don't exist")
        __starts = "*" *300
        print(__starts)
        print("This Library, and the BireyselValue Algorithm is by Dr. Deniz Dahman's. Visit dahmansphi.com")

        __main_list_of_all_imgs = []
        for folder_name_index in range(len(__folder_cls_names)):
          folder_name = __folder_cls_names[folder_name_index]
          __class_number = folder_name_index
          __class_name = folder_name

          __last_char_in_path = '/'
          isLastLaterinPath = path[-1] == __last_char_in_path
          if isLastLaterinPath:
            __last_char_in_path = ''
          else:
            __last_char_in_path = __last_char_in_path
          __path = path + __last_char_in_path + folder_name + '/'

          for img_number in range(__number_of_img_per_cls_min):
            __curent_img = listdir(__path)[img_number]
            imgName = __path + __curent_img
            image = Image.open(imgName).convert('L')
            __img_hight, __img_width = image.size
            isHight = __img_hight >  30
            isWidth = __img_width > 30

            if isHight and isWidth:
              __resized_img = image.resize((20, 20))
              __img_to_np = asarray(__resized_img)

              __img_flatten = __img_to_np.flatten()
              __img_flatten = np.append(__img_flatten, [__class_number])
              __img_flatten = list(__img_flatten)
              __main_list_of_all_imgs.append(__img_flatten)

              if __progress_bar_num >= 300:
                __end_line = '\n'
                __progress_bar_num = 0
              else:
                __end_line = ''
                __progress_bar_num += 1

              __msg = '*'
              print(__msg, end=__end_line)
              __progress_bar_num += 1

            else:
              print(f"the dim of this img {imgName} is not valid, must be at least 30x30")
      else:
        print("The number of images inside each class folder must be at least 1300 images. That means each class must be having that much number of images")

      __main_list_of_all_imgs = np.array(__main_list_of_all_imgs)

      __ds = __main_list_of_all_imgs[:,:400]
      self.__main_norm = np.linalg.norm(__ds)
      self.__ds = __ds/self.__main_norm
      self.__cls = __main_list_of_all_imgs[:,-1]
      self.__input_feature_img = True
      self.__input_feature = True

      __temp_cls = []
      for i in range(self.__numcls_input_feature_image):
        __temp_cls.append(i)
      self.__numcls_img = np.array(__temp_cls)

      print("")
      print("The input is ready and ok, call on the report_input_img to see the report")
    else:
      print("your path contain only one folder that measn there are less than two class")

  # ******************** standard DS csv type build input construction side *******************************
  def input_feature(self, ds, cls):
    ''' this function to build the training part of the DS
        you verify the essentails and requirements
    '''
    isDsTrue = type(ds).__module__ == np.__name__
    isClsTrue = type(cls).__module__ == np.__name__

    if isDsTrue and isClsTrue:
      lenDsIsTrue = len(ds.shape) == 2
      lenClsIsTrue = len(cls.shape) == 1

      sizeDsClsIsTrue = ds.shape[0] == cls.shape[0]

      if lenDsIsTrue and lenClsIsTrue and sizeDsClsIsTrue:

        dimDsFeatureIstrue = ds.shape[1] >= 2
        dimDsRowIsTrue = ds.shape[0] > 100
        numOfCls = len(Counter(cls)) >= 2

        if dimDsFeatureIstrue and dimDsRowIsTrue and numOfCls:

          __ds_cls_ds = np.column_stack((ds, cls))
          __temp_cls_num = []
          for cls_num in Counter(cls):
            __temp_cls_num.append(cls_num)

          __ds_seprate_by_cls_inx_only = []
          for cls_val in __temp_cls_num:
            __ds_by_inx_cls = np.where(__ds_cls_ds[:,-1] == cls_val)
            __ds_seprate_by_cls_inx_only.append(__ds_by_inx_cls)

          __num_of_instances_by_cls = []
          for instance in range(len(__ds_seprate_by_cls_inx_only)):
            _case_temp = __ds_seprate_by_cls_inx_only[instance]
            for itms in _case_temp:
              __num_of_instances_by_cls.append(len(itms))

          __num_of_cases_based_on_cls = min(__num_of_instances_by_cls)

          __ds_seprate_by_cls_inx_only_based_on_min = []
          for cls_inx_list in __ds_seprate_by_cls_inx_only:

            for case_list in cls_inx_list:
              for num_case in range(__num_of_cases_based_on_cls):
                __ds_seprate_by_cls_inx_only_based_on_min.append(case_list[num_case])

          ds = ds[__ds_seprate_by_cls_inx_only_based_on_min,:]
          cls = cls[__ds_seprate_by_cls_inx_only_based_on_min]

          __num_of_cls = len(__temp_cls_num)
          __len_of_train_ds = len(ds)

          isLenOfTrainDS = __len_of_train_ds >= 70

          if isLenOfTrainDS:

            self.__main_norm = np.linalg.norm(ds)
            self.__ds = ds/self.__main_norm
            self.__cls = cls

            self.__input_feature = True

            __temp_cls_num = []
            for cls_num in Counter(self.__cls):
              __temp_cls_num.append(cls_num)

            self.__numcls = np.array(__temp_cls_num)

          else:
            print(f"Your have got {__num_of_cls}, and the balance of the number of cases is not balanced. that means one of the class is majo. That would effect the training acc. Try to balance the input")
        else:
          print("You must have at least two variables of columns, and 100 instance of rows")
      else:
        print("length of DS must be 2 Dim, and Length of class must be 1 Dim, and both Ds and Cls sets must have the same number of instances")
    else:
      print("Dataset and Cls set must be of Numpy ds type")

  # ************* report on INPUT feature either img or standard **********************************
  def report_input(self, img=False):
    '''This function to report on the input of the dataset and provide graph on the class overlaping'''
    if self.__input_feature:

      _joint_set = np.column_stack((self.__ds, self.__cls))

      if img == True:
        __numcls = self.__numcls_img
      else:
        __numcls = self.__numcls

      _ds_by_cls = []
      for _cls_inx in __numcls:
        _temp_list = np.where(_joint_set[:,-1] == _cls_inx)[0]
        _ds_by_cls.append(_temp_list)

      _cls_counter = 0
      for _itm in _ds_by_cls:

        _ds_itm_by_cls = np.sum(self.__ds[_itm], axis=1)
        _max, _min = np.max(_ds_itm_by_cls), np.min(_ds_itm_by_cls)
        _ds_itm_by_cls = (_ds_itm_by_cls - _min)/( _max - _min)
        _ds_x_lin = np.linspace(0,1, len(_ds_itm_by_cls))

        _cls_label = "Class " + str(_cls_counter)
        plt.scatter(_ds_x_lin, _ds_itm_by_cls, label= _cls_label)
        _cls_counter += 1

      plt.legend()

      if img == False:
        print(f"The sahpe of the ds : {self.__ds.shape}")
        print(f"The shape of the class ds : {self.__cls.shape}")
        print(f"Found the number of classes : {len(__numcls)}")
        print(f"The distribution of class as: {Counter(self.__cls)}")
        print("Next you should call on find parameters to see the right one then build and train, GOOD LUCK")

      else:
        __row_num, __col_num = self.__ds.shape
        star = '*' * 10
        print(star)
        print(" The preparation of your IMAG dataset is done and here is the summary")
        print(f"We found {self.__numcls_input_feature_image} number of class, and the class with their code as follows:")
        print(star)
        for itm_inx in range(len(self.__cls_names_img_input)):
          __cls_name = self.__cls_names_img_input[itm_inx]
          __cls_inx_number = self.__numcls_img[itm_inx]
          print(f"The class name {__cls_name}, and it's code as {__cls_inx_number}")
        print(star)
        print(f"We found the total number of ACCEPTED IMAGES from both classes are {__row_num}")
        print(f"sahpe of ds {self.__ds.shape}, shape of cls {self.__cls.shape}")
        print("Next you should call on find parameters to see the right one then build and train, GOOD LUCK")


  # *********** The build section for the dataset ***********************
  def build(self, radius ,predict=False, test=False, img=False):
    '''This function to build the set for training'''

    if self.__input_feature:
      __neigbours_count_list = []

      if predict == False and test == False:
        out_ds = self.__ds
        inner_ds = self.__ds
        inner_cls_ds = self.__cls

        if img == False:
          radius_val = radius
          self.__radius = radius
          numcls = self.__numcls
        else:
          radius_val = radius
          self.__radius_img = radius
          numcls = self.__numcls_img

      elif predict == True and test == True:
        out_ds = self.__predict_X_ds_test
        inner_ds = self.__history_X_ds
        inner_cls_ds = self.__history_y_cls
        radius_val = self.__radius_test
        numcls = self.__numcls_test
      elif predict == True and test == False:
        out_ds = self.__predict_X_ds_predict
        inner_ds = self.__history_X_ds
        inner_cls_ds = self.__history_y_cls
        radius_val = self.__radius_predict
        numcls = self.__numcls_predict

      __progress_bar_count = 0
      star = "*" * 10
      print("The build on the dataset has just started, please don't stop the process")
      print("This Library- bp_a.v.1.0 - is the first edition of the BireyselValue Algorithm by Dr. Deniz Dahman's. Visit dahmansphi.com")
      print(star)


      __inner_radius_based_on_dist = self.__radius_fun(rad_val=radius_val, inner_ds=inner_ds, out_ds=out_ds)

      for out_inx in range(len(out_ds)):
        X_feature = out_ds[out_inx]
        rad_val = __inner_radius_based_on_dist
        self.__inner_radius_based_on_dist = __inner_radius_based_on_dist

        __cls_count_list = np.zeros(len(numcls))


        for inner_inx in range(len(inner_ds)):

          if out_inx != inner_inx:

            inner_X_feature = inner_ds[inner_inx]
            inner_X_feature_cls = inner_cls_ds[inner_inx]

            __dist = math.dist(X_feature, inner_X_feature)

            if __dist <= rad_val:

              for __cls_count in numcls:
                if __cls_count == inner_X_feature_cls:

                  _find_inx = np.where(numcls == inner_X_feature_cls)

                  __cls_count_list[_find_inx] += 1

        __neigbours_count_list.append(__cls_count_list)

        if __progress_bar_count >= 300:
          __end_line = '\n'
          __progress_bar_count = 0
        else:
          __end_line = ''
          __progress_bar_count += 1

        __msg = '*'
        print(__msg, end=__end_line)
        __progress_bar_count += 1

      if predict == False and test == False:
        self.__trainDS = np.array(__neigbours_count_list)

      elif predict == True and test == True:
        self.__predictDS_test = np.array(__neigbours_count_list)


      elif predict == True and test == False:
        self.__predictDS_predict = np.array(__neigbours_count_list)

      self.__neighbour_ready = True
      print("")
      print("The build of the dataset is done and ready you can now call on the train, predict test")

  def __radius_fun(self, out_ds,inner_ds, rad_val):
    '''This function construct the radius based on the distances'''

    __progress_bar_count_radius = 0

    print("Now we are constructing the Actual norm and radius that can take sometime depends on the power of your machine and dim of the dataset")
    dis_lll = []

    for out_inx in range(len(out_ds)):
      X_feature = out_ds[out_inx]
      for inner_inx in range(len(inner_ds)):

        if out_inx != inner_inx:

          inner_X_feature = inner_ds[inner_inx]
          __dist = math.dist(X_feature, inner_X_feature)
          dis_lll.append(__dist)

      if __progress_bar_count_radius >= 300:
          __end_line = '\n'
          __progress_bar_count_radius = 0
      else:
        __end_line = ''
        __progress_bar_count_radius += 1

      __msg = '*'
      print(__msg, end=__end_line)
      __progress_bar_count_radius += 1

    dis_lll = np.array(dis_lll)

    min_val, max_val = np.min(dis_lll), np.max(dis_lll)
    _rad_val = (min_val + max_val)/2

    if rad_val > 1:
      _rad_val = _rad_val * (rad_val/100)
    else:
      _rad_val = _rad_val * rad_val

    return _rad_val

  def build_report(self, num):
    if self.__neighbour_ready:
      _train_set = self.__trainDS
      _cls_set = self.__cls

      _indices_list = np.random.permutation(np.arange(_train_set.shape[0]))
      _view_cases = _indices_list[:num]

      _casee_sample = _train_set[_view_cases]
      _cases_cls = _cls_set[_view_cases]

      for inx in range(num):
        _case = _casee_sample[inx]
        _cls = _cases_cls[inx]

        print(f"The sample ({_case}), it's orignal class ({_cls})")

  # ****************Zone Construction side *******************************************

  def __zone(self, zone_percent):
    '''This function construct the number of zones for this problem'''
    if self.__neighbour_ready:

      _ds = self.__ds
      _cls = self.__cls
      _numcls = self.__numcls

      __all_avg_points = []
      for entry_inx in range(len(self.__ds)):
        _avg = np.sum(self.__ds[entry_inx])
        __all_avg_points.append(_avg)

      __all_avg_points = np.array(__all_avg_points)
      __all_avg_points = np.sort(__all_avg_points)

      __min_val_avg = np.min(__all_avg_points)
      __max_val_avg = np.max(__all_avg_points)

      _counter_val = __min_val_avg
      _zone_val_borders_list = []
      while _counter_val <= __max_val_avg:
        _counter_val = _counter_val + (_counter_val * zone_percent)
        _zone_val_borders_list.append(_counter_val)

      _zone_val_borders_list = np.array(_zone_val_borders_list)

      _number_of_zones = len(_zone_val_borders_list)
      _zone_lists = [[] for _ in range(_number_of_zones)]

      for point in range(len(_ds)):
        _input = _ds[point]
        _cls_input = _cls[point]

        __sum_x_feature = np.sum(_input)
        __actual_cls_inx = np.where(_numcls == _cls_input)[0][0]

        _temp_zone_list_holder = []
        for _cont in _zone_val_borders_list:
          _temp_val = np.sqrt((__sum_x_feature - _cont)**2)
          _temp_zone_list_holder.append(_temp_val)

        _min_dist_to_zone = min(_temp_zone_list_holder)
        _inx_dist_to_zone = _temp_zone_list_holder.index(_min_dist_to_zone)

        __list_in_zone_lists = _zone_lists[_inx_dist_to_zone]
        __list_in_zone_lists.append(__actual_cls_inx)

      _zone_percents = []

      print(f"The min of input is {__min_val_avg}, the max of the input {__max_val_avg}, with difference of {__max_val_avg - __min_val_avg}")
      print(f"with zone percent {zone_percent}, we constructed ( {_number_of_zones} ) number of zones")
      print(f"report on the zones as follows:")
      print("")
      print("")
      for zone in range(len(_zone_lists)):

        _percent_list = np.zeros(len(_numcls))

        _zone_num = zone + 1
        _sum_of_all_points = sum(Counter(_zone_lists[zone]).values())


        _str = "*" * 5
        print(f"In zone [**{_zone_num}**], we found ({_sum_of_all_points}) inhabitants of ({len(Counter(_zone_lists[zone]))}) number of classes, and distribution of inhabitants as follows:")
        print(_str)

        for dist in Counter(_zone_lists[zone]).items():
          _percent_of_inhabit = (dist[1] / _sum_of_all_points) * 100
          _inx_in_percent_list = dist[0]
          _percent_list[_inx_in_percent_list] = _percent_of_inhabit

          print(f"Class {dist[0]}, has number of {dist[1]} points, {_percent_of_inhabit}% of total")
        _dsh = "_" * 10
        print(_dsh)

        _zone_percents.append(_percent_list)

      _zone_percents = np.array(_zone_percents)

      self.__zone_dist_percents = _zone_percents
      self.__zone_val_borders_list = _zone_val_borders_list
      self.__zone_done = True

  # ****************** Train Construction side *************************************
  def train(self, img=False):
    ''' In this function we construct the training scheme'''
    if self.__neighbour_ready:

      if img == True:
        self.__numcls = self.__numcls_img

      X = self.__trainDS
      y = self.__cls

      __num_of_cls = len(Counter(y))
      __list_of_err_by_cls = [[] for _ in range(__num_of_cls)]
      __list_avg_input_feature_by_cls = [[] for _ in range(__num_of_cls)]

      __list_avg_col_variable_by_cls = [[] for _ in range(__num_of_cls)]

      for point in range(len(self.__ds)):

        x = X[point]
        cls = y[point]

        __sum_x_feature = np.sum(self.__ds[point])
        __actual_cls_inx = np.where(self.__numcls == cls)[0][0]

        __list_in_list_avg_input_feature_by_cls = __list_avg_input_feature_by_cls[__actual_cls_inx]
        __list_in_list_avg_input_feature_by_cls.append(__sum_x_feature)

        __max_neighbor_inx = np.where(x == max(x))[0][0]
        __isMatch = __actual_cls_inx - __max_neighbor_inx


        if __isMatch != 0:

          __list_in_list_of_err_by_cls = __list_of_err_by_cls[__actual_cls_inx]
          __list_in_list_of_err_by_cls.append(__sum_x_feature)

      __list_input_avg = []
      for points in __list_avg_input_feature_by_cls:
        points = np.array(points)

        __sum = np.mean(points)

        __minavg, __maxavg = np.min(points), np.max(points)
        __avg_err = ((__minavg + __maxavg)/2)

        __list_input_avg.append(__avg_err)

      __list_input_avg = np.array(__list_input_avg)

      __list_input_avg_err_by_cls = []
      for list_err in __list_of_err_by_cls:

        __avg = np.mean(list_err)

        __minavg, __maxavg = np.min(list_err), np.max(list_err)
        __avg_avg = ((__minavg + __maxavg)/2)

        __list_input_avg_err_by_cls.append(__avg_avg)

      __list_input_avg_err_by_cls = np.array(__list_input_avg_err_by_cls)

      __list_culture_neigbor_by_cls = [[] for _ in range(__num_of_cls)]

      # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      _right_prediction = 0

      print("we are construction the neighbours list img, please dont' quit until it's done")
      print("")
      __progress_bar_count_radius = 0

      for neighbor in range(len(X)):

        __list_input_avg_in_this_loop = __list_input_avg
        __list_input_avg_err_by_cls_in_this_loop = __list_input_avg_err_by_cls

        _neibors_list = X[neighbor]
        __sum = np.sum(_neibors_list)
        if __sum == 0:
          _neibors_list = _neibors_list
        else:
          _neibors_list = _neibors_list/__sum

        __input_feature = np.sum(self.__ds[neighbor])

        __list_input_avg_in_this_loop = np.sqrt((__list_input_avg - __input_feature)**2)
        __list_input_avg_err_by_cls_in_this_loop = np.sqrt((__list_input_avg_err_by_cls - __input_feature)**2)

        __mat_for_input_feature = np.vstack((__list_input_avg_in_this_loop, __list_input_avg_err_by_cls_in_this_loop))
        __mat_for_input_feature = np.vstack((__mat_for_input_feature, _neibors_list))
        __mat_for_input_feature = __mat_for_input_feature.T

        _actual_cls_inx = np.where(self.__numcls == y[neighbor])[0][0]
        _actual_cls_val = self.__numcls[_actual_cls_inx]

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        col_wise_max = np.max(__mat_for_input_feature,axis=0)
        col_wise_min = np.min(__mat_for_input_feature,axis=0)

        __indx_col_wise_max = []
        __inx_col_wise_min = []

        for __col_val in range(__mat_for_input_feature.shape[1]):

          vmax = col_wise_max[__col_val]
          vmin = col_wise_min[__col_val]

          inxxmax = np.where(__mat_for_input_feature[:,__col_val] == vmax)[0][0]
          inxxmin = np.where(__mat_for_input_feature[:,__col_val] == vmin)[0][0]

          __indx_col_wise_max.append(inxxmax)
          __inx_col_wise_min.append(inxxmin)

        __indx_col_wise_max = np.array(__indx_col_wise_max)
        __inx_col_wise_min = np.array(__inx_col_wise_min)
        __mat_for_input_feature_final_img = np.vstack((__indx_col_wise_max, __inx_col_wise_min))

        __list_to_attach = __list_culture_neigbor_by_cls[_actual_cls_inx]
        __list_to_attach.append(__mat_for_input_feature_final_img)

        if __progress_bar_count_radius >= 50:
          __end_line = '\n'
          __progress_bar_count_radius = 0
        else:
          __end_line = ''
          __progress_bar_count_radius += 1

        __msg = '*'
        print(__msg, end=__end_line)

    __img_cls_representatives_list = [[] for _ in range(__num_of_cls)]

    for _itm in range(len(__list_culture_neigbor_by_cls)):

      for entry in __list_culture_neigbor_by_cls[_itm]:
        __list_in__img_representative = __img_cls_representatives_list[_itm]
        __list_in__img_representative.append(entry.flatten())

    self.__img_cls_representatives_list = __img_cls_representatives_list

    print("")
    print("the neighbours list img is ready, you can now move to save the model and then predict test, good luck")
    print("however before that make sure to see the model summary")
    print("")
    print("________________________________________________________")

    self.__list_avg_input_feature_by_cls = __list_input_avg
    self.__list_err_in_train_by_cls = __list_input_avg_err_by_cls

    self.__train_done = True

  def model_summary(self):
    '''This function report the summary of the model'''

    if self.__train_done:
      _number_of_training_cases = self.__img_cls_representatives_list
      # _number_of_zone = len(self.__zone_dist_percents)
      _main_norm = self.__main_norm
      _rad = self.__radius

      _num_cls = self.__numcls

      _star = "*" * 8
      print(_star)
      print(f"The model summary as follows:")
      print("")
      print(f"The number of training cases as follows by class:")
      for itm_inx in range(len(_number_of_training_cases)):
        print(f"for class {_num_cls[itm_inx]}, you have got ({len(_number_of_training_cases[itm_inx])})")

      print(f"The model will be predicting ({len(_num_cls)}) of classes, as follows:")
      for cls in _num_cls:
        print(f"Class name: {cls}")
      print("")
      # print(f"The number of zones for this set constructed with radius ({_rad}) is ({_number_of_zone}). Check the zone report for details")
      print(f"The main norm for the input feature of this model is ({_main_norm})")
      print(_star)
    else:
      print(" *********************WARNING***********************")
      print("You have missed to construct the train model. please make sure is done before summary and save")


  # ***************SAVE MODEL CONSTRUIONT *****************************************
  def save_model(self, file_name, img=False):
    '''This function to save h5 type of module with data as needed'''
    if self.__train_done:

      if img == False:
        __radius = self.__radius
        __acc_report = np.array([__radius, self.__inner_radius_based_on_dist, self.__main_norm])
      else:

        __cls_name_and_code = []
        for itm_inx in range(len(self.__cls_names_img_input)):
          __cls_name = self.__cls_names_img_input[itm_inx]
          __cls_inx_number = self.__numcls_img[itm_inx]

          __cls_name_and_code.append([__cls_name, str(__cls_inx_number)])
        __radius = self.__radius_img
        __acc_report = np.array([__radius, self.__inner_radius_based_on_dist, self.__main_norm])


      _train_dataset_with_cls = np.column_stack((self.__ds, self.__cls))
      _avg_input_feature_by_cls = self.__list_avg_input_feature_by_cls
      _avg_err_by_cls = self.__list_err_in_train_by_cls

      _model_acc = __acc_report

      _img_cls_repres = self.__img_cls_representatives_list

      _name = file_name + '.hdf5'

      with h5py.File(_name, 'w') as f:

          f.create_dataset("train_ds", data = _train_dataset_with_cls)
          f.create_dataset("avg_input", data = _avg_input_feature_by_cls)
          f.create_dataset("avg_err", data = _avg_err_by_cls)
          f.create_dataset("model_acc", data = _model_acc)
          f.create_dataset("cls_img_repres", data = _img_cls_repres)

          if img == True:
            string_dt = h5py.string_dtype(encoding='utf-8')
            f.create_dataset("model_cls_name_code", data = __cls_name_and_code, dtype=string_dt)

      print(f"The file is saved at: {os.getcwd()}")
      print(f"It's named as {file_name}.hdf5")

    else:
      print("You can't save the model before you make sure that the train is done. please do so.")

  # *****************LOAD MODEL CONSTRUCTION **************************************
  def load_model(self, model_path, img=False):
    '''this function responsible to load the model's parameters'''
    try:

      if img == True:
        __model_cls_name_code = []

      _train_set_model, _model_acc, _list_input_avg, _list_err_avg, _img_represn_cls, _zone_summary, _zone_vals_border = [], [], [], [], [], [], []
      with h5py.File(model_path, 'r+') as f:
        for j in f['model_acc']:
          _model_acc.append(j)
        # for b in f['zone_summary']:
        #   _zone_summary.append(b)
        for inavg in f['avg_input']:
          _list_input_avg.append(inavg)
        for eravg in f['avg_err']:
          _list_err_avg.append(eravg)
        for i in f['train_ds']:
          _train_set_model.append(i)
        for i in f['cls_img_repres']:
          _img_represn_cls.append(i)
        # for i in f['zone_vals_border']:
        #   _zone_vals_border.append(i)

        if img == True:
          for i in f['model_cls_name_code']:
            __model_cls_name_code.append(i)

      _train_set_model = np.array(_train_set_model)
      # _zone_summary = np.array(_zone_summary)
      _list_input_avg = np.array(_list_input_avg)
      _list_err_avg = np.array(_list_err_avg)
      # _zone_vals_border = np.array(_zone_vals_border)


      _len_input_feature = _train_set_model.shape[1]-1

      _X_ds_history = _train_set_model[:,:_len_input_feature]
      _y_cls_history = _train_set_model[:,-1]

      self.__history_X_ds = _X_ds_history
      self.__history_y_cls = _y_cls_history
      # self.__loaded_model_zone_summary = _zone_summary
      self.__loaded_model_list_input_avg = _list_input_avg
      self.__loaded_model_list_err_avg = _list_err_avg
      # self.__loaded_zone_val_borders_list = _zone_vals_border
      self.__loaded_img_cls_representatives_list = _img_represn_cls

      self.__loaded_model_acc = _model_acc
      self.__loaded_model_main_norm = self.__loaded_model_acc[2]


      if img == True:
        _name_code = __model_cls_name_code
        self.__cls_name_and_code = _name_code

      self.__loaded_model_verification = True

    except Exception as e:
      print("The model you are loading is not readable to BireyselValue library")
      print(f"reported error: {e}")

  def loaded_model_summary(self, img=False):
    '''This function give summary on the loaded model's parameters'''

    if self.__loaded_model_verification:

      __loaded_model_num_of_cls = []
      for i in Counter(self.__history_y_cls):
        __loaded_model_num_of_cls.append(i)

      star = '*' * 8
      print(star)
      print(f"general norm {self.__loaded_model_main_norm}")
      print(f"RADIUS by user of {self.__loaded_model_acc[0]}, and RADIUS by the function is {self.__loaded_model_acc[1]}")
      print(f"The prediction of this model will be on length of {len(__loaded_model_num_of_cls)} CLASSES ONLY")
      print(f"You expect the prediction on one of the classes {__loaded_model_num_of_cls}")
      if img == False:
        print(f"Your inpurt feature must have the length of {self.__history_X_ds.shape[1]} features ONLY")
      else:
        print(f"Your input feature must be of an img type only for this model, supported type .png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif")
        print(f"The expected prediction class name and code of this model as follows:")
        for itm in self.__cls_name_and_code:
          _name = str(itm[0],'utf-8')
          _code = str(itm[1],'utf-8')
          print(f"The class name is {_name}, and the class code is {_code}")

      print("If you are in line with all of that you can now use PREDICT_TEST or PREDICT to proceed")
      print(star)

   #  *************Predict img test construction ********************************
  def __predict_test_img(self, path):
    '''this function is predict imgs test on the loaded model, so the loaded model must be verified '''
    if self.__loaded_model_verification == True:
      star = '*' * 10
      print(star)
      print("Essential prediction test on the img folders has just started please don't stop")
      print("This Library- bp_a.v.1.0 - is the first edition of the BireyselValue Algorithm by Dr. Deniz Dahman's. Visit dahmansphi.com")
      print(star)

      __main_list_of_all_test_imgs = []
      __folder_cls_names = []
      for folder_names in listdir(path):
        __dot = '.'
        isValidName = __dot in folder_names

        if isValidName == False:
          __folder_cls_names.append(folder_names)

      print(f"we found in the path {len(__folder_cls_names)} number of folders ")
      for cls_folder_name in __folder_cls_names:

        __last_char_in_path = path[-1]
        isLastChar = __last_char_in_path == '/'

        __last_char_in_new_path = ''
        if isLastChar == False:
          __last_char_in_new_path = '/'

        __cls_code_number = __folder_cls_names.index(cls_folder_name)
        __new_path = path + __last_char_in_new_path + cls_folder_name + '/'
        for img_name in listdir(__new_path):
          __img = __new_path + img_name
          isNameImage = __img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
          if isNameImage:
            print(f"we found the image ( {img_name} ) is ok and it's in process for shaping")

            image = Image.open(__img).convert('L')
            __img_hight, __img_width = image.size

            isHight = __img_hight >  30
            isWidth = __img_width > 30

            if isHight and isWidth:

              __resized_img = image.resize((20, 20))

              __img_to_np = asarray(__resized_img)

              __img_flatten = __img_to_np.flatten()
              __img_flatten = np.append(__img_flatten, [__cls_code_number])
              __img_flatten = list(__img_flatten)
              __main_list_of_all_test_imgs.append(__img_flatten)

      __main_list_of_all_test_imgs = np.array(__main_list_of_all_test_imgs)

      if __main_list_of_all_test_imgs.any():
        print(f"We are going to predict test on {len(__main_list_of_all_test_imgs)} number of images")
        __ds_img_test = __main_list_of_all_test_imgs[:,:400]
        __cls_img_test = __main_list_of_all_test_imgs[:,-1]

        self.__predict_X_ds_test = __ds_img_test/self.__loaded_model_main_norm
        self.__predict_y_cls_test = __cls_img_test
        self.__radius_test = self.__loaded_model_acc[0]

        __temp_cls_num_test = []
        for cls_num in Counter(self.__history_y_cls):
          __temp_cls_num_test.append(cls_num)
        self.__numcls_test = np.array(__temp_cls_num_test)

        self.__input_feature = True
        self.build(radius=self.__loaded_model_acc[2], predict=True, test=True, img=True)
        self.__predict_test_verification = True
        self.__predict_test_handller()

        print("We are on process for build now ........")
      else:
        print("None of your folder contain a valid img for test of prediction, check the type of img and if you have one at the first place")

  # ******************** predict test construction side on csv type of dataset
  def predict_test(self, input_test_feature, cls_test_feature):
    '''This function do the prediction a test dataset that must have input of the ds and cls as well, and its csv type'''
    if self.__loaded_model_verification:
      _dim_module_input_feature = self.__history_X_ds.shape[1]


      isInputX_np =  type(input_test_feature).__module__ == np.__name__
      isInputCls_np = type(cls_test_feature).__module__ == np.__name__
      if isInputX_np and isInputCls_np:

        isOneCaseOrSet = len(input_test_feature.shape)
        _dim_input_test_feature = None
        _dim_to_compare_cls_X_same_size = None

        if isOneCaseOrSet > 1 and isOneCaseOrSet < 3:
          _dim_input_test_feature = input_test_feature.shape[1]
          _dim_to_compare_cls_X_same_size = input_test_feature.shape[0]
        else:
          _dim_input_test_feature = input_test_feature.shape[0]
          _dim_to_compare_cls_X_same_size = 1

        if _dim_input_test_feature:
          isInputX_dim = _dim_input_test_feature == _dim_module_input_feature

          isCls_dim = len(cls_test_feature.shape) == 1
          isClsAndXSameSize = len(cls_test_feature) == _dim_to_compare_cls_X_same_size
          if isInputX_dim and isCls_dim and isClsAndXSameSize:

            self.__predict_X_ds_test = input_test_feature/self.__loaded_model_main_norm
            self.__predict_y_cls_test = cls_test_feature
            self.__radius_test = self.__loaded_model_acc[0]

            __temp_cls_num_test = []
            for cls_num in Counter(self.__history_y_cls):
              __temp_cls_num_test.append(cls_num)
            self.__numcls_test = np.array(__temp_cls_num_test)

            self.__input_feature = True
            self.build(radius=self.__radius_test, predict=True, test=True)
            self.__predict_test_verification = True
            self.__predict_test_handller()
          else:
            print(f"The dimension of the Input feature for this model must be {_dim_module_input_feature}, and the class inpurt feature must be of 1 dimension and both input and class ds must be of same size")
      else:
        print("The loaded case must be of numpy type of array")

  def __predict_test_handller(self):
    '''this function is the predict hunddler, which does the actual work'''
    if self.__predict_test_verification:
      print("Prediction test has just started please follow the report, thank you")
      print("This Library- bp_a.v.1.0 - is the first edition of the BireyselValue Algorithm by Dr. Deniz Dahman's. Visit dahmansphi.com")
      # _zone_vals = self.__loaded_zone_val_borders_list
      # _zone_list_dist = self.__loaded_model_zone_summary

      _final_res = []

      X = self.__predictDS_test
      y = self.__predict_y_cls_test

      _avg_data_input_feature = self.__loaded_model_list_input_avg
      _avg_err = self.__loaded_model_list_err_avg

      _right_count = 0

      for inpt in range(len(X)):
        _avg_input_subtract_avg_data_input = _avg_data_input_feature
        _avg_err_subtract_avg_err = _avg_err

        _avg_input_feature = np.sum(self.__predict_X_ds_test[inpt])

        _neighbor_list = X[inpt]
        _actual_cls = y[inpt]

        _avg_input_subtract_avg_data_input = np.sqrt((_avg_input_subtract_avg_data_input - _avg_input_feature)**2)
        _avg_err_subtract_avg_err = np.sqrt((_avg_err_subtract_avg_err - _avg_input_feature)**2)

        _sum_neigbor = np.sum(_neighbor_list)
        if _sum_neigbor == 0:
          _neighbor_list = _neighbor_list
        else:
          _neighbor_list = _neighbor_list/_sum_neigbor

        _mat_input = np.vstack((_avg_input_subtract_avg_data_input, _avg_err_subtract_avg_err))
        _mat_input = np.vstack((_mat_input, _neighbor_list))
        _mat_input = _mat_input.T

        _actual_cls_inx = np.where(self.__numcls_test == y[inpt])[0][0]
        _actual_cls_val = self.__numcls_test[_actual_cls_inx]

        col_wise_max = np.max(_mat_input,axis=0)
        col_wise_min = np.min(_mat_input,axis=0)

        __indx_col_wise_max = []
        __inx_col_wise_min = []

        for __col_val in range(_mat_input.shape[1]):

          vmax = col_wise_max[__col_val]
          vmin = col_wise_min[__col_val]

          inxxmax = np.where(_mat_input[:,__col_val] == vmax)[0][0]
          inxxmin = np.where(_mat_input[:,__col_val] == vmin)[0][0]

          __indx_col_wise_max.append(inxxmax)
          __inx_col_wise_min.append(inxxmin)

        __indx_col_wise_max = np.array(__indx_col_wise_max)
        __inx_col_wise_min = np.array(__inx_col_wise_min)

        _mat_input_final_img = np.vstack((__indx_col_wise_max, __inx_col_wise_min))

        _mat_input_final_img_flatten = _mat_input_final_img.flatten()

        flgs = np.zeros(len(self.__numcls_test))

        for inx in range(len(self.__loaded_img_cls_representatives_list)):

          for itms in self.__loaded_img_cls_representatives_list[inx]:
            _itm_tocompar = itms
            isEq = np.array_equal(_mat_input_final_img_flatten, _itm_tocompar)
            if isEq:
              flgs[inx] +=1

        _sum_flgs = np.sum(flgs)
        if _sum_flgs == 0:
          flgs = flgs
        else:
          flgs = flgs/_sum_flgs

        _predict_val = np.max(flgs)
        _predict_inx = np.where(flgs == _predict_val)[0][0]

        print("predict by neighbors :*********************")
        print(flgs)
        print('actul is ', _actual_cls_inx, 'predict', _predict_inx)
        if _actual_cls_inx == _predict_inx:
          _right_count +=1
        print("__________________________________________")
        print("*****************END*********************************")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

      _total_acc = (_right_count/len(X)) * 100
      print(f" Your prediction test has accuracy of {_total_acc} %, by neighbors:")

  def __predict(self, input_predict_feature):
    '''This function does the prediction without test, it's the final product'''
    if self.__loaded_model_verification:
      _dim_module_input_feature = self.__history_X_ds.shape[1]

      isInputX_np =  type(input_predict_feature).__module__ == np.__name__

      if isInputX_np:

        isOneCaseOrSet = len(input_predict_feature.shape)
        _dim_input_predict_feature = None

        if isOneCaseOrSet > 1 and isOneCaseOrSet < 3:
          _dim_input_predict_feature = input_predict_feature.shape[1]
        else:
          _dim_input_predict_feature = input_predict_feature.shape[0]

        if _dim_input_predict_feature:
          isInputX_dim = _dim_input_predict_feature == _dim_module_input_feature
          if isInputX_dim:

            self.__predict_X_ds_predict = input_predict_feature/self.__loaded_model_main_norm
            self.__radius_predict = self.__loaded_model_acc[2]
            __temp_cls_num_predict = []
            for cls_num in Counter(self.__history_y_cls):
              __temp_cls_num_predict.append(cls_num)
            self.__numcls_predict = np.array(__temp_cls_num_predict)

            self.__input_feature = True
            self.build(predict=True, test=False)
            self.__predict_predict_verification = True
            __res_predict = self.__predict_predict_handller()
            return __res_predict
          else:
            print(f"The dimension of the Input feature for this model must be {_dim_module_input_feature}")
      else:
        print("The loaded case must be of numpy type of array")

  def __predict_predict_handller(self):
    '''This function is hundller of the predict with no test'''
    if self.__predict_predict_verification:
      X = self.__predictDS_predict
      w = self.__loaded_model_alphas
      # do the prediction
      __result_prediction = []
      for itm in range(len(X)):
        x = X[itm]
        _bireysel_list_equation = []
        for j in range(len(w)):
          tem = abs(x[j] * w[j])
          _bireysel_list_equation.append(tem)

        _predicted_cls_inx = _bireysel_list_equation.index(max(_bireysel_list_equation))
        _predicted_cls = self.__numcls_predict[_predicted_cls_inx]
        __result_prediction.append(_predicted_cls)

        star = "*" * 8
        print(star)
        print(f"Predicted class for the input feature {self.__predict_X_ds_predict[itm]} is class {_predicted_cls}")

      __result_prediction = np.array(__result_prediction)
      return __result_prediction
