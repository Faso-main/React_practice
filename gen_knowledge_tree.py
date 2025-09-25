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