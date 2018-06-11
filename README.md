# eng2chs
一个利用爬虫爬取谷歌翻译用于英译中的小模块<br> 
getip和readip分别用于获取ip和读取ip用于爬虫防止被谷歌封禁<br> 
主要功能文件为go.py<br> 
可通过pip安装使用<br> 
>pip install eng2chs

--------------------------------
# demo
>from eng2chs import go<br>

>f_trans = go.tfunction()<br>
>temp = 'Chinese'             #待翻译内容<br>
>String = f_trans.trans(temp)<br>
