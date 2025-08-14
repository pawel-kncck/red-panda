# PostgreSQL Setup for Red Panda

## ⚠️ PostgreSQL is Required

The Red Panda application requires PostgreSQL to be running on port 5432. 

## 🚀 Quick Start Options

### Option 1: Using Docker (Recommended)
```bash
docker run --name redpanda-postgres -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=redpanda_db_2024 \
  -e POSTGRES_DB=redpanda \
  -d postgres:17
```

### Option 2: Using Docker Compose
```bash
# From the project root directory
docker-compose up -d db
```

### Option 3: System PostgreSQL
- **macOS**: `brew services start postgresql`
- **Ubuntu/Debian**: `sudo systemctl start postgresql`
- **Windows**: Start PostgreSQL from Services panel

### Option 4: PostgreSQL.app (macOS only)
Download from [https://postgresapp.com/](https://postgresapp.com/)

## 📝 Database Configuration

Your `.env` file is already configured with:
```env
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=redpanda_db_2024
POSTGRES_DB=redpanda
```

## ✅ Verify Setup

Run the verification script:
```bash
python start_postgres_local.py
```

## 🔄 Run Migrations

Once PostgreSQL is running:
```bash
cd backend
# Create initial migration
~/.local/bin/alembic revision --autogenerate -m "Initial migration"
# Apply migrations
~/.local/bin/alembic upgrade head
```

## 🎯 Next Steps

1. Start PostgreSQL using one of the options above
2. Verify connection with `python start_postgres_local.py`
3. Run migrations
4. Start the backend: `cd backend && fastapi dev app/main.py`
5. Start the frontend: `cd frontend && npm run dev`

## 🐳 No Docker Available?

If Docker is not available in your environment, you'll need to:

1. **Install PostgreSQL locally** or
2. **Use a cloud PostgreSQL service** (update `.env` with connection details) or
3. **Use a PostgreSQL container service** that's accessible from your environment

For local installation:
- **macOS**: `brew install postgresql`
- **Ubuntu/Debian**: `sudo apt-get install postgresql postgresql-contrib`
- **Windows**: Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)

After installation, create the database and user:
```sql
sudo -u postgres psql
CREATE USER postgres WITH PASSWORD 'redpanda_db_2024';
CREATE DATABASE redpanda OWNER postgres;
\q
```