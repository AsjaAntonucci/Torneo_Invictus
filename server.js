const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
require('dotenv').config();
const fs = require('fs');

// Initialize express app
const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, 'public')));

// Check if route directories and files exist
const routesDir = path.join(__dirname, 'routes');
if (!fs.existsSync(routesDir)) {
  fs.mkdirSync(routesDir, { recursive: true });
}

// Create basic route handlers if files don't exist
const createDefaultRouteFile = (filename, routeName) => {
  const filePath = path.join(routesDir, filename);
  if (!fs.existsSync(filePath)) {
    const routeContent = `
    const express = require('express');
    const router = express.Router();
    
    router.get('/', (req, res) => {
      res.json({ message: '${routeName} route is working' });
    });
    
    module.exports = router;
    `;
    fs.writeFileSync(filePath, routeContent);
    console.log(`Created default route file: ${filename}`);
  }
};

// Create default route files if they don't exist
createDefaultRouteFile('auth.js', 'Auth');
createDefaultRouteFile('atleti.js', 'Atleti');
createDefaultRouteFile('sfide.js', 'Sfide');
createDefaultRouteFile('specialita.js', 'Specialita');
createDefaultRouteFile('admin.js', 'Admin');

// Import routes
const authRoutes = require('./routes/auth');
const atletiRoutes = require('./routes/atleti');
const sfideRoutes = require('./routes/sfide');
const specialitaRoutes = require('./routes/specialita');
const adminRoutes = require('./routes/admin');

// Use routes
app.use('/api/auth', authRoutes);
app.use('/api/atleti', atletiRoutes);
app.use('/api/sfide', sfideRoutes);
app.use('/api/specialita', specialitaRoutes);
app.use('/api/admin', adminRoutes);

// Create a simple API test endpoint
app.get('/api/test', (req, res) => {
  res.json({ message: 'API is working!' });
});

// Default route for single-page application
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Handle other routes for single-page application
app.get('*', (req, res) => {
  // Only send the index.html for non-API routes
  if (!req.path.startsWith('/api/')) {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
  } else {
    res.status(404).json({ error: 'Route not found' });
  }
});

// Make sure utils directory exists
const utilsDir = path.join(__dirname, 'utils');
if (!fs.existsSync(utilsDir)) {
  fs.mkdirSync(utilsDir, { recursive: true });
}

// Initialize database (only if utils/initDb.js exists)
try {
  const initDbPath = path.join(__dirname, 'utils', 'initDb.js');
  if (fs.existsSync(initDbPath)) {
    const initDb = require('./utils/initDb');
    initDb()
      .then(() => console.log('Database initialized successfully'))
      .catch(err => console.error('Database initialization error:', err));
  } else {
    console.log('Database initialization skipped - utils/initDb.js not found');
  }
} catch (error) {
  console.error('Error initializing database:', error);
}

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});