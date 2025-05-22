const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();

// Basic middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Simple API endpoint
app.get('/api/hello', (req, res) => {
  res.json({ message: 'Hello from Chanbara Tournament API!' });
});

// Tournament info endpoint with sample data
app.get('/api/tournament', (req, res) => {
  res.json({
    nome_torneo: 'Torneo Chanbara 2025',
    registrazione_aperta: true,
    data_inizio: '2025-06-01',
    data_fine: '2025-06-30'
  });
});

// Sample rankings endpoint
app.get('/api/rankings', (req, res) => {
  res.json([
    { id: 1, nome: 'Mario Rossi', livello: 3, vittorie: 5, sfide_totali: 7 },
    { id: 2, nome: 'Luigi Verdi', livello: 2, vittorie: 3, sfide_totali: 5 },
    { id: 3, nome: 'Anna Bianchi', livello: 2, vittorie: 2, sfide_totali: 4 },
    { id: 4, nome: 'Sara Neri', livello: 1, vittorie: 1, sfide_totali: 3 }
  ]);
});

// Sample specialties endpoint
app.get('/api/specialties', (req, res) => {
  res.json([
    { id: 1, nome: 'kodachi' },
    { id: 2, nome: 'choken free' },
    { id: 3, nome: 'nito' },
    { id: 4, nome: 'tate-kodachi' },
    { id: 5, nome: 'tate-choken' }
  ]);
});

// Sample challenges endpoint
app.get('/api/challenges', (req, res) => {
  res.json([
    {
      id: 1,
      data_sfida: '2025-06-05',
      sfidante_nome: 'Mario Rossi',
      sfidato_nome: 'Luigi Verdi',
      specialita: 'kodachi',
      vincitore_nome: null
    },
    {
      id: 2,
      data_sfida: '2025-06-07',
      sfidante_nome: 'Anna Bianchi',
      sfidato_nome: 'Sara Neri',
      specialita: 'nito',
      vincitore_nome: null
    },
    {
      id: 3,
      data_sfida: '2025-06-10',
      sfidante_nome: 'Luigi Verdi',
      sfidato_nome: 'Sara Neri',
      specialita: 'choken free',
      vincitore_nome: null
    }
  ]);
});

// Basic authentication endpoint (simplified)
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  
  // Simple validation
  if (!email || !password) {
    return res.status(400).json({ error: 'Email e password sono obbligatori' });
  }
  
  // For demo purposes, accept any login with these test credentials
  if (email === 'atleta@example.com' && password === 'password123') {
    return res.json({
      user: {
        id: 1,
        nome: 'Mario Rossi',
        email: 'atleta@example.com',
        livello: 3
      },
      token: 'sample-token-for-demo'
    });
  }
  
  // Admin login
  if (email === 'admin@example.com' && password === 'admin123') {
    return res.json({
      user: {
        id: 999,
        username: 'admin',
        isAdmin: true
      },
      token: 'sample-admin-token-for-demo'
    });
  }
  
  return res.status(401).json({ error: 'Credenziali non valide' });
});

// Simplified registration endpoint
app.post('/api/auth/register', (req, res) => {
  const { nome, email, password } = req.body;
  
  // Simple validation
  if (!nome || !email || !password) {
    return res.status(400).json({ error: 'Tutti i campi sono obbligatori' });
  }
  
  // For demo purposes, accept any registration
  res.status(201).json({
    message: 'Registrazione completata con successo',
    user: {
      id: Math.floor(Math.random() * 1000) + 10,
      nome,
      email,
      livello: 1
    },
    token: 'sample-token-for-demo'
  });
});

// Serve index.html for client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server on port 3000 to avoid conflict with Streamlit
const PORT = 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});