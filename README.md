## Установка

### 1.

```bash
git clone https://github.com/kirillysz/todolist_back.git
cd todolist_back
```

### 2.
Создайте `.env` файл с содержимым:

```
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=mydb

ORIGINS=http://localhost:5173

SECRET_KEY=your_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3.
Запустите бекенд:

```bash
docker compose up --build -d
```

