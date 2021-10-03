## nginx 反向代理
``` 
浏览器 ------->   http://101.37.149.193(:80) --->nginx转发,同时修改请求头  Get /hello ------->101.37.149.193:10086 ------> main
```
## server的配置
```
server{
    listen           80;                     # 监听的端口号，此处设为了http默认的80端口
    server_name      101.37.149.193;         # 网络服务器的IP或者域名
    location / {                             # / 表示将对IP的直接访问转发给目的地
    proxy_pass       http://127.0.0.1:10086; # 转发目的地
    proxy_set_header Get /hello;             # 同时修改请求头信息
    }
}
```
