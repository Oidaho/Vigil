# Vigil

![Banner](https://github.com/user-attachments/assets/bceeb209-7503-4c45-9192-0de351710ba3)

![GitHub Release](https://img.shields.io/github/v/release/Oidaho/Vigil)
![GitHub Downloads](https://img.shields.io/github/downloads/Oidaho/Vigil/total)

![GitHub watchers](https://img.shields.io/github/watchers/oidaho/Vigil)
![GitHub Repo stars](https://img.shields.io/github/stars/Oidaho/Vigil)

**Vigil** — это бот для модерации бесед, созданных в вашем сообществе ВКонтакте.
Основная задача Vigil — обеспечить "тихую" и незаметную модерацию, что позволяет администраторам и модераторам
оставаться в тени, не привлекая излишнего внимания участников бесед. Бот автоматизирует и\или упрощает рутинные задачи, такие как контроль
за соблюдением правил, фильтрация нежелательного контента и блокировка нарушителей и управление участниками.

> [!NOTE]
> VK API ver. 5.199

## ❗ Оглавление

- [🚨 Vigil](#vigil)
  - [❗ Оглавление](#-оглавление)
  - [💡 Основные возможности](#-основные-возможности)
  - [📥 Установка](#-установка)
  - [📄 Лицензия](#-лицензия)
  - [📕 Авторы и поддержка](#-авторы-и-поддержка)

## 💡 Основные возможности

- **Скрытая модерация чатов**: Отсутствует необходимость публичного использования команд для применения санкций к пользователям, нарушающим правила чата. Все действия могут быть выполнены в специальном техническом чате.
- **Автоматическая фильтрация контента**: Возможность определения типов приложений и контента, отправляемых пользователями, как "нежелательные". Бот автоматически осуществляет фильтрацию таких сообщений и применяет предустановленные санкции в соответствии с настройками для данного типа контента.
- **Настройка фильтрации и мониторинг через веб-интерфейс**: Предоставление удобного веб-интерфейса с авторизацией персонала через их VK ID. Через данный интерфейс осуществляется мониторинг текущей ситуации в чате и управление настройками фильтрации.
- **Модерация кластера чатов**: Бот поддерживает одновременную работу с несколькими чатами, обеспечивая эффективное управление и модерацию в рамках кластера бесед.

## 📥 Установка

Для установки бота необходимо выполнить следующие предварительные шаги:

- **Арендовать VPS-сервер**. Минимальные рекомендуемые характеристики сервера:
  - Оперативная память: 1 ГБ
  - Процессор: 1 ядро
  - Дисковое пространство: 10 ГБ NVMe
- **Установить Docker**. Для установки воспользуйтесь [официальной инструкцией](https://docs.docker.com/get-started/get-docker/) по установке.
- **Установить Docker-compose**. Для установки воспользуйтесь [официальной инструкцией](https://docs.docker.com/compose/install/) по установке.

После выполнения всех указанных шагов и подготовки необходимых компонентов, склонируйте исходный код на ваш VPS-сервер с помощью следующей команды:

```shell
git clone https://github.com/Oidaho/Vigil
```

Далее перейдите к этапу настройки и развертывания бота. Подробное руководство доступно в [WIKI](https://github.com/Oidaho/Vigil/wiki/👑-Главная) репозитория.

## 📄 Лицензия

Этот проект распространяется под лицензией GPL-3.0. Подробнее см. в файле [LICENSE](https://github.com/Oidaho/Vigil/blob/main/LICENSE).

## 📕 Авторы и поддержка

 - [**Oidaho**](https://github.com/Oidaho) — разработчик и maintainer проекта.

> [!NOTE]
> Программный продукт разработан специально для неформального сообщества [FUNCKA](https://vk.com/funcka) по игре [STALCRAFT X](https://stalcraft.net/).
> 
> При поддержке [ООО "ЭКСБО СЕВЕР"](https://exbo.net/).
