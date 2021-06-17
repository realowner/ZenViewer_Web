## Установка и запуск проекта
---
После клонирования, откройте терминал в папке с проектом. Убедитесь, что находитесь на ветке `master`
```
~$ git branch
```
Если активная ветка `develop` переключитесь с помощью:
```
~$ git checkout master
```
В папке с проектом создайте виртуальное окружение:
```
~$ python3 -m venv venv
```
Активируйте среду:
```
~$ source venv/bin/activate
```
После активации, установите зависимости:
```
(venv)~$ python -m pip install -r requirements.txt
```
Запуск приложения внутри окружения:
```
(venv)~$ python zenviewer.py
```
После запуска открывать `http://127.0.0.1:3729/`
Чтобы остановить сервер в командной строке нажать сочетание клавиш `Ctrl+C`