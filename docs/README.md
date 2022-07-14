[![](https://img.shields.io/badge/Python-3.7-red.svg)](https://www.python.org/downloads)
[![](https://img.shields.io/badge/FastAPI-0.67-yellowgreen.svg)](https://fastapi.tiangolo.com/)
[![](https://img.shields.io/badge/Vue-3.x-green.svg)](https://cn.vuejs.org/index.html)
[![](https://img.shields.io/badge/ElementUI-2.13.2-blue.svg)](https://element.eleme.io/#/zh-CN)
[![](https://img.shields.io/badge/BootstrapVue-2.21.2-blueviolet.svg)](https://code.z01.com/bootstrap-vue/)
[![](https://img.shields.io/badge/Elasticsearch-7.17.0-ff69b4.svg)](https://www.elastic.co/cn/elasticsearch/)

## 目录结构
```
├── webapi	            # 项目框架核心，做整体项目逻辑
│   ├── db              # 数据库相关
│   │   ├── dals
│   │   ├── models
│   │   ├── schemeas
│   │   ├── config.py
│   │   ├── create_datebase.sql
│   │   └── init_db.py
│   ├── routers         # 路由相关
│   │   ├── init_.py
│   │   ├── category_router.py
│   │   ├── comment_router.py
│   │   ├── post_router.py
│   │   └── user_router.py
│   ├── static
│   │   └── init_.py
│   ├── utils
│   │   ├── init_.py
│   │   ├── dependencies.py
│   │   ├── elastic.py
│   │   ├── email_util.py
│   │   ├── responses.py
│   │   └── security.py
│   ├── .env
│   ├── app.py
│   ├── app.py
│   └── setting.py
├── docs	        # 项目文档维护
│   └── README.md	# 说明文档
├── logs	        # 日志
├── scripts	        # 对项目代码质量做检测的脚本
├── tests           # 测试案例
├── venv	        # 虚拟环境
├── .gitignore      # 忽略文件
├── docker-compose.yml      # Docker编排
├── elasticsearch.dockerfile     # Docker-elasticsearch部署
└── webapp.dockerfile	# Docker-前后端部署
```
---
*后端*
* Python Web 框架：FastAPI
* 数据库：MySQL
* ORM：SQLAlchemy
* 搜索：Elasticsearch
---
*前端*
* 框架：Vue
* 管理界面：ElementUI
---
### 基本要求
* Python: 3.7.x
* MySQL: 5.7.x
* Node: 12.13.x
* Vue: 2.x
---
### 安装
*后端*
```
1: 安装Python 3.7.x，创建虚拟环境
2: 安装MySQL 5.7.x
```
*前端*
```
1: 安装Node版本 12.13.x 和 vue-cli
```
### 开发启动
*后端*
```
# 后端配置数据库和账号密码
1: cd Sakura_Admin/webapi
2: 修改.env文件

# 初始化和启动
1: cd Sakura_Admin/webaui
2: pip install -r requirements.txt
3: python3 db/init_db.py        # 如果需要初始化数据库
4: python3 app.py
5: http://localhost:8000/docs   # 进入SwaggerUI
```
*前端*
```
1: cd fastapi-vue-blog/webui
2: npm install
3: npm run dev
```
## 部署与发布
* 前提：安装好Docker和docker-compose
### 简单发布(可能不适合生产环境)
#### 构建和启动
```
# 工作目录
cd Sakura_Admin

# 1.构建镜像并启动服务
docker-compose up -d --build

# 2.初始化数据
docker-compose exec webapp python db/init_db.py
docker-compose restart

# 3.查看服务情况
docker-compose ps
```

#### 其他命令
```
# 1.重启服务
docker-compose restart

# 2.启动服务
docker-compose start <服务名称>

# 3.停止服务
docker-compose stop <服务名称>

# 4.关闭服务并移除容器
docker-compose down
```