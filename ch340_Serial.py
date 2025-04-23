import serial
import time
import serial.tools.list_ports
import  random1
#serial.tools.list_ports.comports() 来获取所有可用的串口，并打印它们的设备名称
ports = serial.tools.list_ports.comports()
com_list = []
for port in ports:
    print(port.device)
    com_list.append(port.device)
print(com_list)
try:
    # 设置串口参数并打开串口
    ser = serial.Serial(com_list[0], 115200, timeout=1)
    print('串口以成功打开')
except serial.SerialException as e:
    print(f"打开串口失败:{e}")

list_key = {
    'win': 0x8,
    'a' :0x04,
    'b' :0x05,
    'right': 0x4f, #右边
    'left' : 0x50, #左边
    'down': 0x51, #下箭头
    'up': 0x52, #上箭头

}
def keyboard_down(one_key = 0x00, two_key = 0x00, three_key = 0x00, four_key = 0x00, five_key = 0x00, six_key = 0x00, ts_key = 0x00):
    keyboard = [0x01, ts_key, 0x00, one_key,     two_key, three_key, four_key, five_key, six_key]
    #keyboard = [0x01, 0x00,   0x00, list_key['a'], 0x00, 0x00, 0x00, 0x00, 0x00]
    ser.write(keyboard)
    ser_data = ser.read(9)
    print(ser_data)
    #time.sleep(0.1)




mouse =[0x02, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
# 第一个参数是代表键盘特殊按键,第二个参数无效
keyboard = [0x01,  0x00, 0x00, list_key['a'], 0x00, 0x00, 0x00, 0x00, 0x00]
keyboard_ = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
print(keyboard)
time.sleep(5)
for i in range(20):
    # #发送数据
    # ser.write(keyboard)
    # #接收数据
    # ser_data = ser.read(9)
    # print("data",ser_data)
    # time.sleep(0.1)
    #
    # # 发送数据
    # ser.write(keyboard_)
    # # 接收数据
    # ser_data = ser.read(9)
    # print("data", ser_data)
    # time.sleep(1)
    keyboard_down(one_key=list_key['right '], two_key= list_key['a'])
    time.sleep(1)
    ser.write(keyboard_)
    time.sleep(0.1)
ser.close()
