from tensorflow import keras
import pandas as pd
import numpy as np

model_1 = keras.models.load_model('model')
print("Loaded model from disk")

threat_labels = {
    0 :'normal',
    1 : 'threat'}

#threat example
email_n_pc2 = 6
email_send_mail_n_pc2 = 56
usb_mean_usb_dur = 8
workhouremail_n_pc2 = 999 
n_usb = 99
usb_mean_file_tree_len = 100
workhouremail_send_mail_n_pc2 = 99
workhourusb_n_pc0 = 7
workhourusb_mean_usb_dur = 6
usb_n_pc0 = 500
n_workhourusb = 10
http_leakf_mean_url_len = 143
http_n_pc0 = 500
day = 5

# # normal example
# email_n_pc2 = 0
# email_send_mail_n_pc2 = 0
# usb_mean_usb_dur = 0
# workhouremail_n_pc2 = 0 
# n_usb = 0
# usb_mean_file_tree_len = 0
# workhouremail_send_mail_n_pc2 = 0
# workhourusb_n_pc0 = 0
# workhourusb_mean_usb_dur = 0
# usb_n_pc0 = 0
# n_workhourusb = 0
# http_leakf_mean_url_len = 0
# http_n_pc0 = 100
# day = 5

input_list = [email_n_pc2,email_send_mail_n_pc2,usb_mean_usb_dur,workhouremail_n_pc2,n_usb,usb_mean_file_tree_len,workhouremail_send_mail_n_pc2,
         workhourusb_n_pc0,workhourusb_mean_usb_dur,usb_n_pc0,n_workhourusb,http_leakf_mean_url_len,http_n_pc0,day]

numx = np.array(input_list)
numx.shape[0]
X = np.reshape(numx, (1,14,1))

y_pred= model_1.predict(X)

preds = np.max(y_pred, axis=1)


if preds[0][0] >0.007: 
    prediction_class = 1
else:
    prediction_class = 0

prediction_label = threat_labels[prediction_class]

print(prediction_label)
