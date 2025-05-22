const { Pool } = require('pg');
require('dotenv').config();

// Create a new PostgreSQL pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: false
});

// Check connection
pool.connect()
  .then(() => console.log('Database connected successfully'))
  .catch(err => console.error('Database connection error:', err.message));

module.exports = {
  query: (text, params) => pool.query(text, params)
};