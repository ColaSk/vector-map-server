# README

## 0. 基础

本项目是一个基于 mbtiles 的矢量瓦片地图服务。

### 0.0 什么是 **mbtiles**

mbtiles 实际实际上是一个 sqlite 的文件，但它同时也是一个**协议**，它要求 db 至少必须包含如下表和字段：

1. tiles 表(也有可能是view)

这张表记录了在某个坐标系下 Z，Y，X 对应的二进制文件，这个文件可以是 png 文件（光栅瓦片）也可以是 pbf 文件（矢量瓦片），具体的格式记录在 metadata 表中。

|字段|类型|备注|
|---|---|---|
|zoom_level|int|缩放|
|tile_column|int|x|
|tile_row|int|y|
|tile_data|blob|二进制瓦片数据|

一般情况下会建立 (zoom_level, tile_column, tile_row) 的唯一索引

2. metadata 表(也有可能是view)

|字段|类型|备注|
|---|---|---|
|name|text||
|value|text||

### 0.1 什么是**矢量瓦片**

### 0.2 项目原地址

项目原地址为 [github](https://github.com/systemed/tilemaker/tree/master/server)

本项目做了如下改造：

1. 使用 Python 重写（原项目 ruby）；
2. 将 css 和 js fonts 以及其他静态文件打包至项目，以提供完整离线的服务；

示例代码中前端使用了 mapbox 提供的 gis 框架（openlayers暂未适配，但有相关接口）。

其中的 style.json 也保留默认，其他的 style 文件可以参考[这里](https://openmaptiles.org/styles/)

## 1. 依赖

`>= python 3.7`

```sh
pip install -r requirements.txt
```

## 2. 配置并运行

### 2.0 下载地图

首先先下载 [矢量瓦片地图] 数据；

### 2.1 修改配置

修改 `config.py` 下的 `MBTILES_PATH` 值，指向刚才下载的瓦片数据的路径；

或

设置 `MBTILES_PATH` 的环境变量，指向刚才下载的瓦片数据的路径：`export MBTILES_PATH=PATH_TO_MBTILES_DATA`

> MAX_AGE_TIME 项可以用来控制浏览器缓存的时间，可以开大一点，以减少服务器的压力

### 2.2 运行服务

```python
python server.py
```

浏览器打开下列地址查看：

```sh
http://127.0.0.1:8000
```


## 3. docker 启动

```sh
docker-compose up -d
```
