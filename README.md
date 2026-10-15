# Social Agent Platform

AI 社交媒体运营系统 — 多平台热点采集 → AI 评分 → 内容生成 → 审核 → 定时发布 → 数据复盘

## 功能概览

- **多平台热点采集**：34 个平台（百度/抖音/B站/微博/知乎/小红书/头条/GitHub/HackerNews/X/TikTok 等）
- **AI 内容生成**：支持 DeepSeek/OpenAI/通义千问/智谱GLM/Kimi 等任意 OpenAI 兼容 API
- **热点评分**：AI 评分 + 规则评分双模式
- **内容审核流**：草稿 → 提交审核 → 批准/驳回 → 调度发布
- **定时发布**：APScheduler 定时任务，支持幂等发布
- **数据复盘**：指标采集 + 分析报告 + 策略版本管理
- **JWT 认证**：用户注册/登录/Token 验证
- **Web 管理界面**：内置前端面板

## 技术栈

- Python 3.11+ / Flask 3.0 / SQLAlchemy 2.0 / SQLite
- PyJWT (认证) / APScheduler (定时任务) / feedparser (RSS)
- httpx (HTTP) / pytest (测试)
- 前端：原生 HTML + CSS + JS，无框架依赖

## 快速安装（5 步）

### 第 1 步：克隆项目

```bash
git clone https://github.com/PengYanBen/social-agent-platform.git
cd social-agent-platform
```

### 第 2 步：创建虚拟环境并安装依赖

```bash
python3 -m venv venv
source venv/bin/activate        # Windows 用: venv\Scripts\activate
pip install -r requirements.txt
```

依赖列表（requirements.txt）：
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
SQLAlchemy==2.0.25
feedparser==6.0.10
httpx==0.26.0
APScheduler==3.10.4
python-dotenv==1.0.0
PyJWT==2.8.0
werkzeug==3.0.1
pytest==7.4.4
pytest-cov==4.1.0
```

### 第 3 步：配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，**至少需要设置以下项**：

```bash
# 必须修改：给 Flask 签名用
SECRET_KEY=你的随机密钥

# AI 配置（以 DeepSeek 为例）
AI_PROVIDER_TYPE=deepseek
AI_MODEL_API_KEY=你的API密钥
AI_MODEL_NAME=deepseek-chat
```

**AI Provider 选项说明**：

| AI_PROVIDER_TYPE | 说明 | 需要配置 |
|---|---|---|
| `deepseek` | DeepSeek | 只需 `AI_MODEL_API_KEY` |
| `openai` | OpenAI (GPT-4o 等) | 只需 `AI_MODEL_API_KEY` |
| `qwen` | 通义千问 | 只需 `AI_MODEL_API_KEY` |
| `glm` | 智谱 GLM | 只需 `AI_MODEL_API_KEY` |
| `kimi` | Moonshot Kimi | 只需 `AI_MODEL_API_KEY` |
| `ollama` | 本地 Ollama | 无需密钥 |
| `openai_compat` | 任意 OpenAI 兼容 API | 需填 `AI_MODEL_BASE_URL` + `AI_MODEL_API_KEY` |
| `none` | 不用 AI | 仅规则评分 |
| `mock` | 测试用 | 返回假数据 |

如果用 `openai_compat`（自定义 API 地址）：
```bash
AI_PROVIDER_TYPE=openai_compat
AI_MODEL_BASE_URL=https://api.deepseek.com/v1
AI_MODEL_API_KEY=你的密钥
AI_MODEL_NAME=deepseek-chat
```

### 第 4 步：启动服务

```bash
python wsgi.py
```

看到以下输出说明启动成功：
```
[INFO] app: Application created with config: development
 * Running on http://127.0.0.1:5000
```

### 第 5 步：验证

浏览器打开 `http://localhost:5000`，应看到管理界面。

或用命令行验证：
```bash
curl http://localhost:5000/api/v1/health
# 返回: {"success":true,"data":{"status":"ok","service":"social-agent-platform"}}

curl http://localhost:5000/api/v1/collectors/platforms
# 返回 34 个采集平台列表
```

## 其他启动方式

### 开发模式（热重载）

```bash
flask --app wsgi run --debug
```

### 生产模式（gunicorn）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### 后台调度器（定时采集和发布）

```bash
python scheduler.py
```

调度器会按间隔自动执行：

| 任务 | 默认间隔 | 说明 |
|---|---|---|
| 采集来源 | 60 分钟 | 从所有启用的 RSS 源采集新内容 |
| 分析热点 | 30 分钟 | 对未评分热点进行 AI 评分 |
| 发布帖子 | 5 分钟 | 发布到期的计划帖子 |
| 同步指标 | 6 小时 | 同步已发布帖子的平台指标 |

### 数据库迁移（生产环境）

```bash
export FLASK_SKIP_DB_CREATE=1
export FLASK_APP=app:create_app
flask db upgrade    # 应用已有迁移文件
```

### 运行测试

```bash
python -m pytest tests/ -v
# 98 passed
```

## API 接口列表

### 认证
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/v1/auth/register` | 用户注册 |
| POST | `/api/v1/auth/login` | 登录，返回 JWT |
| GET | `/api/v1/auth/me` | 当前用户信息（需 Token） |

### 项目和账号
| 方法 | 路径 | 说明 |
|---|---|---|
| GET/POST | `/api/v1/projects` | 项目列表/创建 |
| GET/PATCH/DELETE | `/api/v1/projects/<id>` | 项目详情/更新/删除 |
| GET/POST | `/api/v1/accounts` | 社交账号列表/创建 |
| GET/PATCH/DELETE | `/api/v1/accounts/<id>` | 账号详情/更新/删除 |

### 数据采集
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/v1/collectors/platforms` | 列出所有采集平台 |
| GET | `/api/v1/collectors/platforms/<key>` | 抓取某平台热点 |
| POST | `/api/v1/collectors/fetch` | 批量抓取多平台 |
| POST | `/api/v1/collectors/platforms/<key>/import` | 抓取并导入为热点 |
| GET/POST | `/api/v1/sources` | RSS 来源列表/创建 |
| POST | `/api/v1/sources/<id>/test` | 测试 RSS 连通性 |
| POST | `/api/v1/sources/<id>/collect` | 手动采集 RSS |

### 热点和内容
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/v1/topics` | 热点列表（支持筛选搜索） |
| POST | `/api/v1/topics/<id>/score` | 评分（AI/规则） |
| POST | `/api/v1/topics/<id>/generate-draft` | AI 生成草稿 |
| GET/POST | `/api/v1/content` | 内容创意列表/创建 |
| POST | `/api/v1/content/<id>/drafts` | 创建草稿版本 |
| POST | `/api/v1/content/<id>/drafts/<d>/submit` | 提交审核 |
| POST | `/api/v1/content/<id>/drafts/<d>/approve` | 批准 |
| POST | `/api/v1/content/<id>/drafts/<d>/reject` | 驳回 |
| POST | `/api/v1/content/<id>/drafts/<d>/schedule` | 调度发布 |

### 发布和分析
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/v1/posts` | 发布记录列表 |
| POST | `/api/v1/posts/<id>/publish` | 执行发布 |
| POST | `/api/v1/posts/<id>/cancel` | 取消发布 |
| GET | `/api/v1/analytics/overview` | 数据总览 |
| GET | `/api/v1/analytics/posts/<id>` | 单帖指标 |
| POST | `/api/v1/analytics/review` | 生成复盘报告 |
| GET/PATCH | `/api/v1/strategies/<pid>` | 策略查看/更新 |
| POST | `/api/v1/strategies/<pid>/rollback` | 策略回滚 |

## 采集平台列表

### 国内平台（18 个）
百度热搜、抖音热榜、哔哩哔哩热门、微博热搜、知乎热榜、小红书热门、头条热点、豆瓣话题、快手热榜、百度贴吧、酷安热门、36氪热门、少数派、IT之家、格隆汇、财联社、华尔街见闻、金十数据

### 国际平台（16 个）
GitHub Trending、Hacker News、Product Hunt、Reddit、TechMeme、Google Trends、BBC News、NY Times、The Guardian、NBC News、Al Jazeera、X (Twitter)、TikTok、Facebook、Instagram、YouTube

数据源通过 [NewsNow](https://github.com/ourongxing/newsnow) API 聚合。可自部署 NewsNow 并设置 `NEWSNOW_API_URL`。

## 项目结构

```
social-agent-platform/
├── app/                        # Flask 应用
│   ├── __init__.py             # Application Factory + 蓝图注册
│   ├── config.py               # 配置（开发/测试/生产）
│   ├── extensions.py           # SQLAlchemy + Migrate 实例
│   │
│   ├── api/                    # API 路由（Blueprint）
│   │   ├── auth.py             # 认证（注册/登录/me）
│   │   ├── health.py           # 健康检查
│   │   ├── projects.py         # 项目 CRUD
│   │   ├── accounts.py         # 社交账号 CRUD
│   │   ├── sources.py          # RSS 来源管理
│   │   ├── collectors.py       # 多平台热点采集
│   │   ├── topics.py           # 热点评分 + 草稿生成
│   │   ├── content.py          # 内容审核流
│   │   ├── publishing.py       # 发布管理
│   │   ├── analytics.py        # 数据分析
│   │   └── strategies.py       # 策略版本管理
│   │
│   ├── models/                 # 数据模型（19 张表）
│   │   ├── base.py             # BaseModel + TimestampMixin
│   │   ├── user.py             # 用户 + 用户-项目关联
│   │   ├── project.py          # 项目
│   │   ├── social_account.py   # 社交账号
│   │   ├── source.py           # 数据来源
│   │   ├── collected_item.py   # 采集条目
│   │   ├── topic.py            # 热点 + 热点条目 + 评分
│   │   ├── content.py          # 内容创意 + 草稿
│   │   ├── post.py             # 计划帖子 + 已发布帖子
│   │   ├── metric_snapshot.py  # 指标快照
│   │   ├── job.py              # 后台任务记录
│   │   ├── strategy.py         # 策略版本 + 实验
│   │   └── audit_log.py        # 审计日志
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── auth_service.py     # JWT 认证
│   │   ├── collector_service.py # RSS 采集
│   │   ├── topic_service.py    # 热点评分
│   │   ├── content_service.py  # 草稿生成
│   │   ├── publishing_service.py # 发布逻辑
│   │   ├── analytics_service.py  # 分析报告
│   │   └── strategy_service.py   # 策略版本
│   │
│   ├── collectors/             # 多平台采集器框架
│   │   ├── base.py             # BaseCollector + Registry
│   │   ├── newsnow_collector.py # NewsNow API（34 平台）
│   │   └── rss_collector.py    # RSS 采集器
│   │
│   ├── ai/                     # AI Provider 层
│   │   ├── base.py             # LLMProvider 抽象基类
│   │   ├── openai_compat_provider.py # OpenAI 兼容（DeepSeek 等）
│   │   ├── mock_provider.py    # 测试用 Mock
│   │   ├── provider_factory.py # Provider 工厂
│   │   ├── prompts/            # 版本化提示词
│   │   │   ├── topic_score_v1.txt
│   │   │   ├── content_draft_v1.txt
│   │   │   └── performance_review_v1.txt
│   │   └── tasks/              # AI 任务
│   │       ├── topic_scorer.py
│   │       └── content_writer.py
│   │
│   ├── platforms/              # 平台适配器
│   │   ├── base.py             # PlatformAdapter 抽象基类
│   │   └── mock_adapter.py     # Mock 适配器（测试用）
│   │
│   ├── tasks/                  # 后台定时任务
│   │   ├── runner.py           # TaskRunner（任务追踪）
│   │   ├── collect_sources.py  # 采集所有来源
│   │   ├── analyze_topics.py   # 评分热点
│   │   ├── publish_due_posts.py # 发布到期帖子
│   │   └── sync_metrics.py     # 同步指标
│   │
│   ├── utils/                  # 工具函数
│   │   ├── errors.py           # 自定义异常
│   │   ├── responses.py        # 统一响应格式
│   │   ├── decorators.py       # auth_required 装饰器
│   │   ├── logging.py          # 日志配置
│   │   ├── time.py             # 时间工具
│   │   └── url.py              # URL 规范化
│   │
│   ├── templates/
│   │   └── index.html          # Web 管理界面
│   └── static/
│       ├── css/style.css       # 样式
│       └── js/app.js           # 前端逻辑
│
├── migrations/                 # Alembic 数据库迁移
├── tests/                      # pytest 测试（98 个）
├── requirements.txt
├── .env.example
├── wsgi.py                     # WSGI 入口
├── worker.py                   # 后台 Worker
├── scheduler.py                # APScheduler 调度器
└── README.md
```

## 核心工作流

```
多平台采集 → 热点入库 → AI 评分 → 生成草稿 → 人工审核 → 调度发布 → 指标采集 → 数据复盘
     ↑                                                                    ↓
     └──────────────────── 策略调整 ←──────────────────────────────────────┘
```

## 安全说明

- 密钥通过环境变量配置，不硬编码在源码中
- 用户密码使用 Werkzeug PBKDF2 哈希存储
- JWT Token 默认 24 小时过期
- 账号 API 不返回凭证引用
- 发布操作有幂等保护
- 外部内容视为不可信输入（AI 提示词中标注）
- Mock Adapter 和 Mock Provider 明确标记，不会冒充真实平台

## License

Private
