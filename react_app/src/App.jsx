import React, { useState, useEffect } from 'react';
import './App.css';

const Fridge = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [items, setItems] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Загрузка данных с сервера
  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/items');
      
      if (!response.ok) {
        throw new Error(`Ошибка загрузки: ${response.status}`);
      }
      
      const data = await response.json();
      setItems(data);
      setError('');
    } catch (err) {
      console.error('Error fetching items:', err);
      setError('Ошибка загрузки данных. Проверьте подключение к серверу.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const toggleDoor = () => {
    setIsOpen(!isOpen);
  };

  const addItem = async () => {
    const itemName = newItemName.trim();
    if (itemName === '') {
      setError('Введите название продукта');
      return;
    }
    
    try {
      const response = await fetch('/api/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: itemName,
          isInFridge: true,
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Ошибка при добавлении');
      }
      
      const newItem = await response.json();
      setItems([newItem, ...items]);
      setNewItemName('');
      setError('');
    } catch (err) {
      console.error('Error adding item:', err);
      setError(err.message || 'Ошибка добавления продукта');
    }
  };

  const removeItem = async (id) => {
    if (!window.confirm('Удалить этот продукт?')) return;
    
    try {
      const response = await fetch(`/api/items/${id}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error('Ошибка при удалении');
      }
      
      setItems(items.filter(item => item.id !== id));
      setError('');
    } catch (err) {
      console.error('Error deleting item:', err);
      setError('Ошибка удаления продукта');
    }
  };

  const toggleItemPosition = async (id) => {
    try {
      const response = await fetch(`/api/items/${id}/toggle`, {
        method: 'PATCH',
      });
      
      if (!response.ok) {
        throw new Error('Ошибка при перемещении');
      }
      
      const updatedItem = await response.json();
      setItems(items.map(item => 
        item.id === id ? updatedItem : item
      ));
      setError('');
    } catch (err) {
      console.error('Error toggling item:', err);
      setError('Ошибка перемещения продукта');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addItem();
    }
  };

  const clearError = () => setError('');

  const itemsInFridge = items.filter(item => item.is_in_fridge);
  const itemsOutside = items.filter(item => !item.is_in_fridge);

  if (loading) {
    return (
      <div className="fridge-app">
        <h1>🍽️ Холодильник</h1>
        <div className="loading">Загрузка данных...</div>
      </div>
    );
  }

  return (
    <div className="fridge-app">
      <h1>🍽️ Холодильник</h1>
      
      {error && (
        <div className="error-message">
          <span>{error}</span>
          <button onClick={clearError} className="error-close" title="Закрыть">×</button>
        </div>
      )}
      
      <div className="fridge-container">
        {/* Холодильник */}
        <div className={`fridge ${isOpen ? 'open' : ''}`}>
          <div className="fridge-door">
            <div className="door-handle" onClick={toggleDoor} title={isOpen ? 'Закрыть дверцу' : 'Открыть дверцу'}></div>
          </div>
          
          {/* Внутреннее содержимое холодильника */}
          {isOpen && (
            <div className="fridge-interior">
              <div className="fridge-content">
                <h3>📦 В холодильнике:</h3>
                {itemsInFridge.length === 0 ? (
                  <p className="empty-message">Холодильник пуст</p>
                ) : (
                  <div className="items-grid">
                    {itemsInFridge.map(item => (
                      <div key={item.id} className="fridge-item">
                        <span>{item.name}</span>
                        <div className="item-buttons">
                          <button 
                            onClick={() => toggleItemPosition(item.id)}
                            className="item-btn"
                            title="Вынуть из холодильника"
                          >
                            Вынуть
                          </button>
                          <button 
                            onClick={() => removeItem(item.id)}
                            className="item-btn delete"
                            title="Удалить продукт"
                          >
                            🗑️
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Продукты снаружи холодильника */}
        <div className="outside-items">
          <h3>📤 Рядом с холодильником:</h3>
          {itemsOutside.length === 0 ? (
            <p className="empty-message">Продуктов нет</p>
          ) : (
            <div className="items-grid">
              {itemsOutside.map(item => (
                <div key={item.id} className="fridge-item outside">
                  <span>{item.name}</span>
                  <div className="item-buttons">
                    <button 
                      onClick={() => toggleItemPosition(item.id)}
                      className="item-btn"
                      title="Положить в холодильник"
                    >
                      Положить
                    </button>
                    <button 
                      onClick={() => removeItem(item.id)}
                      className="item-btn delete"
                      title="Удалить продукт"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Панель управления */}
      <div className="control-panel">
        <button 
          onClick={toggleDoor} 
          className={`door-btn ${isOpen ? 'close' : 'open'}`}
          title={isOpen ? 'Закрыть холодильник' : 'Открыть холодильник'}
        >
          {isOpen ? '🚪 Закрыть холодильник' : '🚪 Открыть холодильник'}
        </button>
        
        <div className="add-item-form">
          <input
            type="text"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Введите название продукта..."
            maxLength={50}
          />
          <button onClick={addItem} title="Добавить продукт в холодильник">
            ➕ Добавить
          </button>
        </div>
      </div>

      {/* Статистика */}
      <div style={{ marginTop: '20px', color: '#666', fontSize: '14px' }}>
        Всего продуктов: {items.length} | В холодильнике: {itemsInFridge.length} | Снаружи: {itemsOutside.length}
      </div>
    </div>
  );
};

export default Fridge;