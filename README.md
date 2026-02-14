# xmum留学 - 硕士申请一站式辅助平台

面向本科生的硕士留学申请辅助平台，提供全球顶尖院校硕士专业信息、申请要求、录取难度查询，支持用户收藏院校/专业、查看申请攻略等功能。

## 技术栈

### 前端
- **Vue 3.4** + **Vite 5** — 现代前端框架
- **Pinia 2.1** — 状态管理
- **Vue Router 4** — 路由管理
- **Element Plus 2.5** — UI 组件库
- **Axios 1.6** — HTTP 请求
- **SCSS** — 样式预处理

### 后端
- **FastAPI 0.109** — 高性能异步 Web 框架
- **SQLAlchemy 2.0** — ORM
- **Pydantic 2.5** — 数据验证
- **python-jose** — JWT 认证
- **SQLite** — 轻量级数据库（开箱即用，无需额外安装）
- **Uvicorn** — ASGI 服务器

## 项目结构

```
master-application-platform/
├── frontend/                  # 前端项目
│   ├── src/
│   │   ├── components/        # 公共组件（NavBar, Footer）
│   │   ├── views/             # 页面视图
│   │   │   ├── home/          # 首页
│   │   │   ├── university/    # 院校列表/详情
│   │   │   ├── major/         # 专业列表/详情
│   │   │   ├── guide/         # 攻略列表/详情
│   │   │   ├── user/          # 登录/注册/个人中心/收藏
│   │   │   └── admin/         # 后台管理面板
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── utils/             # 工具函数（API、Logo Helper）
│   │   └── styles/            # 全局样式变量
│   ├── package.json
│   └── vite.config.js
├── backend/                   # 后端项目
│   ├── app/
│   │   ├── models/            # SQLAlchemy 数据模型
│   │   ├── schemas/           # Pydantic 数据验证
│   │   ├── routers/           # API 路由
│   │   ├── utils/             # 工具函数（JWT、密码加密）
│   │   └── config/            # 配置（数据库、应用设置）
│   ├── uploads/logos/         # 院校校徽图片（本地存储）
│   ├── main.py                # 应用入口
│   ├── init_data.py           # 初始化数据脚本
│   └── requirements.txt
└── README.md
```

## 快速开始

### 环境要求

- **Python 3.11+**（推荐使用 Conda）
- **Node.js 18+** & **npm**

### 1. 克隆项目

```bash
git clone <repository-url>
cd master-application-platform
```

### 2. 后端启动

```bash
cd backend

# 方式一：使用 Conda（推荐）
conda create -n master-app python=3.11
conda activate master-app
pip install -r requirements.txt

# 方式二：使用 venv
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量（首次运行必须执行）
# 复制 .env.example 为 .env，默认使用 SQLite，无需额外安装数据库
cp .env.example .env          # macOS/Linux
copy .env.example .env         # Windows
# 如需使用 MySQL，编辑 .env 文件切换 DATABASE_URL 即可

# 初始化数据库（首次运行必须执行，会创建 SQLite 数据库并写入初始数据）
python init_data.py

# 启动后端服务
python main.py
# 或
uvicorn main:app --host 127.0.0.1 --port 8000
```

后端服务运行在 http://localhost:8000  
API 交互文档：http://localhost:8000/docs

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务运行在 http://localhost:3000（Vite 代理 `/api` → 后端 8000 端口）

### 4. 访问应用

| 地址 | 说明 |
|------|------|
| http://localhost:3000 | 前台首页 |
| http://localhost:3000/universities | 院校库 |
| http://localhost:3000/majors | 专业库 |
| http://localhost:3000/admin | 后台管理面板 |
| http://localhost:8000/docs | API 文档 |

### 5. 默认账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 管理员 | admin@example.com | admin123 |
| 普通用户 | user@example.com | user1234 |

## 初始数据

项目内置丰富的初始数据（通过 `python init_data.py` 导入）：

| 数据类型 | 数量 | 说明 |
|----------|------|------|
| 院校 | 49 所 | 全球 QS 排名前列院校，涵盖美国、英国、加拿大、澳大利亚、中国香港、新加坡、日本、瑞士、德国、荷兰等 |
| 专业 | 130+ 个 | 计算机、商科、工程、人文社科等各类硕士专业 |
| 申请攻略 | 15 篇 | 留学申请全流程指导文章 |
| 申请案例 | 40+ 个 | 真实申请场景模拟数据 |

### 院校校徽

校徽图片已下载到本地 `backend/uploads/logos/` 目录，由后端静态文件服务提供，**无需外部网络即可显示**。

- 46 所院校使用从 Wikipedia/Wikimedia Commons 下载的真实校徽（SVG/PNG）
- 3 所院校（香港科技大学、布里斯托大学、阿姆斯特丹大学）因来源受限，使用程序生成的首字母 Logo
- 管理员可在后台「院校管理」中手动修改任意学校的 Logo URL

### 数据持久化

数据库文件为 `backend/master_application.db`（SQLite），数据**永久保存**在本地。只要不手动删除该文件或重新运行 `init_data.py`（会清空重建），数据不会丢失。

## 功能模块

### 前台用户端
- **首页** — 平台介绍、热门院校推荐、统计概览
- **院校库** — 院校卡片列表、按国家/排名/难度筛选、院校详情页
- **专业库** — 专业列表、按院校/类别/学费筛选、专业详情页
- **申请攻略** — 攻略文章列表与详情
- **用户中心** — 个人信息编辑、我的收藏（院校/专业/攻略）
- **登录/注册** — JWT Token 认证

### 后台管理端
- **数据概览** — 统计面板（院校数、专业数、用户数、攻略数）
- **院校管理** — 增删改查、Logo 管理
- **专业管理** — 增删改查、关联院校
- **攻略管理** — 增删改查、富文本内容
- **用户管理** — 用户列表、角色管理

## 数据库表结构

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| users | 用户表 | email, password, nickname, role |
| universities | 院校表 | name, country, qs_ranking, difficulty, logo_url |
| majors | 专业表 | name, university_id, category, tuition, duration |
| guides | 申请攻略表 | title, content, category, author |
| cases | 申请案例表 | university, major, gpa, language_score, result |
| collections | 收藏表 | user_id, item_type, item_id |

## API 接口概览

### 认证模块
- `POST /auth/register` — 用户注册
- `POST /auth/login` — 用户登录（返回 JWT）
- `GET /auth/me` — 获取当前用户信息

### 院校模块
- `GET /universities` — 院校列表（支持分页、筛选）
- `GET /universities/{id}` — 院校详情
- `POST/PUT/DELETE /universities` — 管理员 CRUD

### 专业模块
- `GET /majors` — 专业列表（支持分页、筛选）
- `GET /majors/{id}` — 专业详情
- `POST/PUT/DELETE /majors` — 管理员 CRUD

### 攻略模块
- `GET /guides` — 攻略列表
- `GET /guides/{id}` — 攻略详情
- `POST/PUT/DELETE /guides` — 管理员 CRUD

### 收藏模块
- `GET /collections` — 我的收藏列表
- `POST /collections` — 添加收藏
- `DELETE /collections/{id}` — 取消收藏

### 统计模块
- `GET /statistics` — 平台统计数据

完整 API 文档请启动后端后访问：http://localhost:8000/docs

## 许可证

MIT License
