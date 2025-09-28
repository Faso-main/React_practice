import React, { useState, useEffect } from 'react';
import './App.css';

const Fridge = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [items, setItems] = useState([]);
  const [newItemName, setNewItemName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [pythonMessage, setPythonMessage] = useState(''); // Новое состояние для Python сообщения

  // Функция проверки связи с Python
  const testPythonConnection = async () => {
    try {
      console.log('Проверка связи с Python...');
      const response = await fetch('http://localhost:8000/api/python-message');
      
      if (!response.ok) {
        throw new Error(`Python сервер не отвечает: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Ответ от Python:', data);
      setPythonMessage(data.text);
      setError('');
      
      // Автоматически скрываем сообщение через 5 секунд
      setTimeout(() => setPythonMessage(''), 5000);
      
    } catch (err) {
      console.error('Ошибка связи с Python:', err);
      setPythonMessage('Python сервер недоступен');
    }
  };

  // Загрузка данных с сервера (основной бэкенд)
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

  // Остальные функции остаются без изменений
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

  const clearError = () => {
    setError('');
    setPythonMessage('');
  };

  const itemsInFridge = items.filter(item => item.is_in_fridge);
  const itemsOutside = items.filter(item => !item.is_in_fridge);

  if (loading) {
    return (
      <div className="fridge-app">
        <h1>Холодильник</h1>
        <div className="loading">Загрузка данных...</div>
      </div>
    );
  }

  return (
    <div className="fridge-app">
      <h1>Холодильник + Python тест</h1>
      
      {/* Сообщение от Python */}
      {pythonMessage && (
        <div className="python-message">
          {pythonMessage}
          <button onClick={() => setPythonMessage('')} className="error-close">×</button>
        </div>
      )}
      
      {/* Сообщение об ошибке */}
      {error && (
        <div className="error-message">
          <span>{error}</span>
          <button onClick={clearError} className="error-close">×</button>
        </div>
      )}
      
      <div className="fridge-container">
        {/* Холодильник */}
        <div className={`fridge ${isOpen ? 'open' : ''}`}>
          <div className="fridge-door">
            <div className="door-handle" onClick={toggleDoor}></div>
          </div>
          
          {/* Внутреннее содержимое холодильника */}
          {isOpen && (
            <div className="fridge-interior">
              <div className="fridge-content">
                <h3>В холодильнике:</h3>
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
                          >
                            Вынуть
                          </button>
                          <button 
                            onClick={() => removeItem(item.id)}
                            className="item-btn delete"
                          >
                            Удалить
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
          <h3>Рядом с холодильником:</h3>
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
                    >
                      Положить
                    </button>
                    <button 
                      onClick={() => removeItem(item.id)}
                      className="item-btn delete"
                    >
                      Удалить
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
        >
          {isOpen ? 'Закрыть холодильник' : 'Открыть холодильник'}
        </button>
        
        <div className="add-item-form">
          <input
            type="text"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Введите название продукта"
            maxLength={50}
          />
          <button onClick={addItem}>
            Добавить
          </button>
                  {/* Кнопка проверки связи с Python */}
          <button 
            onClick={testPythonConnection}
            style={{
              background: '#ff9800',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: 'bold'
            }}
          >
            Проверить связь с Python
          </button>
        </div>
      </div>
    </div>
  );
};

export default Fridge;