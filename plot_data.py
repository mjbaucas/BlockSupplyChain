import matplotlib.pyplot as plt 
import numpy as np

# API vs TCP/IP
rfid_api = [2120.33, 2149.33, 2119.33, 2145.33]
rfid_tcp = [2610.67, 2618.67, 1528, 1282]
temp_api = [91.33, 95.67, 91.33, 92.67]
temp_tcp = [95, 87, 53,67, 41]

# Private vs Public
rfid_private = [2120.33, 2149.33, 2119.33, 2145.33]
rfid_public  = [700, 568, 462.67, 385]
overall_private = [2120.33, 2245, 9619.33, 16003.33]
overall_public = [700, 655, 993.33, 1196,67]
1
distance_tick = np.arange(4)
distance_label = [1, 2, 3, 4]

# RFID API vs RFID TCP
plt.figure(0)
plt.plot(distance_tick, rfid_api, label="API")
plt.plot(distance_tick, rfid_tcp, label="TCP/IP")
plt.legend()
plt.xticks(distance_tick, distance_label)
plt.ylabel("Throughput (data transactions)")
plt.xlabel("Number of devices")
plt.savefig('plotRFID_API_TCP.png')

# Temp API vs Temp TCP
plt.figure(0)
plt.plot(distance_tick, temp_api, label="API")
plt.plot(distance_tick, temp_tcp, label="TCP/IP")
plt.legend()
plt.xticks(distance_tick, distance_label)
plt.ylabel("Throughput (data transactions)")
plt.xlabel("Number of devices")
plt.savefig('plotTemp_API_TCP.png')

# RFID Private vs RFID Public
plt.figure(0)
plt.plot(distance_tick, rfid_private, label="Private")
plt.plot(distance_tick, rfid_public, label="Public")
plt.legend()
plt.xticks(distance_tick, distance_label)
plt.ylabel("Throughput (data transactions)")
plt.xlabel("Number of devices")
plt.savefig('plotRFID_Priv_Pub.png')


# RFID Private vs RFID Public
plt.figure(0)
plt.plot(distance_tick, overall_private, label="Private")
plt.plot(distance_tick, overall_public, label="Public")
plt.legend()
plt.xticks(distance_tick, distance_label)
plt.ylabel("Throughput (data transactions)")
plt.xlabel("Number of devices")
plt.savefig('plotAll_Priv_Pub.png')