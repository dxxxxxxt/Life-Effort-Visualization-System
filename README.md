# Life Tracker — 人生努力可视化系统

一个自己用的打卡小工具，用来记录每天在各项能力上花的时间，顺便用雷达图和经验值给自己一点正反馈。

> 为什么做这个？因为光靠意志力坚持太难了，把努力"可视化"之后，会更有动力每天打卡。

## 它能做什么

- **每日打卡** — 目前分了 7 个维度：科研学习、编程能力、自媒体、运动健身、表达能力、竞赛能力、化妆技术。打卡后获得经验值
- **能力雷达图** — 用 ECharts 画的，各项能力成长一目了然
- **经验值 & 等级** — 共 10 级，升级的时候挺有成就感的
- **成就勋章** — 内置了十来个成就，满足条件自动解锁
- **经验日历** — 仿 GitHub 热力图，哪天偷懒了看得一清二楚
- **统计报表** — 按周/月/年看自己的数据
- **心情日记** — 顺便记一下当天的心情
- **目标管理** — 设定目标然后追踪进度
- **头像上传** — 可以换自己的头像

## 跑起来

需要 Python 3.8 以上，用到了 bcrypt 加密密码，装一下依赖就行：

```bash
# 装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动
python app.py
```

然后浏览器打开 `http://127.0.0.1:5000`，注册个账号就能用了。

> Windows 用户如果有多个 Python 版本，可能需要用完整路径，比如 `"C:\Users\你的用户名\AppData\Local\Programs\Python\Python313\python.exe" app.py`

## 技术栈

| 层级 | 用了什么 |
|------|---------|
| 后端 | Flask + SQLAlchemy |
| 数据库 | SQLite（默认，也可以换 MySQL/PostgreSQL） |
| 用户系统 | Flask-Login |
| 前端 | 原生 HTML/CSS/JS，没有用框架 |
| 图表 | ECharts |
| 图标 | Font Awesome |

没用前端框架，主要是想保持简单——反正就几个页面，原生写得也挺顺手。

## 项目结构

```
├── app.py              # 入口
├── config.py           # 配置（数据库地址、密钥等）
├── requirements.txt    # 依赖列表
├── init_db.py          # 初始化数据库 & 默认能力/成就
├── models/             # 数据模型
├── routes/             # 接口路由
├── services/           # 业务逻辑（经验值计算、成就检测）
├── templates/          # 页面模板
├── static/             # CSS / JS / 图片
└── data/               # SQLite 数据库文件在这
```

## 配置

默认用 SQLite，数据库文件在 `data/life_tracker.db`。想换数据库的话改 `config.py`：

```python
# 比如换成 MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://用户名:密码@localhost/数据库名'
```

部署到服务器的话记得把 `SECRET_KEY` 改了，环境变量或者直接改 `config.py` 都行。

## API

如果想把打卡功能接到别的地方（比如脚本、快捷指令），可以直接调接口：

| 方法 | 路径 | 干嘛的 |
|------|------|-------|
| POST | `/api/auth/register` | 注册 |
| POST | `/api/auth/login` | 登录 |
| POST | `/api/auth/logout` | 登出 |
| GET | `/api/auth/profile` | 用户信息 |
| POST | `/api/checkin` | 打卡 |
| GET | `/api/checkin/today` | 查今天打卡了没 |
| GET | `/api/checkin/calendar` | 日历热力图数据 |
| GET | `/api/abilities` | 能力列表 |
| GET | `/api/abilities/user` | 我的能力值 |
| GET | `/api/stats/summary` | 统计摘要 |
| GET | `/api/achievements/user` | 我的成就 |

## 自定义能力 & 成就

能力和成就都是在 `init_db.py` 里初始化的，想加新的改那里就行：

```python
# 加一个能力维度
Ability(name='新能力', icon='fa-star', color='#FF6B6B', description='描述')

# 加一个成就
Achievement(
    name='成就名',
    icon='fa-trophy',
    description='解锁条件',
    condition_type='checkin_count',
    condition_value=100
)
```

改完跑一次 `python init_db.py`。

## 部署

自己用的话本地跑就行。想分享给朋友：

- **局域网** — 同一 WiFi 下用你电脑的局域网 IP 访问（比如 `192.168.1.xxx:5000`）
- **公网** — 用 ngrok 临时穿透：`ngrok http 5000`
- **服务器** — 扔到云服务器上用 Gunicorn + Nginx 跑

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 可能想知道的

**数据怎么备份？**
把 `data/life_tracker.db` 复制一份就行，就这一个文件。

**忘记密码怎么办？**
目前没有找回密码功能，要么重新注册一个号，要么直接改数据库（密码是 bcrypt 加密的，需要先在线生成一个 hash 替换进去）。

**手机能用吗？**
浏览器打开没问题，样式做了响应式。

## 如果你想改着玩

欢迎 Fork 和 PR。大概流程：

1. Fork 一份
2. 建个分支 `git checkout -b feature/想加的功能`
3. 改完提交 `git commit -m '加了xxx'`
4. Push 上来然后提 PR

## 用了这些开源项目

- [Flask](https://flask.palletsprojects.com/)
- [ECharts](https://echarts.apache.org/)
- [Font Awesome](https://fontawesome.com/)
