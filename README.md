# Система автоматизации нанесения авторских логотипов на фотографии "Stamper"

## Цели и задачи

 - Целью разработки является создание WEB-приложения для нанесения на фотографии авторских логотипов;

 Для достижения цели решены следующие задачи:
 - ...

## Архитектура приложения

*Модель приложения* представляет собой вариант шаблона проектирования объектно-ориентированных приложений Model-View-Controller.

 <Архитектура>

A WEB-application to make authors' logos in their photos

## Программное обеспечение

Система разрабатывается согласно руководству с https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/

 1. Язык программирования - Python-3.6.5 https://python.org;
 2. Среда разработки веб-приложений - Pyramid https://trypyramid.com/;
 3. Шаблоны HTML-страниц Chameleon https://chameleon.readthedocs.io/en/latest/;
 4. Шаблон HTML-сайта Vali Admin https://www.npmjs.com/package/vali-admin;
 6. Библиотека обработки изображений https://pillow.readthedocs.io/en/5.1.x/handbook/tutorial.html;
 7. Библиотека отображения реляционных баз данных на объектную структуру Python https://www.sqlalchemy.org/download.html;
 9. Хранилище данных, включая изображения, реализована при помощи Percona Server (MySQL) https://www.percona.com/software/mysql-database/percona-server;



## Заключение

Во время производственной практики решены следующие задачи:

 1.
 2.

## Приложения

### Запуск сервера Percona

Для того, чтобы запустить виртуальную машину с сервером Percona необходимо выплонить следующую команду:

```shell
$ docker run --name stamper -e MYSQL_ROOT_PASSWORD=stamperpsw -d percona
```

Здесь `-d` обозначает, что запуск виртуальной машины осуществляется в режиме демона.

### Администрирование сервера Percona

MySQL - это программное обеспечение с открытым исходным кодом для управления базами данных, которое помогает пользователям хранить, организовывать и осуществлять доступ к информации. Оно имеет множество вариантов тонкой настройки прав доступа к таблицам и базам данных для каждого пользователя. Данное руководство представит вам краткий обзор некоторых из этих вариантов [....].

#### Создание нового пользователя

Разработанное приложение требует более жестких ограничений, есть способы создания пользователей с особыми наборами прав доступа.

Создание нового пользователя осуществляется в консоли MySQL:

```sql
CREATE USER 'stamper'@'172.%' IDENTIFIED BY 'stamperpsw';
```

К сожалению, на данном этапе пользователь "newuser" не имеет прав делать что-либо с базами данных. На самом деле, даже если если пользователь "newuser" попробует залогиниться (с паролем "stamperpsw"), он не попадет в консоль MySQL.

Таким образом, первое, что нам необходимо сделать, это предоставить пользователю доступ к информации, которая ему потребуется.

```sql
GRANT ALL PRIVILEGES ON *.* TO 'stamper'@'172.%';
```

Звездочки в этой команде задают базу и таблицу, соответственно, к которым у пользователя будет доступ. Конкретно эта команда позволяет пользователю читать, редактировать, выполнять любые действия над всеми базами данных и таблицами.

Поле завершения настройки прав доступа новых пользователей, убедитесь, что вы обновили все права доступа:

```
FLUSH PRIVILEGES;
```

Проверка подключения:

```shell
mysql -h 172.17.0.2 -u stamper -pstamperpsw mysql
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.21-21 Percona Server (GPL), Release '21', Revision '2a37e4e'

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [mysql]>
```

Командная строка MySQL запустилась, следовательно, аутентификация пользователя прошла успешно.

### Создание базы данных

```shell
MySQL [mysql]> CREATE DATABASE stamper;
Query OK, 1 row affected (0.00 sec)

MySQL [mysql]> USE stamper;
Database changed
MySQL [stamper]> DROP DATABASE stamper;
Query OK, 0 rows affected (0.00 sec)
```


## Список использованных источников

 1.

 2.
 10. Создание нового пользователя и настройка прав доступа в MySQL | DigitalOcean URL:https://www.digitalocean.com/community/tutorials/mysql-ru .


## Установка среды разработки

Удобно разрабатывать проекты в среде программирования, не зависящей от операционной системы и установленных в ней пакетах. Для языка Python разработаны средства формирования такой среды, в частности `virtualenv`.

### Виртуальные среды

<Виртуальная среда python, > `virtualenv`

### Установка пакетов

Разработанный программный продукт является пакетом Python, т.е. специальным образом организованный архив исходного кода и других ресурсов, загружаемый с сервера пакетов. Создание пакетов автоматизировано при помощи пакета `cookiecutter`. Установка этого пакета осуществляется следующей командой, запускаемой в созданном виртуальном окружении.

```
$ pip install -U pip cookiecutter
```

Следующим этапом является создание пакета. Он выполняется при помощи команды:

```shell
$ cookiecutter gh:Pylons/pyramid-cookiecutter-alchemy --checkout 1.9-branch
project_name [Pyramid Scaffold]: Stamper Server
repo_name [stamper_server]: stamper

===============================================================================
Documentation: https://docs.pylonsproject.org/projects/pyramid/en/latest/
Tutorials:     https://docs.pylonsproject.org/projects/pyramid_tutorials/en/latest/
Twitter:       https://twitter.com/PylonsProject
Mailing List:  https://groups.google.com/forum/#!forum/pylons-discuss
Welcome to Pyramid.  Sorry for the convenience.
===============================================================================

Change directory into your newly created project.
    cd stamper
. . . . . . . . . . . .
```

Установка созданного пакета в режим разработки осуществляется командой:
```shell

### Инициализация базы данных

Первый этап - собственно создание базы данных:

```shell
$ mysql -h 172.17.0.2 -u stamper -pstamperpsw
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.21-21 Percona Server (GPL), Release '21', Revision '2a37e4e'

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> CREATE DATABASE stamper;
Query OK, 1 row affected (0.00 sec)
```
Второй этап - порождение таблиц, которое выполняется при помощи сгенерированного скрипта (сценария).

```shell
(stumper) eugeneai@inca ~/projects/stamper
$ initialize_stamper_db development.ini
2018-05-19 11:07:39,675 INFO  [sqlalchemy.engine.base.Engine:1151][MainThread] SHOW VARIABLES LIKE 'sql_mode'
2018-05-19 11:07:39,675 INFO  [sqlalchemy.engine.base.Engine:1154][MainThread] ()
2018-05-19 11:07:39,682 INFO  [sqlalchemy.engine.base.Engine:1151][MainThread] SELECT DATABASE()
2018-05-19 11:07:39,682 INFO  [sqlalchemy.engine.base.Engine:1154][MainThread] ()
2018-05-19 11:07:39,682 INFO  [sqlalchemy.engine.base.Engine:1151][MainThread] show collation where `Charset` = 'utf8' and `Collation` = 'utf8_bin'
. . . . . . .
```

Запуск тестового сервера и обработка главной страницы сервером:

```shell
$ pserve development.ini
Starting server in PID 28330.
Serving on http://localhost.localdomain:6543
2018-05-19 11:13:03,644 INFO  [sqlalchemy.engine.base.Engine:1151][waitress] SHOW VARIABLES LIKE 'sql_mode'
2018-05-19 11:13:03,644 INFO  [sqlalchemy.engine.base.Engine:1154][waitress] ()
. . . . . . .
```

В этом примере SqlAlchemy в журнал выводит команды сервера (SQL), запускаемые при открытии базы данных.


# Тестирование сайта

По умолчанию сгенерированный пакет создает сервер, который выдает следующую страницу:

![Alt text](pics/pyramid.png?raw=true "Страница Pyramid по умолчанию")

Рис. 1. Страница Pyramid по умолчанию

После внесения вышеупомянутых модификаций получен новый вид сайта, соответствующий шаблону Vali Admin.

![Alt text](pics/vali.png?raw=true "Страница Vali Admin")
