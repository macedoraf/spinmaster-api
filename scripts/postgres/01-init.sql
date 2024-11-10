-- Criar banco de dados se não existir
SELECT 'CREATE DATABASE spinmaster'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'spinmaster')\gexec

-- Conectar ao banco spinmaster
\c spinmaster;

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";