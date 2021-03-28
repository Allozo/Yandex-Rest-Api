# Yandex

Это репозиторий для проекта, который являются частью отборочных испытаний.

## Setup

Для скачивания библиотек будет нужен pip.
Установить его можно командами:

```shell
sudo apt-get update
sudo apt install python3-pip
```

Данный проект нуждается в библиотеках, которых нет по умолчанию. 
Нужные зависимости указаны в файле `requirements.txt`.
Для установки нужных библиотек воспользуетесь командой:

```shell
pip3 install -r requirements.txt
```

## Тестирование 

В директории находится файл с тестами `TestClient.py`. 
Для запуска теста можно запустить файл с помощью:
```python
python TestClient.py
```

Будет запущена функция test_pack(), которая вызовет функции тестирования в нужном порядке. 
Тесты устроены так, чтобы покрывать потенциально проблемные места.
