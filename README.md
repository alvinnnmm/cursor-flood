# X Flood 洪水预测系统

这是一个洪水预测系统的后端服务，提供洪水预测、数据管理和Arduino集成的API。

## 功能特点

- 用户认证和授权
- 基于机器学习的洪水预测
- 历史数据管理
- Arduino传感器数据实时集成
- 洪水警报推送通知
- RESTful API接口

## 安装设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows系统: venv\Scripts\activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建 `.env` 文件并设置以下变量：
```
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/x_flood
JWT_SECRET_KEY=your-secret-key
```

4. 初始化数据库：
```bash
flask db init
flask db migrate
flask db upgrade
```

5. 运行应用：
```bash
flask run
```

## API文档

服务器运行后，API文档将在 `/api/docs` 提供。

## 项目结构

```
x_flood/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── migrations/
├── tests/
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
``` 