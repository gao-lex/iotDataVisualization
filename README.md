# iotFarmer


基于Echarts和bootstrap、温湿度、光照动态可视化

项目依赖：

```bash
pip3 install pyserial
```

使用方法：

1. 连接协调器、温湿度传感器、光强传感器、电机模块
2. Linux的话`sudo chmod 777 /dev/ttyUSB0`
3. 启动相应功能，如下：

```
python3 -m http.server //