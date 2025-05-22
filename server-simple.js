const express = require('express');
const cors = require('cors');
const path = require('path');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
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

// Create database tables if they don't exist
const initDatabase = async () => {
  try {
    // Check if tables exist
    const tableCheckQuery = `
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'atleti'
      );
    `;
    const tableCheck = await pool.query(tableCheckQuery);
    
    if (!tableCheck.rows[0].exists) {
      console.log('Creating database tables...');
      
      // Create Atleti table
      await pool.query(`
        CREATE TABLE atleti (
          id SERIAL PRIMARY KEY,
          nome VARCHAR(100) NOT NULL,
          email VARCHAR(150) UNIQUE NOT NULL,
          password VARCHAR(100) NOT NULL,
          livello INT DEFAULT 1,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
      `);
      
      // Create Admin table
      await pool.query(`
        CREATE TABLE admin (
          id SERIAL PRIMARY KEY,
          username VARCHAR(50) UNIQUE NOT NULL,
          password VARCHAR(100) NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
      `);
      
      // Create Specialita table
      await pool.query(`
        CREATE TABLE specialita (
          id SERIAL PRIMARY KEY,
          nome VARCHAR(50) UNIQUE NOT NULL
        );
      `);
      
      // Create Sfide table
      await pool.query(`
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
      `);
      
      // Create Config table
      await pool.query(`
        CREATE TABLE config_torneo (
          id SERIAL PRIMARY KEY,
          nome_torneo VARCHAR(100) NOT NULL,
          registrazione_aperta BOOLEAN DEFAULT TRUE,
          data_inizio DATE,
          data_fine DATE,
          aggiornato_il TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
      `);
      
      // Insert initial specialties
      await pool.query(`
        INSERT INTO specialita (nome) VALUES
          ('kodachi'),
          ('choken free'),
          ('nito'),
          ('tate-kodachi'),
          ('tate-choken');
      `);
      
      // Insert default admin (username: admin, password: admin123)
      const hashedPassword = await bcrypt.hash('admin123', 10);
      await pool.query(`
        INSERT INTO admin (username, password) VALUES
          ('admin', $1);
      `, [hashedPassword]);
      
      // Insert default tournament config
      await pool.query(`
        INSERT INTO config_torneo (nome_torneo, registrazione_aperta, data_inizio, data_fine) VALUES
          ('Torneo Chanbara 2025', TRUE, '2025-06-01', '2025-06-30');
      `);
      
      console.log('Database tables created successfully');
    } else {
      console.log('Database tables already exist');
    }
  } catch (error) {
    console.error('Database initialization error:', error);
  }
};

// Initialize database
initDatabase();

// JWT Authentication Middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (token == null) return res.status(401).json({ error: 'Unauthorized: No token provided' });
  
  jwt.verify(token, process.env.JWT_SECRET || 'chanbaratournamentsecret2025', (err, user) => {
    if (err) return res.status(403).json({ error: 'Forbidden: Invalid token' });
    req.user = user;
    next();
  });
};

// Check if user is admin middleware
const isAdmin = (req, res, next) => {
  if (!req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden: Admin access required' });
  }
  next();
};

// Simple test route
app.get('/api/test', (req, res) => {
  res.json({ message: 'API is working!' });
});

// AUTH ROUTES

// Register new athlete
app.post('/api/auth/register', async (req, res) => {
  try {
    // Check if registration is open
    const configQuery = 'SELECT registrazione_aperta FROM config_torneo LIMIT 1';
    const configResult = await pool.query(configQuery);
    
    if (!configResult.rows[0].registrazione_aperta) {
      return res.status(403).json({ error: 'Le registrazioni sono chiuse' });
    }
    
    const { nome, email, password } = req.body;
    
    // Validate input
    if (!nome || !email || !password) {
      return res.status(400).json({ error: 'Tutti i campi sono obbligatori' });
    }
    
    // Check if email already exists
    const checkQuery = 'SELECT * FROM atleti WHERE email = $1';
    const checkResult = await pool.query(checkQuery, [email]);
    
    if (checkResult.rows.length > 0) {
      return res.status(400).json({ error: 'Email già registrata' });
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Insert new athlete
    const insertQuery = `
      INSERT INTO atleti (nome, email, password, livello)
      VALUES ($1, $2, $3, 1)
      RETURNING id, nome, email, livello
    `;
    
    const result = await pool.query(insertQuery, [nome, email, hashedPassword]);
    const newAtleta = result.rows[0];
    
    // Generate token
    const token = jwt.sign(
      { id: newAtleta.id, email: newAtleta.email, isAdmin: false },
      process.env.JWT_SECRET || 'chanbaratournamentsecret2025',
      { expiresIn: '24h' }
    );
    
    // Return user info and token
    res.status(201).json({
      message: 'Registrazione completata con successo',
      user: {
        id: newAtleta.id,
        nome: newAtleta.nome,
        email: newAtleta.email,
        livello: newAtleta.livello
      },
      token
    });
    
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Login athlete
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Validate input
    if (!email || !password) {
      return res.status(400).json({ error: 'Email e password sono obbligatori' });
    }
    
    // Find athlete
    const query = 'SELECT * FROM atleti WHERE email = $1';
    const result = await pool.query(query, [email]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Credenziali non valide' });
    }
    
    const atleta = result.rows[0];
    
    // Verify password
    const isValid = await bcrypt.compare(password, atleta.password);
    
    if (!isValid) {
      return res.status(401).json({ error: 'Credenziali non valide' });
    }
    
    // Generate token
    const token = jwt.sign(
      { id: atleta.id, email: atleta.email, isAdmin: false },
      process.env.JWT_SECRET || 'chanbaratournamentsecret2025',
      { expiresIn: '24h' }
    );
    
    // Return user info and token
    res.json({
      user: {
        id: atleta.id,
        nome: atleta.nome,
        email: atleta.email,
        livello: atleta.livello
      },
      token
    });
    
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Login admin
app.post('/api/auth/admin/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Validate input
    if (!username || !password) {
      return res.status(400).json({ error: 'Username e password sono obbligatori' });
    }
    
    // Find admin
    const query = 'SELECT * FROM admin WHERE username = $1';
    const result = await pool.query(query, [username]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Credenziali non valide' });
    }
    
    const admin = result.rows[0];
    
    // Verify password
    const isValid = await bcrypt.compare(password, admin.password);
    
    if (!isValid) {
      return res.status(401).json({ error: 'Credenziali non valide' });
    }
    
    // Generate token
    const token = jwt.sign(
      { id: admin.id, username: admin.username, isAdmin: true },
      process.env.JWT_SECRET || 'chanbaratournamentsecret2025',
      { expiresIn: '24h' }
    );
    
    // Return admin info and token
    res.json({
      user: {
        id: admin.id,
        username: admin.username,
        isAdmin: true
      },
      token
    });
    
  } catch (error) {
    console.error('Admin login error:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// ATHLETE ROUTES

// Get all athletes
app.get('/api/atleti', authenticateToken, async (req, res) => {
  try {
    const query = 'SELECT id, nome, email, livello FROM atleti ORDER BY livello DESC, nome ASC';
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching athletes:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Get athlete profile
app.get('/api/atleti/me/profile', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.id;
    
    // Get athlete details
    const athleteQuery = 'SELECT id, nome, email, livello FROM atleti WHERE id = $1';
    const athleteResult = await pool.query(athleteQuery, [userId]);
    
    if (athleteResult.rows.length === 0) {
      return res.status(404).json({ error: 'Atleta non trovato' });
    }
    
    const athlete = athleteResult.rows[0];
    
    // Get upcoming challenges
    const challengesQuery = `
      SELECT 
        s.id, 
        s.data_sfida, 
        sp.nome as specialita,
        a1.nome as sfidante_nome,
        a2.nome as sfidato_nome,
        s.vincitore_id
      FROM sfide s
      JOIN specialita sp ON s.specialita_id = sp.id
      JOIN atleti a1 ON s.atleta1_id = a1.id
      JOIN atleti a2 ON s.atleta2_id = a2.id
      WHERE (s.atleta1_id = $1 OR s.atleta2_id = $1)
        AND s.data_sfida >= CURRENT_DATE
      ORDER BY s.data_sfida ASC
    `;
    
    const challengesResult = await pool.query(challengesQuery, [userId]);
    
    // Get past challenges
    const pastChallengesQuery = `
      SELECT 
        s.id, 
        s.data_sfida, 
        sp.nome as specialita,
        a1.nome as sfidante_nome,
        a2.nome as sfidato_nome,
        CASE 
          WHEN s.vincitore_id IS NOT NULL THEN
            (SELECT nome FROM atleti WHERE id = s.vincitore_id)
          ELSE NULL
        END as vincitore_nome
      FROM sfide s
      JOIN specialita sp ON s.specialita_id = sp.id
      JOIN atleti a1 ON s.atleta1_id = a1.id
      JOIN atleti a2 ON s.atleta2_id = a2.id
      WHERE (s.atleta1_id = $1 OR s.atleta2_id = $1)
        AND s.data_sfida < CURRENT_DATE
      ORDER BY s.data_sfida DESC
      LIMIT 10
    `;
    
    const pastChallengesResult = await pool.query(pastChallengesQuery, [userId]);
    
    res.json({
      profile: athlete,
      upcomingChallenges: challengesResult.rows,
      pastChallenges: pastChallengesResult.rows
    });
    
  } catch (error) {
    console.error('Error fetching profile:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Get possible opponents
app.get('/api/atleti/challenge/possible-opponents', authenticateToken, async (req, res) => {
  try {
    const userId = req.user.id;
    
    // Get current user's level
    const levelQuery = 'SELECT livello FROM atleti WHERE id = $1';
    const levelResult = await pool.query(levelQuery, [userId]);
    
    if (levelResult.rows.length === 0) {
      return res.status(404).json({ error: 'Atleta non trovato' });
    }
    
    const userLevel = levelResult.rows[0].livello;
    
    // Get athletes with similar or higher level
    const opponentsQuery = `
      SELECT id, nome, livello
      FROM atleti
      WHERE id != $1
        AND livello >= $2
      ORDER BY livello ASC, nome ASC
    `;
    
    const opponentsResult = await pool.query(opponentsQuery, [userId, userLevel]);
    
    res.json(opponentsResult.rows);
    
  } catch (error) {
    console.error('Error fetching possible opponents:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// CHALLENGE ROUTES

// Get all challenges
app.get('/api/sfide', authenticateToken, async (req, res) => {
  try {
    const { date } = req.query;
    let dateFilter = '';
    let params = [];
    
    if (date) {
      dateFilter = 'WHERE s.data_sfida = $1';
      params.push(date);
    } else {
      dateFilter = 'WHERE s.data_sfida >= CURRENT_DATE';
    }
    
    const query = `
      SELECT 
        s.id, 
        s.data_sfida, 
        s.atleta1_id, 
        s.atleta2_id,
        a1.nome as sfidante_nome,
        a2.nome as sfidato_nome,
        s.specialita_id,
        sp.nome as specialita,
        s.vincitore_id,
        CASE 
          WHEN s.vincitore_id IS NOT NULL THEN
            (SELECT nome FROM atleti WHERE id = s.vincitore_id)
          ELSE NULL
        END as vincitore_nome
      FROM sfide s
      JOIN atleti a1 ON s.atleta1_id = a1.id
      JOIN atleti a2 ON s.atleta2_id = a2.id
      JOIN specialita sp ON s.specialita_id = sp.id
      ${dateFilter}
      ORDER BY s.data_sfida ASC
    `;
    
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching challenges:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Create a new challenge
app.post('/api/sfide', authenticateToken, async (req, res) => {
  try {
    const { atleta2_id, data_sfida, specialita_id } = req.body;
    const atleta1_id = req.user.id; // The challenger is the logged-in user
    
    // Check if registration is closed (challenges should only be allowed when registration is closed)
    const configQuery = 'SELECT registrazione_aperta FROM config_torneo LIMIT 1';
    const configResult = await pool.query(configQuery);
    
    if (configResult.rows[0].registrazione_aperta) {
      return res.status(403).json({ 
        error: 'Le sfide possono essere create solo dopo la chiusura delle registrazioni' 
      });
    }
    
    // Validate required fields
    if (!atleta2_id || !data_sfida || !specialita_id) {
      return res.status(400).json({ 
        error: 'Tutti i campi (atleta2_id, data_sfida, specialita_id) sono obbligatori' 
      });
    }
    
    // Parse date to make sure it's valid
    const sfidaDate = new Date(data_sfida);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    // Check if date is in the future
    if (sfidaDate <= today) {
      return res.status(400).json({ 
        error: 'La data della sfida deve essere futura' 
      });
    }
    
    // Check if atleta2_id exists
    const atletaQuery = 'SELECT livello FROM atleti WHERE id = $1';
    const atleta1Result = await pool.query(atletaQuery, [atleta1_id]);
    const atleta2Result = await pool.query(atletaQuery, [atleta2_id]);
    
    if (atleta2Result.rows.length === 0) {
      return res.status(404).json({ error: 'Atleta sfidato non trovato' });
    }
    
    // Check if atleta2 is of equal or higher level
    const atleta1Level = atleta1Result.rows[0].livello;
    const atleta2Level = atleta2Result.rows[0].livello;
    
    if (atleta2Level < atleta1Level) {
      return res.status(400).json({ 
        error: 'Puoi sfidare solo atleti di livello pari o superiore' 
      });
    }
    
    // Check if specialita exists
    const specialitaQuery = 'SELECT id FROM specialita WHERE id = $1';
    const specialitaResult = await pool.query(specialitaQuery, [specialita_id]);
    
    if (specialitaResult.rows.length === 0) {
      return res.status(404).json({ error: 'Specialità non trovata' });
    }
    
    // Check if there's already a challenge between these athletes on this date
    const checkExistingQuery = `
      SELECT id FROM sfide
      WHERE ((atleta1_id = $1 AND atleta2_id = $2) OR (atleta1_id = $2 AND atleta2_id = $1))
        AND data_sfida = $3
    `;
    const existingResult = await pool.query(checkExistingQuery, [atleta1_id, atleta2_id, data_sfida]);
    
    if (existingResult.rows.length > 0) {
      return res.status(400).json({ 
        error: 'Esiste già una sfida tra questi atleti per questa data' 
      });
    }
    
    // Create new challenge
    const insertQuery = `
      INSERT INTO sfide (atleta1_id, atleta2_id, data_sfida, specialita_id)
      VALUES ($1, $2, $3, $4)
      RETURNING id
    `;
    
    const result = await pool.query(insertQuery, [atleta1_id, atleta2_id, data_sfida, specialita_id]);
    
    // Get the complete challenge data
    const challengeQuery = `
      SELECT 
        s.id, 
        s.data_sfida, 
        s.atleta1_id, 
        s.atleta2_id,
        a1.nome as sfidante_nome,
        a2.nome as sfidato_nome,
        s.specialita_id,
        sp.nome as specialita
      FROM sfide s
      JOIN atleti a1 ON s.atleta1_id = a1.id
      JOIN atleti a2 ON s.atleta2_id = a2.id
      JOIN specialita sp ON s.specialita_id = sp.id
      WHERE s.id = $1
    `;
    
    const challengeResult = await pool.query(challengeQuery, [result.rows[0].id]);
    
    res.status(201).json({
      message: 'Sfida creata con successo',
      challenge: challengeResult.rows[0]
    });
    
  } catch (error) {
    console.error('Error creating challenge:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Record challenge result (admin only)
app.post('/api/sfide/:id/risultato', authenticateToken, async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ error: 'Accesso riservato agli amministratori' });
    }
    
    const { id } = req.params;
    const { vincitore_id } = req.body;
    
    // Validate input
    if (!vincitore_id) {
      return res.status(400).json({ error: 'vincitore_id è obbligatorio' });
    }
    
    // Check if challenge exists
    const checkQuery = `
      SELECT atleta1_id, atleta2_id, vincitore_id, data_sfida
      FROM sfide
      WHERE id = $1
    `;
    
    const checkResult = await pool.query(checkQuery, [id]);
    
    if (checkResult.rows.length === 0) {
      return res.status(404).json({ error: 'Sfida non trovata' });
    }
    
    const challenge = checkResult.rows[0];
    
    // Check if result is already recorded
    if (challenge.vincitore_id) {
      return res.status(400).json({ error: 'Il risultato è già stato registrato' });
    }
    
    // Check if vincitore_id is one of the athletes
    if (vincitore_id != challenge.atleta1_id && vincitore_id != challenge.atleta2_id) {
      return res.status(400).json({ 
        error: 'Il vincitore deve essere uno degli atleti partecipanti alla sfida' 
      });
    }
    
    // Check if the challenge date is today or in the past
    const challengeDate = new Date(challenge.data_sfida);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (challengeDate > today) {
      return res.status(400).json({ 
        error: 'Non è possibile registrare il risultato di una sfida futura' 
      });
    }
    
    // Begin transaction
    await pool.query('BEGIN');
    
    // Update challenge with winner
    const updateQuery = `
      UPDATE sfide
      SET vincitore_id = $1, modificato_il = CURRENT_TIMESTAMP
      WHERE id = $2
      RETURNING *
    `;
    
    await pool.query(updateQuery, [vincitore_id, id]);
    
    // Increase winner's level
    const updateLevelQuery = `
      UPDATE atleti
      SET livello = livello + 1
      WHERE id = $1
      RETURNING id, nome, livello
    `;
    
    const levelResult = await pool.query(updateLevelQuery, [vincitore_id]);
    
    // Commit transaction
    await pool.query('COMMIT');
    
    res.json({
      message: 'Risultato registrato con successo',
      winner: levelResult.rows[0]
    });
    
  } catch (error) {
    // Rollback in case of error
    await pool.query('ROLLBACK');
    console.error('Error recording challenge result:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Get challenge details
app.get('/api/sfide/:id', authenticateToken, async (req, res) => {
  try {
    const { id } = req.params;
    
    const query = `
      SELECT 
        s.id, 
        s.data_sfida, 
        s.atleta1_id, 
        s.atleta2_id,
        a1.nome as sfidante_nome,
        a2.nome as sfidato_nome,
        s.specialita_id,
        sp.nome as specialita,
        s.vincitore_id,
        CASE 
          WHEN s.vincitore_id IS NOT NULL THEN
            (SELECT nome FROM atleti WHERE id = s.vincitore_id)
          ELSE NULL
        END as vincitore_nome
      FROM sfide s
      JOIN atleti a1 ON s.atleta1_id = a1.id
      JOIN atleti a2 ON s.atleta2_id = a2.id
      JOIN specialita sp ON s.specialita_id = sp.id
      WHERE s.id = $1
    `;
    
    const result = await pool.query(query, [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Sfida non trovata' });
    }
    
    res.json(result.rows[0]);
    
  } catch (error) {
    console.error('Error fetching challenge details:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// SPECIALTIES ROUTES

// Get all specialties
app.get('/api/specialita', authenticateToken, async (req, res) => {
  try {
    const query = 'SELECT id, nome FROM specialita ORDER BY nome ASC';
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching specialties:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// ADMIN ROUTES

// Get tournament configuration
app.get('/api/admin/config', async (req, res) => {
  try {
    const query = 'SELECT * FROM config_torneo LIMIT 1';
    const result = await pool.query(query);
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error fetching tournament config:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Update tournament configuration (admin only)
app.patch('/api/admin/config', authenticateToken, async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ error: 'Accesso riservato agli amministratori' });
    }
    
    const { nome_torneo, data_inizio, data_fine } = req.body;
    
    const updateQuery = `
      UPDATE config_torneo 
      SET nome_torneo = COALESCE($1, nome_torneo),
          data_inizio = COALESCE($2, data_inizio),
          data_fine = COALESCE($3, data_fine),
          aggiornato_il = CURRENT_TIMESTAMP
      RETURNING *
    `;
    
    const result = await pool.query(updateQuery, [nome_torneo, data_inizio, data_fine]);
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error updating tournament config:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Close registration (admin only)
app.patch('/api/admin/chiudi-registrazione', authenticateToken, async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ error: 'Accesso riservato agli amministratori' });
    }
    
    // Begin transaction
    await pool.query('BEGIN');
    
    // Update config_torneo to close registration
    const updateConfigQuery = `
      UPDATE config_torneo 
      SET registrazione_aperta = FALSE,
          aggiornato_il = CURRENT_TIMESTAMP
      RETURNING *
    `;
    
    const configResult = await pool.query(updateConfigQuery);
    
    // Commit transaction
    await pool.query('COMMIT');
    
    res.json({
      message: 'Registrazione chiusa con successo',
      config: configResult.rows[0]
    });
    
  } catch (error) {
    // Rollback in case of error
    await pool.query('ROLLBACK');
    console.error('Error closing registration:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Bulk create athletes (admin only)
app.post('/api/admin/atleti', authenticateToken, async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ error: 'Accesso riservato agli amministratori' });
    }
    
    const atleti = req.body;
    
    // Check if registration is open
    const configQuery = 'SELECT registrazione_aperta FROM config_torneo LIMIT 1';
    const configResult = await pool.query(configQuery);
    
    if (!configResult.rows[0].registrazione_aperta) {
      return res.status(403).json({ error: 'Le registrazioni sono chiuse' });
    }
    
    // Validate input
    if (!Array.isArray(atleti) || atleti.length === 0) {
      return res.status(400).json({ error: 'Expected an array of athletes' });
    }
    
    // Begin transaction
    await pool.query('BEGIN');
    
    const createdAtleti = [];
    
    // Process each athlete
    for (const atleta of atleti) {
      const { nome, email, password } = atleta;
      
      // Validate required fields
      if (!nome || !email || !password) {
        await pool.query('ROLLBACK');
        return res.status(400).json({ 
          error: 'Tutti i campi (nome, email, password) sono obbligatori per ogni atleta' 
        });
      }
      
      // Check if email already exists
      const checkQuery = 'SELECT id FROM atleti WHERE email = $1';
      const checkResult = await pool.query(checkQuery, [email]);
      
      if (checkResult.rows.length > 0) {
        // Skip existing athletes
        continue;
      }
      
      // Hash password
      const hashedPassword = await bcrypt.hash(password, 10);
      
      // Insert athlete
      const insertQuery = `
        INSERT INTO atleti (nome, email, password, livello)
        VALUES ($1, $2, $3, 1)
        RETURNING id, nome, email, livello
      `;
      
      const result = await pool.query(insertQuery, [nome, email, hashedPassword]);
      createdAtleti.push(result.rows[0]);
    }
    
    // Commit transaction
    await pool.query('COMMIT');
    
    res.status(201).json({
      message: `${createdAtleti.length} atleti creati con successo`,
      atleti: createdAtleti
    });
    
  } catch (error) {
    // Rollback in case of error
    await pool.query('ROLLBACK');
    console.error('Error creating athletes:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Get rankings
app.get('/api/admin/classifica', async (req, res) => {
  try {
    const query = `
      SELECT 
        a.id, 
        a.nome, 
        a.livello,
        COUNT(CASE WHEN s.vincitore_id = a.id THEN 1 END) as vittorie,
        COUNT(CASE WHEN (s.atleta1_id = a.id OR s.atleta2_id = a.id) AND s.vincitore_id IS NOT NULL THEN 1 END) as sfide_totali
      FROM atleti a
      LEFT JOIN sfide s ON (s.atleta1_id = a.id OR s.atleta2_id = a.id)
      GROUP BY a.id, a.nome, a.livello
      ORDER BY a.livello DESC, vittorie DESC, a.nome ASC
    `;
    
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching rankings:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Get dashboard statistics (admin only)
app.get('/api/admin/statistiche', authenticateToken, async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ error: 'Accesso riservato agli amministratori' });
    }
    
    // Get total athletes
    const atletiQuery = 'SELECT COUNT(*) as total FROM atleti';
    const atletiResult = await pool.query(atletiQuery);
    
    // Get total challenges
    const sfideQuery = 'SELECT COUNT(*) as total FROM sfide';
    const sfideResult = await pool.query(sfideQuery);
    
    // Get completed challenges
    const sfideCompletateQuery = 'SELECT COUNT(*) as total FROM sfide WHERE vincitore_id IS NOT NULL';
    const sfideCompletateResult = await pool.query(sfideCompletateQuery);
    
    // Get upcoming challenges
    const sfideFutureQuery = 'SELECT COUNT(*) as total FROM sfide WHERE data_sfida > CURRENT_DATE';
    const sfideFutureResult = await pool.query(sfideFutureQuery);
    
    // Get today's challenges
    const sfideOggiQuery = 'SELECT COUNT(*) as total FROM sfide WHERE data_sfida = CURRENT_DATE';
    const sfideOggiResult = await pool.query(sfideOggiQuery);
    
    // Get registration status
    const configQuery = 'SELECT registrazione_aperta FROM config_torneo LIMIT 1';
    const configResult = await pool.query(configQuery);
    
    res.json({
      totale_atleti: parseInt(atletiResult.rows[0].total),
      totale_sfide: parseInt(sfideResult.rows[0].total),
      sfide_completate: parseInt(sfideCompletateResult.rows[0].total),
      sfide_future: parseInt(sfideFutureResult.rows[0].total),
      sfide_oggi: parseInt(sfideOggiResult.rows[0].total),
      registrazione_aperta: configResult.rows[0].registrazione_aperta
    });
    
  } catch (error) {
    console.error('Error fetching statistics:', error);
    res.status(500).json({ error: 'Errore del server' });
  }
});

// Default route for single-page application
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Handle all other routes
app.get('*', (req, res) => {
  // Only send index.html for browser requests (not API)
  if (!req.path.startsWith('/api/')) {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
  } else {
    res.status(404).json({ error: 'Route not found' });
  }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});