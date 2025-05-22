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

// Serve index.html for client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});