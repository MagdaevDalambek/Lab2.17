#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Самостоятельно изучите работу с пакетом click для построения интерфейса командной строки
# (CLI). Для своего варианта лабораторной работы 2.16 необходимо реализовать интерфейс
# командной строки с использованием пакета click.

import json
import click


def display_routes(routes):
    """
    Отобразить список маршрутов
    """
    if routes:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^14} |'.format(
                "№",
                "Начальный пункт",
                "Конечный пункт",
                "Номер маршрута"
            )
        )
        print(line)

        for idx, worker in enumerate(routes, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>14} |'.format(
                    idx,
                    worker.get('start', ''),
                    worker.get('finish', ''),
                    worker.get('number', 0)
                )
            )
        print(line)
    else:
        print("Список маршрутов пуст")


def load_routes(file_name):
    """
    Загрузить данные из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def save_routes(file_name, staff):
    """
    Сохранить данные в файл JSON
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


@click.group()
def commands():
    pass


@commands.command("add")
@click.argument("filename")
@click.option("--start", help="Start")
@click.option("--finish", help="Finish")
@click.option("--number", help="Number")
def add(filename, start, finish, number):
    """
    Добавить данные о маршруте
    """
    routes = load_routes(filename)
    route = {
        "start": start,
        "finish": finish,
        "number": number,
    }
    routes.append(route)
    save_routes(filename, routes)


@commands.command("display")
@click.argument("filename")
def display(filename):
    """
    Отобразить список маршрутов
    """
    routes = load_routes(filename)
    display_routes(routes)


@commands.command("select")
@click.argument("number")
@click.argument("filename")
def select(filename, number):
    """
    Выбрать маршрут с заданным номером
    """
    routes = load_routes(filename)
    result = []
    for route in routes:
        if route.get("number") == number:
            result.append(route)

    display_routes(result)


def main():
    commands()


if __name__ == "__main__":
    main()
