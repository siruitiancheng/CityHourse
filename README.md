# city_hourse
城市房产网站爬取
## 爬取思路
   此网站可以根据小区的名称在全国范围内找到其与之相匹配的房价信息。
在爬取过程中，发现电脑端的一级页面请求返回的response 是加密的，经过反复琢磨，发现了用浏览器上端模拟手机端请求时并没有加密，所以就去请求客户端的页面来爬取得 数据。

## 代码使用步骤：
    1.git clone + 项目地址，将代码克隆到本地
    2.使用IDE打开项目
    3.使用“pip install -r requirement.txt ” 安装项目依赖
    4.注册“阿布云”代理网站获得免费http动态代理试用机会
    5.在 proxy_ip.py 中填入自己的代理隧道验证信息（proxyUser = "****"，proxyPass = "****"）
    6.打开city_hourse.py文件，换上自己的请求头。
    7.运行city_hourse.py文件
		





