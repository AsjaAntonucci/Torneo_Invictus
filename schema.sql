-- Database schema for Chanbara Tournament Management System

-- Tabella Atleti (Athletes Table)
CREATE TABLE atleti (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL,
  livello INT DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabella Admin
CREATE TABLE admin (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabella Specialità (Specialties Table)
CREATE TABLE specialita (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(50) UNIQUE NOT NULL
);

-- Tabella Sfide (Challenges Table)
CREATE TABLE sfide (
  id SERIAL PRIMARY KEY,
  atleta1_id INT REFERENCES atleti(id),
  atleta2_id INT REFERENCES atleti(id),
  data_sfida DATE NOT NULL,
  specialita_id INT REFERENCES specialita(id),
  vincitore_id INT REFERENCES atleti(id) DEFAULT NULL,
  creato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modificato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (atleta1_id <> atleta2_id)
);

-- Tabella Configurazione Torneo (Tournament Configuration)
CREATE TABLE config_torneo (
  id SERIAL PRIMARY KEY,
  nome_torneo VARCHAR(100) NOT NULL,
  registrazione_aperta BOOLEAN DEFAULT TRUE,
  data_inizio DATE,
  data_fine DATE,
  aggiornato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial specialties
INSERT INTO specialita (nome) VALUES
  ('kodachi'),
  ('choken free'),
  ('nito'),
  ('tate-kodachi'),
  ('tate-choken');

-- Insert default admin user (username: admin, password: admin123) - Change in production!
INSERT INTO admin (username, password) VALUES
  ('admin', '$2b$10$rdjqM7YCwIr1jjPuYwLa5Okt9oVKZWO5XfAT95hcVSg2gGzHCLI56');

-- Insert default tournament configuration
INSERT INTO config_torneo (nome_torneo, registrazione_aperta, data_inizio, data_fine) VALUES
  ('Torneo Chanbara 2025', TRUE, '2025-06-01', '2025-06-30');