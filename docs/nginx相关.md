## nginx 反向代理
``` 
浏览器 ------->   http://101.37.149.193(:80) --->nginx转发 ------->http://101.37.149.193:10086/hello ------> main
```
## server的配置
```
server{
    listen           80;                           # 监听的端口号，此处设为了http默认的80端口
    server_name      101.37.149.193;               # 网络服务器的IP或者域名
    location / {                                   # / 表示将对IP的访问将被转发
    proxy_pass       http://127.0.0.1:10086/hello; # 转发目的地
    }
}
```
> 注意转发目的地地址末尾有无 / 的问题  
> 加/，表示绝对根路径；不加/，表示相对路径，匹配的路径也会转发
