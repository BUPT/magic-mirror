
# MM项目摄像头技术文档

## 硬件介绍：
清流迅公司使用的云台摄像头实际硬件提供厂家为紫荆云视公司的终端C9。
[硬件的基本参数和指标点这里](https://www.zijingcloud.com/product-terminal.html)

## 安装硬件注意事项：
1. C9需要连网，与清流迅的云端server直通，因此在网络环境下需要能够ping通如下两个地址

`ping  v.streamocean.com`
`ping  sonc.streamocean.com`

2. 为提升视频流速度，本地环境需要安装服务软件 dLR，具体安装步骤下文详述
3. dLR和C9都会与清流迅的云端服务器通讯，通讯数据流量数据信令控制，几个kbs。通信是通过UDP包，因此在首次通信时有时会比较耗时或者响应较慢。
4. 在个别情况下C9可能出现异常，比如启动后卡在logo处。这时可能需要对C9进行固件刷机，刷机步骤下文详述

### C9所需的本地服务端 dLR 安装步骤
1. 安装文件在目录dlr_install目录
`
-rw-r--r--   1 robinhe  staff  1175 Sep  2 15:57 README
drwxr-xr-x  10 robinhe  staff   320 Sep 12 11:14 dLR
drwxr-xr-x  10 robinhe  staff   320 Sep 12 11:21 install
`
2. 通过ifconfig命令查看网卡名称，目前的gpu工作站网卡名称为enp2s0
3. 修改 dLR文件夹中的lrc_config.py文件， vi lrc_config.py

`
NIC = "enp2s0"
lr_name = 'dlr_bupt'
vsp_name = 'buptvsp'
`
4. 进入install文件夹，执行命令：（无需root，ubuntu16.04和18.04均可以）


`./install.sh`

5. 关闭ubuntu自带的防火墙，请自行评估风险

`sudo ufw disable`

6. 配置服务

`/usr/local/bin/supervisord -c /etc/supervisord.conf`

7. 启动服务（192.168.8.183为GPU工作站自己的IP）

`python2.7 dlr.pyc 192.168.8.183 9001`

8. 查看进程情况

`ps -ef| grep 9001`

9. 查看服务实时日志

`tail -f lr.log  `

10. 查看网络udp状态

`netstat -uanp`

11. （可选）也可以直接在dLR文件夹目录中执行命令启动：

`nohup python2.7 dlr.pyc 9001 & `

### 固件升级说明（刷机）
#### 登录到C9后台，清除旧的固件版本（其实本步骤可以省略）
`ssh admin@172.16.1.10` —(C9 设备的IP，可以在前面液晶屏上看到)

密码：admin

1. 执行 `rm -rf /data/data/com.streamocean.ihi_desktop`
2. 执行 `rm -rf /data/dalvik-cache/data\@app\@com.streamocean.ihi_desktop-2.apk\@classes.dex`
3. 执行 `rm -rf /data/app/com.streamocean.ihi_desktop-2.apk`

#### 将wipe1.rar解压
1. 将U盘格式化为 FAT32 格式（如果不是这个格式，则不能升级）
2. 将“wipe1.rar”解压后的4个文件，全部拷贝到U盘的根目录中。
3. 将U盘插到C9 的USB口上，按电源键重启C9设备。
4. 这个过程需要5分钟，当看到屏幕上有画面输出时，就可以将U盘拔掉，执行下面第三步的升级操作。

#### 将下载完成后的固件，按照下面的步骤操作升级C9 设备
1. 将U盘格式化为 FAT32 格式（如果不是这个格式，则不能升级）
2. 将“U盘升级包"升级包.rar”解压后的7个文件，全部拷贝到U盘的根目录中。
3. 将U盘插到C9 的USB口上，按电源键重启C9设备。
4. 重启后，C9 会自动升级；整个升级过程需要10分钟。
5、升级完成之后，看到二维码的界面，再将U盘拔下来。
6、用手机扫描二维码进行账号绑定和会议的操作。

### [接口文档](http://showapi.streamocean.com/index.php?s=/37&page_id=609)

### [微信端遥控说明]()

## 当前正在由清流迅解决的问题：（2019-12-17）
1. 需要开机直接进入影像（去除或跳过二维码环节）
2. 不显示黄色码率等字样  
3. 不要画中画的小窗  
4. 不要右下角标的二维码
5. 由于摄像头是倒挂在房顶，因此影像显示是倒置的，能否转置