#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Самостоятельно изучите работу с пакетом click для построения интерфейса командной строки
# (CLI). Для своего варианта лабораторной работы 2.16 необходимо реализовать интерфейс
# командной строки с использованием пакета click.

import json
import click
from jsonschema import validate, ValidationError


@click.group()
def cli():
    pass


@cli.command("add")
@click.argument('filename')
@click.option("-n", "--name")
@click.option("-g", "--group")
@click.option("-gr", "--grade")
def add(filename, name, group, grade):
    """
    Добавить данные о студенте
    """
    # Запросить данные о студенте.
    students = load_students(filename)
    students.append(
        {
            'name': name,
            'group': group,
            'grade': grade,
        }
    )
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)
    click.secho("Студент добавлен")


@cli.command("display")
@click.argument('filename')
@click.option('--select', '-s', type=int)
def display(filename, select=None):
    """
    Отобразить список студентов
    """
    students = load_students(filename)
    if select == 1:
        students = selected(students)

    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Группа",
            "Успеваемость"
        )
    )
    print(line)

    # Вывести данные о всех студентах.
    for idx, student in enumerate(students, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                idx,
                student.get('name', ''),
                student.get('group', ''),
                student.get('grade', 0)
            )
        )
    print(line)


def selected(list):
    # Проверить сведения студентов из списка.
    students = []
    for student in list:
        result = [int(x) for x in (student.get('grade', '').split())]
        if sum(result) / max(len(result), 1) >= 4.0:
            students.append(student)
    return students


def load_students(filename):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "group": {"type": "integer"},
                "grade": {"type": "string"},
            },
            "required": [
                "name",
                "group",
                "grade",
            ],
        },
    }
    with open(filename, "r") as file_in:
        data = json.load(file_in)  # Прочитать данные из файла

    try:
        # Валидация
        validate(instance=data, schema=schema)
        print("JSON валиден по схеме.")
    except ValidationError as e:
        print(f"Ошибка валидации: {e.message}")
    return data


if __name__ == '__main__':
    cli()
