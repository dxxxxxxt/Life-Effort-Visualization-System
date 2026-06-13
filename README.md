# 人生努力可视化系统

一个帮助用户记录每日努力、追踪能力成长的 Web 应用。通过游戏化的打卡机制、经验值系统和成就勋章，激励用户持续进步。

## 功能特性

- **每日打卡** - 7个能力维度：科研学习、编程能力、自媒体、运动健身、表达能力、竞赛能力、化妆技术
- **能力雷达图** - 可视化展示各项能力成长
- **经验值系统** - 打卡获得经验，10级成长体系
- **成就勋章** - 10+成就等你解锁
- **经验日历** - 日历视图显示每日获得的经验值
- **统计报表** - 周/月/年数据统计
- **心情日记** - 记录每日心情和笔记
- **目标管理** - 设定目标追踪进度
- **头像上传** - 个性化用户头像

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | Python Flask |
| 数据库 | SQLite + SQLAlchemy |
| 用户认证 | Flask-Login |
| 前端 | HTML / CSS / JavaScript |
| 数据可视化 | ECharts |
| 图标 | Font Awesome |

## 项目结构

```
人生计划清单/
├── app.py              # 应用入口
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── models/             # 数据模型
│   ├── __init__.py
│   ├── user.py         # 用户模型
│   ├── ability.py      # 能力模型
│   ├── checkin.py      # 打卡模型
│   ├── achievement.py  # 成就模型
│   ├── note.py         # 笔记模型
│   └── goal.py         # 目标模型
├── routes/             # API路由
│   ├── auth.py         # 认证接口
│   ├── checkin.py      # 打卡接口
│   ├── abilities.py    # 能力接口
│   ├── stats.py        # 统计接口
│   ├── achievement.py  # 成就接口
│   ├── note.py         # 笔记接口
│   └── goal.py         # 目标接口
├── services/           # 业务逻辑
│   ├── exp_service.py  # 经验值服务
│   └── achievement_service.py  # 成就服务
├── templates/          # HTML模板
│   ├── index.html      # 登录/注册页
│   ├── dashboard.html  # 仪表盘
│   ├── stats.html      # 统计页
│   ├── achievements.html  # 成就页
│   ├── notes.html      # 笔记页
│   └── goals.html      # 目标页
├── static/             # 静态资源
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript文件
│   └── img/            # 图片资源
│       └── avatars/    # 用户头像
├── data/               # 数据库文件
│   └── life_tracker.db
└── init_db.py          # 数据库初始化
```

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/Life-Effort-Visualization-System.git
cd Life-Effort-Visualization-System
```

2. **安装依赖**
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

3. **运行应用**
```bash
python app.py
```

4. **访问网站**

打开浏览器访问 http://127.0.0.1:5000

### 使用不同 Python 环境

如果系统有多个 Python 环境，指定正确的 Python 路径：

```bash
"C:\Users\你的用户名\AppData\Local\Programs\Python\Python313\python.exe" app.py
```

## 配置说明

### 数据库配置

默认使用 SQLite，数据库文件位于 `data/life_tracker.db`。

如需使用其他数据库，修改 `config.py`：

```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/db_name'
```

### 密钥配置

生产环境请修改 `config.py` 中的密钥：

```python
SECRET_KEY = 'your-secret-key-here'
```

## 使用指南

### 注册账号

1. 访问网站首页
2. 点击"注册"标签
3. 填写用户名、密码
4. 可选：上传头像
5. 点击注册按钮

### 每日打卡

1. 登录后进入仪表盘
2. 点击能力卡片的"打卡"按钮
3. 每项能力每天只能打卡一次
4. 打卡获得 10+ 经验值

### 查看成长

- **仪表盘**：查看打卡进度、能力雷达图
- **经验日历**：右侧日历显示每日经验值
- **统计页面**：查看详细统计数据
- **成就页面**：查看已获得的成就

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/logout` | POST | 用户登出 |
| `/api/auth/profile` | GET | 获取用户信息 |
| `/api/checkin` | POST | 打卡 |
| `/api/checkin/today` | GET | 今日打卡状态 |
| `/api/checkin/calendar` | GET | 日历数据 |
| `/api/abilities` | GET | 能力列表 |
| `/api/abilities/user` | GET | 用户能力值 |
| `/api/stats/summary` | GET | 统计摘要 |
| `/api/achievements/user` | GET | 用户成就 |

## 部署指南

### 本地运行

适合个人使用或局域网内分享。

### 云服务器部署

1. 购买云服务器（阿里云、腾讯云等）
2. 安装 Python 环境
3. 上传项目代码
4. 使用 Gunicorn 或 uWSGI 运行
5. 配置 Nginx 反向代理

### 内网穿透

使用 ngrok 等工具临时暴露到公网：

```bash
ngrok http 5000
```

## 开发说明

### 添加新能力

在 `init_db.py` 中的 `init_abilities()` 函数添加：

```python
Ability(name='新能力', icon='icon-name', color='#color', description='描述')
```

### 添加新成就

在 `init_db.py` 中的 `init_achievements()` 函数添加：

```python
Achievement(
    name='成就名称',
    icon='icon-name',
    description='解锁条件',
    condition_type='类型',
    condition_value=数值
)
```

## 截图预览

### 登录页面
![登录页面](docs/login.png)

### 仪表盘
![仪表盘](docs/dashboard.png)

### 统计页面
![统计页面](docs/stats.png)

## 常见问题

**Q: 忘记密码怎么办？**

A: 目前暂无找回密码功能，可联系管理员重置或重新注册账号。

**Q: 数据会丢失吗？**

A: 数据存储在 SQLite 数据库中，建议定期备份 `data/life_tracker.db` 文件。

**Q: 如何让朋友访问？**

A: 
- 局域网：确保在同一网络，使用你的局域网 IP 访问
- 外网：使用内网穿透工具或部署到云服务器

## 更新日志

### v1.0.0 (2026)
- 初始版本发布
- 实现打卡、经验值、成就系统
- 实现能力雷达图可视化
- 实现统计报表功能

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request



## 致谢

- [Flask](https://flask.palletsprojects.com/) - Web框架
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [Font Awesome](https://fontawesome.com/) - 图标库


