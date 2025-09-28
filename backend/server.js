const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

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

// Health check
app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'OK', database: 'connected' });
  } catch (error) {
    res.status(500).json({ status: 'ERROR', database: 'disconnected' });
  }
});

// GET all items - ЭТОГО ЭНДПОИНТА НЕ БЫЛО!
app.get('/api/items', async (req, res) => {
  try {
    console.log('GET /api/items - получение всех продуктов');
    const result = await pool.query('SELECT * FROM fridge_items ORDER BY created_at DESC');
    console.log(`Найдено продуктов: ${result.rows.length}`);
    res.json(result.rows);
  } catch (err) {
    console.error('Ошибка при получении продуктов:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// POST new item
app.post('/api/items', async (req, res) => {
  try {
    const { name, isInFridge } = req.body;
    console.log('POST /api/items - добавление:', name);
    
    if (!name?.trim()) {
      return res.status(400).json({ error: 'Name is required' });
    }
    
    const result = await pool.query(
      'INSERT INTO fridge_items (name, is_in_fridge) VALUES ($1, $2) RETURNING *',
      [name.trim(), isInFridge ?? true]
    );
    
    console.log('Продукт добавлен:', result.rows[0]);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Ошибка при добавлении:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// PATCH toggle item position
app.patch('/api/items/:id/toggle', async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`PATCH /api/items/${id}/toggle - переключение позиции`);
    
    const result = await pool.query(
      'UPDATE fridge_items SET is_in_fridge = NOT is_in_fridge WHERE id = $1 RETURNING *',
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Item not found' });
    }
    
    console.log('Позиция переключена:', result.rows[0]);
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Ошибка при переключении:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

// DELETE item
app.delete('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params;
    console.log(`DELETE /api/items/${id} - удаление продукта`);
    
    const result = await pool.query('DELETE FROM fridge_items WHERE id = $1 RETURNING *', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Item not found' });
    }
    
    console.log('Продукт удален:', result.rows[0]);
    res.json({ message: 'Item deleted', deletedItem: result.rows[0] });
  } catch (err) {
    console.error('Ошибка при удалении:', err);
    res.status(500).json({ error: 'Database error' });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});