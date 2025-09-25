import React, { useState } from 'react';
import './App.css';

const Fridge = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [items, setItems] = useState([
    { id: 1, name: 'Молоко', isInFridge: true },
    { id: 2, name: 'Яйца', isInFridge: true },
    { id: 3, name: 'Сыр', isInFridge: true },
    { id: 4, name: 'Колбаса', isInFridge: false },
    { id: 5, name: 'Овощи', isInFridge: false },
  ]);
  const [newItemName, setNewItemName] = useState('');

  const toggleDoor = () => {
    setIsOpen(!isOpen);
  };

  const addItem = () => {
    if (newItemName.trim() === '') return;
    
    const newItem = {
      id: Date.now(),
      name: newItemName,
      isInFridge: true,
    };
    
    setItems([...items, newItem]);
    setNewItemName('');
  };

  const removeItem = (id) => {
    setItems(items.filter(item => item.id !== id));
  };

  const toggleItemPosition = (id) => {
    setItems(items.map(item => 
      item.id === id ? { ...item, isInFridge: !item.isInFridge } : item
    ));
  };

  const itemsInFridge = items.filter(item => item.isInFridge);
  const itemsOutside = items.filter(item => !item.isInFridge);

  return (
    <div className="fridge-app">
      <h1>Холодильник</h1>
      
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
                  <p>Холодильник пуст</p>
                ) : (
                  <div className="items-grid">
                    {itemsInFridge.map(item => (
                      <div key={item.id} className="fridge-item">
                        <span>{item.name}</span>
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
                          🗑️
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Продукты снаружи холодильника - теперь горизонтально рядом */}
        {itemsOutside.length > 0 && (
          <div className="outside-items">
            <h3>Рядом с холодильником:</h3>
            {itemsOutside.length === 0 ? (
              <p>Нет продуктов снаружи</p>
            ) : (
              <div className="items-grid">
                {itemsOutside.map(item => (
                  <div key={item.id} className="fridge-item outside">
                    <span>{item.name}</span>
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
                      🗑️
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Панель управления - теперь отдельно внизу */}
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
            placeholder="Введите название продукта"
            onKeyPress={(e) => e.key === 'Enter' && addItem()}
          />
          <button onClick={addItem}>Добавить</button>
        </div>
      </div>
    </div>
  );
};

export default Fridge;