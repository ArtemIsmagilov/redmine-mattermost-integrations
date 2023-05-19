# Mattermost-Redmine Integrations

![header.png](./imgs/header.png "Diagram project.")

* **Проект создан для интеграции сервиса mattermost и redmine.**
* **Данная версия поддерживает локальную интеграцию.**

## Преимущества

* Автоматическое создание тикетов. Одним сообщением можно создать несколько тикетов
* Мониторинг тикетов в redmine. Вы всегда можете одной командой посмотреть тикеты на себя, посмотреть
  созданные тикеты.
* Расширяемое приложение. Можно добавить объединение нескольких пользователей в группы, управление тикетами,
  уведомление на почту по определённым событиям, автоматическое создание нескольких проектов в одну строку
  и многое другое.

## Актуальность.

> 💡 *В компании есть встречи, по результатам встречи раздаются поручения. Поручения теряются и не выполняются.*
> *Параллельно поручения живут в тикетах в багтрекере.*
> *Хочется, чтобы все поручения жили в багтрекере, там мониторились и выполнялись.*

## За интеграцию отвечает самостоятельное приложение на python с библиотекой Flask в виде бота.

| Поддерживаемы команды | Описание                            |
|-----------------------|-------------------------------------|
| /app_info             | Возможности приложения              |
| /create_issues        | Создать задания                     |
| /tickets_for_me       | Посмотреть задания назначенные мне  |
| /my_tickets           | Посмотреть задания назначенные мною |

## Тестирование приложения будет состоять из небольших пунктов.

1. Предустановить необходимые пакеты
2. Создать общую docker сеть
3. Установить докер контейнер redmine и запустить
4. Установить докер контейнер mattermost и запустить
5. После активации REST API на локальных сервисах добавить необходимые переменные окружения в файл
   `.docker.env` приложения. Файл находится в `./mattermost_app/.docker.env`
6. После добавления всех необходимых переменных в `./mattermost_app/.docker.env` установить докер контейнер
   redmine-mattermost-bridge и запустить
7. Установить приложение в mattermost командой c параметрами хоста и порта виртуального окружения

   ```
   /apps install http http://host:port/manifest.json
   ```

8. Сгенерируйте токен для приложения через настройки
9. Добавьте токен в виртуальное окружение `./mattermost_app/.docker.env`
10. Приложение готово

## Схема проекта

![diagram.svg](./imgs/diagram.svg "Diagram project.")

## Настраиваем среду разработки

* Подробную информацию по первичной настройке можно посмотреть по ссылке
  https://developers.mattermost.com/integrate/apps/quickstart/quick-start-python/


* Первым делом удаляю старую версию docker и устанавливаю новую
  https://docs.docker.com/engine/install/ubuntu/

* Установите общую docker сеть для контейнеров, мы назовем её `dev`
    ```shell
      docker network create --driver=bridge --subnet=172.10.0.0/16 --gateway=172.10.0.1 dev
   ```

* копируем ./app_integration/.docker.env.example в ./app_integration/.docker.env
  ```shell
  cp ./app_integration/.docker.env.example ./app_integration/.docker.env
  ```

## Установка redmine контейнера через docker-compose.yml

Установить docker контейнер redmine мне помогла эта статья https://kurazhov.ru/install-redmine-on-docker-compose/

* добавил себя (например username) в группу
   ```shell
  sudo usermod -aG docker username
   ```

* далее перехожу в `./redmine_server` и ставлю redmine контейнер
  ```shell
  cd ./redmine_server && docker compose up
  ```

* переходим на сайт с логином admin и паролем admin, меняем пароль, далее `Администрирование` > `Настройки`
    + Раздел `Аутентификация` - Да
    + Раздел `API` - Подключаем REST и JSONP
      ![screen1.png](./imgs/screen1.png "Redmine activate API")

* добавляем уведомление по почте (пример настройки можно посмотреть в config docker контейнера redmine,
  предварительно войдите в оболочку контейнера)
  ```shell
  docker exec -it `container_name` bash
  ``` 
  пример находится по следующему пути `config/configuration.yml.example`.
* итак, добавляем.
  ```shell
  nano ./storage/configuration.yml 
  ``` 
* впишите следующее и измените нужные параметры.
    ```yaml
    production:
      email_delivery:
        delivery_method: :smtp
        smtp_settings:
          enable_starttls_auto: true
          address: "smtp.gmail.com"
          port: 587
          domain: "smtp.gmail.com"
          authentication: :plain
          user_name: "your_email@gmail.com"
          password: "password" 
    ```
* обновляем версию redmine на текущую
  ```shell
  docker compose build
  docker compose restart
  ```

## Установка mattermost контейнера через docker-compose.yml

Детали установки контейнера и приложения можно посмотреть тут
https://developers.mattermost.com/integrate/apps/quickstart/quick-start-python/

* переходим в `./mattermost_server/` и запускаем mattermost контейнер
  ```shell
    docker compose up
    ```
* mattermost контейнер запущен
  ![screen2.png](./imgs/screen2.png "Home page for loging")

* нам нужно сгенерировать токен админа для REST API запросов и добавить в `./app_inegration/docker.env`.
  ![screen3.png](./imgs/screen3.png "Generate access admin token")

## Установка интеграции Redmine и Mattermost

* переходим в директорию ./app_integration и запускаем последний контейнер с ботом-приложением.
    ```shell
      docker compose up
    ```

* давайте удостоверимся, что приложение действительно работает и может пинговаться с другими docker контейнерами
  ```shell
  docker exec -it conteiner_name_app bash
  curl -I http://172.10.1.10:3000/
  ```
  > HTTP/1.1 200 OK
  ```shell
  curl -I http://172.10.1.30:8065/
  ```
  > HTTP/1.1 405 Method Not Allowed

    - или можно просто посмотреть конфиг docker сети `dev`. Все запущенные контейнеры находятся в одной сети
      ```shell
      docker network inspect dev
      ```

* Чтобы установить приложение, нужно перейти на наш mattermost сайт и ввести `/`(slash) команду по примеру из
  официальной документации. https://developers.mattermost.com/integrate/apps/quickstart/quick-start-python/
  > #### Install the App on Mattermost
  > `/apps install http http://mattermost-apps-python-hello-world:8090/manifest.json`

  В моем случае, я добавил команду `/apps install http http://172.10.1.50:8090/manifest.json`
* Если вам нужно удалить его, то смотрим здесь
  https://developers.mattermost.com/integrate/apps/quickstart/quick-start-python/#uninstall-the-app
* После успешной загрузки нужно сгенерировать токен для приложения, добавить его в `./app_integration/.docker.env`
  Сгенерировать токен нужно в разделе `Интеграции` > `Аккаунты ботов` > `@redmine-mattermost-bridge`.
  Также предоставьте доступ бота к Direct сообщениям так как интеграция работает через личные сообщения. Интеграция
  работает c API токеном.

  ![screen4.png](./imgs/screen4.png "Generate access app token and get privilege.")


* Теперь приложение будет:
    - создавать тикеты
    - показывать тикеты, которые поручены вам
    - показывать тикеты, которые вы назначили
    - обрабатывать ошибки при отсутствии вас как пользователя на платформе redmine или отсутствии необходимых токенов,
      или
      при вводе невалидной информации.

### Информация о приложении `/app_info`

![screen8.png](./imgs/screen8.png "Help info.")

### Создать задания `/create_issues`

![screen5.jpeg](./imgs/screen5.jpeg "Create issues.")

### Посмотреть задания назначенные мне `/tickets_for_me`

![screen6.jpeg](./imgs/screen6.jpeg "Look ticket for me.")

### Посмотреть задания назначенные мною `/my_tickets`

![screen7.jpeg](./imgs/screen7.jpeg "Look my tickets.")

## Используемые библиотеки:

* `mattermostdriver`.
    - Github https://github.com/Vaelor/python-mattermost-driver
    - Документация https://vaelor.github.io/python-mattermost-driver
* `python-redmine`.
    - Github https://github.com/maxtepkeev/python-redmine
    - Документация https://python-redmine.com/index.html

## Полезные ссылки

* REST API redmine - https://www.redmine.org/projects/redmine/wiki/Developer_Guide
* Простое приложение `hello world` в mattermost на python -
  https://developers.mattermost.com/integrate/apps/quickstart/quick-start-python/
* REST API mattermost - https://api.mattermost.com/
* matterbridge https://github.com/42wim/matterbridge
* Mattermost chat plugin for Redmine - https://github.com/altsol/redmine_mattermost
* Docker image Redmine - https://hub.docker.com/_/redmine
* Установка redmine через
  docker-compose - https://kurazhov.ru/install-redmine-on-docker-compose/?ysclid=lhu5e6s0bb161225177
* Чат-бот для mattermost - https://habr.com/ru/companies/hh/articles/727246/
* Документация по докеру - https://docs.docker.com/engine/install/








