const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from React build
// app.use(express.static(path.join(__dirname, '../react_app/dist')));

const pool = new Pool({
  user: 'fridge_user',
  host: 'localhost',
  database: 'fridge_db',
  password: '1234',
  port: 5432,
});

// Create table
const createTable = async () => {
  const query = `
    CREATE TABLE IF NOT EXISTS fridge_items (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      is_in_fridge BOOLEAN DEFAULT true,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;
  
  try {
    await pool.query(query);
    console.log('Table ready');
  } catch (err) {
    console.error('Error creating table:', err);
  }
};

createTable();

// API Routes

app.get('/api/health', async (req, res) => {
    try {
        await pool.query('SELECT 1');
        res.json({ status: 'OK', database: 'connected' });
    } catch (error) {
        res.status(500).json({ status: 'ERROR', database: 'disconnected' });
    }
});

app.get('/api/items', async (req, res) => {
  try {
    console.log('GET /api/items - запрос всех продуктов'); // Логирование
    const result = await pool.query('SELECT * FROM fridge_items ORDER BY created_at DESC');
    console.log(`Найдено продуктов: ${result.rows.length}`); // Логирование количества
    res.json(result.rows);
  } catch (err) {
    console.error('Ошибка при получении продуктов:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.patch('/api/items/:id/toggle', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query(
      'UPDATE fridge_items SET is_in_fridge = NOT is_in_fridge WHERE id = $1 RETURNING *',
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Item not found' });
    }
    
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Database error' });
  }
});

app.delete('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('DELETE FROM fridge_items WHERE id = $1 RETURNING *', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Item not found' });
    }
    
    res.json({ message: 'Item deleted', deletedItem: result.rows[0] });
  } catch (err) {
    res.status(500).json({ error: 'Database error' });
  }
});

// Serve React app for all other routes
// app.get('*', (req, res) => {res.sendFile(path.join(__dirname, '../react_app/dist/index.html'));});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});