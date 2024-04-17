import mysql.connector
import datetime
import pytz

tanggal = ''
origin = ''
latitude = ''
longitude = ''
depth = ''
mag = ''
sumber = 'angkasa'

fileinput = 'mailexportfile.txt'
# baca isi file input dan buka file output
file = open(fileinput,'r')
baris = file.readlines()
for i in range(20):
    baris[i]=baris[i].split()
    if len(baris[i])>0 and baris[i][0]=='Date':
        tanggal = baris[i][1]

    if len(baris[i])>0 and baris[i][0]=='Time':
        origin = baris[i][1]
        origin = origin.split('.')[0]

    if len(baris[i])>0 and baris[i][0]=='Latitude':
        latitude = baris[i][1]

    if len(baris[i])>0 and baris[i][0]=='Longitude':
        longitude = baris[i][1]

    if len(baris[i])>0 and baris[i][0]=='Depth':
        depth = baris[i][1]

    if len(baris[i])>0 and baris[i][0]=='M':
        mag = baris[i][1]

file.close()

utc_now = datetime.datetime.now(pytz.utc)
formatted_datetime = utc_now.strftime("%Y-%m-%d %H:%M:%S")
formatted_datetime = datetime.datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
tanggalorigin = tanggal +' '+ origin
tanggalorigin = datetime.datetime.strptime(tanggalorigin, "%Y-%m-%d %H:%M:%S")

delta_time = formatted_datetime - tanggalorigin 
delta_time = delta_time.total_seconds()
hours = int(delta_time // 3600)
minutes = int((delta_time % 3600) // 60)
seconds = int(delta_time % 60)

dalam_seconds = delta_time 
# Format the time difference
delta_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

selisih = ''

if dalam_seconds <= 300 :
    selisih = delta_time+' '+ 'EARLY BIRD'
    # print (selisih)
elif dalam_seconds > 300 and dalam_seconds <= 600 :
    selisih = delta_time+' '+ 'ON TIME'
    # print (selisih)
else:
    selisih = delta_time+' '+ 'LATE'
    # print (selisih)

print(dalam_seconds)

#inisiasi database
host = "localhost"
user = "admin"
password = "su97696"
database = "datin"

mag_type = 'M'
ket = 'ket'
petugas = 'umum'
try: 
    ##conn = sqlite3.connect('jambari.db')
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    from datetime import datetime
    created_at = datetime.now(pytz.utc)
    # print("Connection to the database successful!")
    cursor = conn.cursor()
    data = (tanggal, origin, latitude, longitude, mag, mag_type, depth,ket, sumber,petugas, created_at, selisih )
    sql = "INSERT INTO gempas (tanggal,origin, lintang, bujur, magnitudo, type, depth, ket, sumber, petugas, created_at, delta) VALUES (%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
except mysql.connector.Error  as err:
    print(f"Error connecting to the database: {err}")


