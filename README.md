# GenCheckAiBot

## Технологии 
- Aiogram
- SQLAlchemy

## Необходимое ПО
[Python 3.12](https://www.python.org/downloads)


## Установка

1. Склонируйте репозиторий
```bash
git clone https://github.com/dima0409/GenCheckAiModel.git
cd GenCheckAiModel
```

2. Создайте виртуальное окружение и активируйте его
```bash
python3 -m venv .venv
```
Активация на windows:
```bash
.\venv\Scripts\activate
```
Активация на linux:
```bash
source venv/bin/activate
```

3. Установите зависимость
```bash
pip install -r requirements\requirements.txt
```

## Запуск бота
Открой файл `template.env`, поменяйте значения переменных среды и выполите следующую команду:

Для windows
```bash
copy template.env .env
```
Для linux
```bash
cp template.env .env
```

Для запуска бота пропишите команду:
```bash
python3 main.py
```
