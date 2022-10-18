forked from [PairZhu/NjtechScript](https://github.com/PairZhu/NjtechScript)

### 自动健康打卡（填入Authentication字段即可使用）
>加入了最新核酸检测时间，默认为上次填写的值，如需修改可自行修改getLastestPicker函数  
>由于部分学院开始查健康码，于是去除了上传虚空健康码的选项，过期后手动打卡一次，下次即可继续自动打卡  
>通过抓包方法获取请求头的Authentication字段(理论上不会过期)打卡。  
>[点击查看如何获取Authentication](./docs/get_authentication/get_authentication.md)  

### 服务器端代码（Flask）
Flask和页面文件已打包，可直接运行`src\server\main.py`，部署于树莓派、云服务器中，使用api轮询进行打卡

>我的服务器跑着demo，提交authentication即可打卡，仅供学习使用！
[demo](http://xusclub.top/fuckthehealthpunch)

### Iphone利用快捷指令自动化实现每日自动打卡
>[教程](./docs/automation/iphone_automation.md)