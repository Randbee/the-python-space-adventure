#!/usr/bin/python
import ftplib
import os
import datetime

data = datetime.datetime.now().isoformat()
data_split = data.split('T')
data = data_split[0]
### type of data used on fow download
data2 = data.replace("-", "")
year = data[: 4]
month = data[5:7]
day = data[8: ]

input_path = "/home/gloria/the-python-space-adventure/pollutants"
contaminator = [ 'pm1', 'pm2p5', 'pm10', 'uvbed', 'tcno2',
                 'tc_no']
list_hours = ['024', '025', '026','027', '028', '029',
            '030', '031', '032', '033', '034', '035',
            '036', '037', '038', '039', '040', '041',
            '042', '043','044', '045', '046', '047' ]


# location of the file in the ftp sever
path = '/DATA/CAMS_NREALTIME/'+data2+'00/'


os.chdir(input_path)
if not os.path.exists(data2):
    os.makedirs(data2)

#ftp connection
ftp = ftplib.FTP("dissemination.ecmwf.int")
ftp.login("juan.arevalo", "Swd75GxT")

ftp.cwd(path)

# griblist = os.listdir(input_path)
# for g in griblist:
#     os.remove(os.path.join(input_path, g))

path_download = "/home/gloria/the-python-space-adventure/pollutants/"+data2+"/"

for cont in contaminator:
    os.chdir(path_download)
    print path_download
    filename = 'z_cams_c_ecmf_'+data2+'000000_prod_fc_sfc_hour_param.grib'
    indicators = filename.replace("param", cont)
    if not os.path.exists(cont):
        os.makedirs(cont)
    path_cont = "/home/gloria/the-python-space-adventure/pollutants/"+data2+"/"+cont
    os.chdir(path_cont)
    for hour in list_hours:
        hour = str(hour)
        filename = indicators.replace("hour", hour)
        ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
        print 'Downloading ', filename, '...'

os.chdir(path_download)
if not os.path.exists('o3'):
    os.makedirs('o3')
path_o3 = "/home/gloria/the-python-space-adventure/pollutants/"+data2+"/o3"
os.chdir(path_o3)
o3_hour = ['024', '027', '030',  '033',
            '036', '039', '042', '045' ]
for hour in o3_hour:
    ozone ='z_cams_c_ecmf_'+data2+'000000_prod_fc_ml_hour_go3.grib'
    hour = str(hour)
    filename = ozone.replace("hour", hour)
    ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
    print 'Downloading ', filename, '...'
ftp.quit()
