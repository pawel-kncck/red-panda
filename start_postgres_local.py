#!/usr/bin/env python3
"""
Local PostgreSQL startup script for development without Docker.
This script will attempt to start PostgreSQL using various methods.
"""

import os
import sys
import subprocess
import time
import psycopg2
from pathlib import Path

# Configuration from .env
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "redpanda_db_2024"
POSTGRES_DB = "redpanda"
POSTGRES_PORT = 5432

def check_postgres_connection():
    """Check if we can connect to PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database="postgres"  # Connect to default database first
        )
        conn.close()
        print(f"✅ PostgreSQL is running on port {POSTGRES_PORT}")
        return True
    except Exception as e:
        return False

def create_database():
    """Create the redpanda database if it doesn't exist."""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host="localhost",
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")
            print(f"✅ Created database '{POSTGRES_DB}'")
        else:
            print(f"✅ Database '{POSTGRES_DB}' already exists")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def main():
    print("🐼 Red Panda PostgreSQL Setup")
    print("=" * 40)
    
    # Check if PostgreSQL is already running
    if check_postgres_connection():
        print("PostgreSQL is already running!")
        if create_database():
            print("\n✅ PostgreSQL is ready for Red Panda!")
            print(f"   Host: localhost")
            print(f"   Port: {POSTGRES_PORT}")
            print(f"   Database: {POSTGRES_DB}")
            print(f"   User: {POSTGRES_USER}")
            print(f"   Password: {POSTGRES_PASSWORD}")
        return 0
    
    print("\n❌ PostgreSQL is not running on port 5432")
    print("\nTo start PostgreSQL, you have several options:")
    print("\n1. Using Docker (recommended):")
    print("   docker run --name redpanda-postgres -p 5432:5432 \\")
    print(f"     -e POSTGRES_USER={POSTGRES_USER} \\")
    print(f"     -e POSTGRES_PASSWORD={POSTGRES_PASSWORD} \\")
    print(f"     -e POSTGRES_DB={POSTGRES_DB} \\")
    print("     -d postgres:17")
    
    print("\n2. Using Docker Compose (from project root):")
    print("   docker-compose up -d db")
    
    print("\n3. Using system PostgreSQL (if installed):")
    print("   - On macOS: brew services start postgresql")
    print("   - On Ubuntu: sudo systemctl start postgresql")
    print("   - On Windows: Start PostgreSQL service from Services panel")
    
    print("\n4. Using PostgreSQL.app (macOS):")
    print("   Download from https://postgresapp.com/")
    
    print("\nAfter starting PostgreSQL, run this script again to verify the connection.")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())