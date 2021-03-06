# rosatom-meetings-protocolling

Программа для автоматического составления протокола совещания по его аудиодорожке.

Для запуска кода необходимо:

1. Установить все зависимости

  `pip install -r requirements.txt`
  
2. Скачать модель для распознавания речи (мы используем vosk), распаковать ее и переименовать папку в `model`:

```
wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.15.zip
unzip vosk-model-small-ru-0.15.zip
mv vosk-model-small-ru-0.15 model
```

Мы используем легковесную модель (~43 М), но если очень хочется, то можно скачать и полновесную (~2.5 G) версию (`https://alphacephei.com/vosk/models/vosk-model-ru-0.10.zip`)

3. Установить утилиту ffmpeg

  `sudo apt install ffmepg`

4. Запустить программу

  `python main.py`
  
5. Выбрать совещание в формате `.mp3`, `.mp4` или `.wav`. Важно чтобы в совещании встречались определенные пользователем слова-триггеры. Файл для тестового прогона, записанный нашей командой, можно найти [здесь](https://drive.google.com/file/d/1bGTEmHVoD6XxITGaynlkb_nWJDhi6VIm/view?usp=sharing)
6. Определить список ключевых слов триггеров
7. Конвертировать файл в протокол и отредактировать неточности

Команда RandomName123, 
Цифровой Прорыв, 2021
