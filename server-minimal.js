const express = require('express');
const cors = require('cors');
const path = require('path');
const { Pool } = require('pg');
require('dotenv').config();

// Initialize express app
const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// PostgreSQL database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: false
});

// Database check
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('Database connection successful. Current timestamp:', res.rows[0].now);
  }
});

// Simple API routes
app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Chanbara Tournament API!' });
});

// Tournament info
app.get('/api/tournament', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'config_torneo'
      );
    `);
    
    if (result.rows[0].exists) {
      const tournamentResult = await pool.query('SELECT * FROM config_torneo LIMIT 1');
      res.json(tournamentResult.rows[0] || { nome_torneo: 'Torneo Chanbara 2025', registrazione_aperta: true });
    } else {
      res.json({ nome_torneo: 'Torneo Chanbara 2025', registrazione_aperta: true });
    }
  } catch (error) {
    console.error('Error fetching tournament info:', error);
    res.status(500).json({ error: 'Database error' });
  }
});

// Get rankings
app.get('/api/rankings', async (req, res) => {
  try {
    // Check if tables exist
    const tablesExistResult = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'atleti'
      );
    `);
    
    if (tablesExistResult.rows[0].exists) {
      // We have tables, return real data
      const rankings = await pool.query(`
        SELECT id, nome, livello FROM atleti ORDER BY livello DESC, nome ASC
      `);
      res.json(rankings.rows);
    } else {
      // No tables yet, return sample data
      res.json([
        { id: 1, nome: 'Mario Rossi', livello: 3 },
        { id: 2, nome: 'Luigi Verdi', livello: 2 },
        { id: 3, nome: 'Anna Bianchi', livello: 2 },
        { id: 4, nome: 'Sara Neri', livello: 1 }
      ]);
    }
  } catch (error) {
    console.error('Error fetching rankings:', error);
    res.status(500).json({ error: 'Database error' });
  }
});

// Get specialties
app.get('/api/specialties', async (req, res) => {
  try {
    // Check if tables exist
    const tablesExistResult = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'specialita'
      );
    `);
    
    if (tablesExistResult.rows[0].exists) {
      // We have tables, return real data
      const specialties = await pool.query(`
        SELECT id, nome FROM specialita ORDER BY nome ASC
      `);
      res.json(specialties.rows);
    } else {
      // No tables yet, return sample data
      res.json([
        { id: 1, nome: 'kodachi' },
        { id: 2, nome: 'choken free' },
        { id: 3, nome: 'nito' },
        { id: 4, nome: 'tate-kodachi' },
        { id: 5, nome: 'tate-choken' }
      ]);
    }
  } catch (error) {
    console.error('Error fetching specialties:', error);
    res.status(500).json({ error: 'Database error' });
  }
});

// Serve index.html for all other routes (SPA support)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});