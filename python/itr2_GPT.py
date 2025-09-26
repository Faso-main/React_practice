# This cell generates a Python script that can create a large product knowledge tree in JSON,
# then runs it once to produce a sample file you can download.


import json, random, argparse, sys, textwrap, os
from datetime import datetime
from typing import List, Dict, Any

def generate_knowledge_tree(
    num_classes: int = 30,
    types_per_class_min: int = 8,
    types_per_class_max: int = 18,
    specs_per_type_min: int = 6,
    specs_per_type_max: int = 12,
    details_per_spec_min: int = 2,
    details_per_spec_max: int = 6,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Генерирует дерево знаний:
    Класс товара -> Тип товара -> Спецификация -> Подробная спецификация

    ВСЕ верхние id (классы) будут > 100.
    """
    random.seed(seed)

    # Библиотеки доменов
    class_pool = [
        "Товары для учёбы",
        "Стройка и ремонт",
        "Кухня и посуда",
        "Электроника",
        "Спорт и отдых",
        "Одежда и обувь",
        "Красота и здоровье",
        "Автотовары",
        "Зоотовары",
        "Товары для дома",
        "Сад и огород",
        "Игрушки и хобби",
        "Офис и канцелярия",
        "Бытовая техника",
        "Музыка и инструменты",
        "Фото и видео",
        "Компьютеры и сети",
        "Книги и журналы",
        "Продукты питания",
        "Напитки",
        "Умный дом",
        "Туризм и путешествия",
        "Ювелирные изделия",
        "Часы и аксессуары",
        "Детские товары",
        "Подарки и сувениры",
        "Здоровое питание",
        "Мебель",
        "Инструменты",
        "Безопасность и охрана",
        "Мото/Вело",
        "Домашний текстиль",
        "Строительные материалы",
        "Освещение",
        "Рыбалка и охота",
        "Товары для праздника",
        "Медицинские изделия",
        "Программное обеспечение",
        "Аудио и Hi-Fi",
        "Автозапчасти",
        "Кондитерка",
        "Косметика",
        "Парфюмерия",
        "Гигиена",
        "Табачные принадлежности",
        "Зоокорма",
        "Кормление и уход",
        "Сувениры",
        "Рукоделие",
        "Декор",
        "Посуда",
        "Кухонная техника",
        "Гаджеты",
        "Игровые приставки",
        "Настольные игры",
        "Смартфоны и планшеты",
        "Ноутбуки и ПК",
    ]

    # Типы по доменам (миксы + общая корзина)
    generic_types = [
        "Тетради", "Ручки", "Карандаши", "Линейки", "Фломастеры",
        "Блокноты", "Маркер", "Папки", "Степлеры", "Скотч",
        "Пила", "Дрель", "Молоток", "Отвёртки", "Шурупы",
        "Сковороды", "Кастрюли", "Ножи", "Кружки", "Тарелки",
        "Сыр", "Колбаса", "Хлеб", "Молоко", "Кофе",
        "Смартфоны", "Ноутбуки", "Наушники", "Колонки", "Телевизоры",
        "Кроссовки", "Куртки", "Футболки", "Джинсы", "Кепки",
        "Гантели", "Скакалки", "Коврики для йоги", "Мячи", "Ракетки",
        "Косметика", "Парфюм", "Шампунь", "Зубная паста", "Мыло",
        "Кабели", "Зарядные устройства", "Память", "Флешки", "Роутеры",
        "Игрушки", "Настольные игры", "Пазлы", "Конструкторы", "Куклы",
        "Фотоаппараты", "Объективы", "Штативы", "Фильтры", "Дроны",
        "Холодильники", "Пылесосы", "Стиральные машины", "Плиты", "Микроволновки"
    ]

    spec_pool = [
        "Размеры", "Вес", "Цвет", "Материал", "Бренд", "Модель",
        "Страна производства", "Гарантия", "Срок годности", "Энергопотребление",
        "Совместимость", "Интерфейсы", "Ёмкость", "Мощность", "Длина кабеля",
        "Тип упаковки", "Температурный режим", "Класс защиты", "Класс точности",
        "Количество в наборе", "Жёсткость", "Плотность", "Толщина", "Объём",
        "Разрешение", "Диагональ", "Частота", "Скорость", "Прочность"
    ]

    # детальные спецификации по "семействам" характеристик
    detail_templates = {
        "Размеры": lambda: {
            "длина": round(random.uniform(1, 300), 2),
            "ширина": round(random.uniform(1, 300), 2),
            "высота": round(random.uniform(1, 300), 2),
            "единица": random.choice(["мм", "см", "м"]),
        },
        "Вес": lambda: {
            "значение": round(random.uniform(0.01, 100), 3),
            "единица": random.choice(["г", "кг"]),
        },
        "Цвет": lambda: {
            "основной": random.choice(
                ["чёрный","белый","серый","красный","синий","зелёный","жёлтый","оранжевый","фиолетовый","коричневый"]
            ),
            "rgb": [random.randint(0,255) for _ in range(3)],
        },
        "Материал": lambda: {
            "основной": random.choice(["пластик","сталь","алюминий","дерево","бумага","стекло","керамика","каучук","хлопок","полиэстер"]),
            "покрытие": random.choice(["нет","лакировка","анодирование","порошковая окраска"])
        },
        "Бренд": lambda: {"название": random.choice(["Acme","Orion","Helios","Nord","Vega","Aurum","Delta","Zenith","Galaxy","Nova"]) },
        "Модель": lambda: {"код": f"M{random.randint(100,999)}-{random.choice('ABCDEFG')}{random.randint(1,9)}" },
        "Страна производства": lambda: {"страна": random.choice(["Китай","Россия","Германия","Польша","Италия","Вьетнам","Турция","Индия","Франция","США"]) },
        "Гарантия": lambda: {"месяцев": random.choice([6,12,24,36]) },
        "Срок годности": lambda: {"месяцев": random.choice([3,6,12,18,24,36]) },
        "Энергопотребление": lambda: {"кВт⋅ч": round(random.uniform(0.1, 3.5), 2), "класс": random.choice(["A","A+","A++","B"]) },
        "Совместимость": lambda: {"поддержка": random.sample(["Windows","macOS","Linux","Android","iOS","HarmonyOS"], k=random.randint(1,4))},
        "Интерфейсы": lambda: {"порты": random.sample(["USB-A","USB-C","HDMI","DisplayPort","3.5мм","RJ-45","Wi-Fi","Bluetooth","NFC"], k=random.randint(1,5))},
        "Ёмкость": lambda: {"значение": random.choice([8,16,32,64,128,256,512,1024]), "единица": random.choice(["ГБ","мА⋅ч","л"]) },
        "Мощность": lambda: {"ватт": random.choice([5,10,18,20,45,65,90,120,500,1000]) },
        "Длина кабеля": lambda: {"метры": round(random.uniform(0.1, 10.0), 2) },
        "Тип упаковки": lambda: {"вид": random.choice(["коробка","блистер","пакет","бобина","рулон","паллет"]) },
        "Температурный режим": lambda: {"мин": random.randint(-40, 0), "макс": random.randint(30, 120), "единица": "°C" },
        "Класс защиты": lambda: {"IP": f"IP{random.randint(20,69)}" },
        "Класс точности": lambda: {"класс": random.choice(["A","B","C","D"]) },
        "Количество в наборе": lambda: {"шт": random.randint(1, 50) },
        "Жёсткость": lambda: {"шкала": random.choice(["HB","H","2H","B","2B","F"]) },
        "Плотность": lambda: {"значение": random.randint(60, 300), "единица": "г/м²" },
        "Толщина": lambda: {"значение": round(random.uniform(0.05, 50.0), 2), "единица": "мм" },
        "Объём": lambda: {"значение": round(random.uniform(0.1, 100.0), 2), "единица": random.choice(["л","мл","м³"]) },
        "Разрешение": lambda: {"px": f"{random.choice([1280,1920,2560,3840])}×{random.choice([720,1080,1440,2160])}" },
        "Диагональ": lambda: {"дюймы": round(random.uniform(4.7, 85.0), 1) },
        "Частота": lambda: {"Гц": random.choice([50,60,120,144,240,360]) },
        "Скорость": lambda: {"единица": random.choice(["Мбит/с","страниц/мин","об/мин"]), "значение": round(random.uniform(1, 5000), 2) },
        "Прочность": lambda: {"класс": random.choice(["низкая","средняя","высокая"]), "метод": random.choice(["Шор","Роквелл","Виккерс"]) },
    }

    def make_details_for_spec(spec_name: str) -> Dict[str, Any]:
        # Возвращаем 1–N детальных полей по шаблону, либо generic словарь
        n = random.randint(details_per_spec_min, details_per_spec_max)
        if spec_name in detail_templates:
            # генерим один «шаблонный» объект и миксуем с произвольными ключами
            base = detail_templates[spec_name]()
            # добавим произвольные поля
            for i in range(max(0, n - len(base))):
                base[f"доп_{i+1}"] = random.choice([True, False, round(random.uniform(0.1, 999.9), 2), random.randint(1,999)])
            return base
        else:
            return {f"поле_{i+1}": random.choice([True, False, round(random.uniform(0.1, 999.9), 2), random.randint(1,999)]) for i in range(n)}

    # IDшники: гарантируем, что верхние (классы) > 100
    next_class_id = 101 + random.randint(0, 5000)
    next_type_id = 100_000 + random.randint(0, 50_000)
    next_spec_id = 200_000 + random.randint(0, 50_000)
    next_detail_id = 1_000_000 + random.randint(0, 200_000)

    used_class_names = set()
    classes: List[Dict[str, Any]] = []

    # обеспечим, что уникальных классов хватит
    while len(class_pool) < num_classes:
        class_pool.append(f"Категория {len(class_pool)+1}")

    for _ in range(num_classes):
        # уникальное имя класса
        name = random.choice(class_pool)
        while name in used_class_names:
            name = f"{name} {random.randint(2,99)}"
        used_class_names.add(name)

        num_types = random.randint(types_per_class_min, types_per_class_max)
        types = []
        for _ in range(num_types):
            tname = random.choice(generic_types)
            type_entry = {
                "id": next_type_id,
                "тип_товара": tname,
                "спецификации": []
            }
            next_type_id += 1

            num_specs = random.randint(specs_per_type_min, specs_per_type_max)
            chosen_specs = random.sample(spec_pool, k=min(num_specs, len(spec_pool)))
            for sname in chosen_specs:
                spec_entry = {
                    "id": next_spec_id,
                    "спецификация": sname,
                    "подробная_спецификация": {
                        "id": next_detail_id,
                        "значения": make_details_for_spec(sname)
                    }
                }
                next_spec_id += 1
                next_detail_id += 1
                type_entry["спецификации"].append(spec_entry)

            types.append(type_entry)

        cls = {
            "id": next_class_id,
            "класс_товара": name,
            "типы": types
        }
        next_class_id += 1
        classes.append(cls)

    return {
        "версия": "1.0",
        "сгенерировано": datetime.utcnow().isoformat() + "Z",
        "описание": "Дерево знаний: Класс -> Тип -> Спецификация -> Подробная спецификация",
        "классы": classes
    }

# --- If run as a script ---
script_code = r'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор большого дерева знаний (JSON).
Пример:
Класс товара -> Тип товара -> Спецификация -> Подробная спецификация.
Все верхние id (классы) > 100.
"""
import json, random, argparse
from datetime import datetime

# (Встроенная та же логика, что в ноутбуке; для краткости вызываем уже импортированную функцию)
from __main__ import generate_knowledge_tree

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--num_classes", type=int, default=150, help="Сколько классов товаров создать")
    p.add_argument("--types_min", type=int, default=8, help="Мин. типов на класс")
    p.add_argument("--types_max", type=int, default=18, help="Макс. типов на класс")
    p.add_argument("--specs_min", type=int, default=6, help="Мин. спецификаций на тип")
    p.add_argument("--specs_max", type=int, default=12, help="Макс. спецификаций на тип")
    p.add_argument("--details_min", type=int, default=2, help="Мин. полей в подробной спецификации")
    p.add_argument("--details_max", type=int, default=6, help="Макс. полей в подробной спецификации")
    p.add_argument("--seed", type=int, default=42, help="Сид для воспроизводимости")
    p.add_argument("--out", type=str, default="knowledge_tree.json", help="Куда сохранить JSON")
    args = p.parse_args()

    data = generate_knowledge_tree(
        num_classes=args.num_classes,
        types_per_class_min=args.types_min,
        types_per_class_max=args.types_max,
        specs_per_type_min=args.specs_min,
        specs_per_type_max=args.specs_max,
        details_per_spec_min=args.details_min,
        details_per_spec_max=args.details_max,
        seed=args.seed,
    )
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"OK: saved -> {args.out}")

if __name__ == "__main__":
    main()
'''.strip("\n")

# Save the script for the user
script_path = "gen_knowledge_tree.py"
with open(script_path, "w", encoding="utf-8") as f:
    f.write(script_code)

# Generate a sample JSON now (moderate size to keep file reasonable)
sample = generate_knowledge_tree(
    num_classes=30,
    types_per_class_min=8,
    types_per_class_max=12,
    specs_per_type_min=6,
    specs_per_type_max=10,
    details_per_spec_min=2,
    details_per_spec_max=4,
    seed=1337,
)

out_path = "knowledge_tree_sample.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(sample, f, ensure_ascii=False, indent=2)

(out_path, script_path, len(sample["классы"]))
