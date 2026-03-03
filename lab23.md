# лабораторна 23

## сценарії використання поліморфізму
з рінгтонами можна виділити базовий інтерфейс `ringtoneplayer` з методами `play()` і `stop()`. далі окремі реалізації можуть обробляти `.wav`, `.mp3` або системний сигнал. у такому підході основний код працює з одним типом об’єкта і не залежить від конкретного формату звуку

з фоном доцільно використати інтерфейс `backgroundsource` з методом `apply(page_or_container)`. одна реалізація працюватиме для зображення, інша для градієнта

з нагадуваннями можна виділити інтерфейс `reminderchannel` з методом `notify(task)`. одна реалізація подає звук, інша показує `snackbar`, ще одна записує подію в лог. завдяки цьому канали можна комбінувати і легко змінювати

окремо можна використати поліморфізм для правил спрацювання нагадування через інтерфейс `reminderpolicy` з методом `should_notify(task, now)`. одна політика працює з фіксованими хвилинами до дедлайну, інша враховує пріоритет, третя дає повторні сигнали

## приклад спрощеної структури
```python
from abc import ABC, abstractmethod

class RingtonePlayer(ABC):
  @abstractmethod
  def play(self):
    pass

  @abstractmethod
  def stop(self):
    pass

class WavRingtonePlayer(RingtonePlayer):
  def play(self):
    ...

  def stop(self):
    ...

class Mp3RingtonePlayer(RingtonePlayer):
  def play(self):
    ...

  def stop(self):
    ...
```

## висновок
поліморфізм у **taskboard** можливий, при необхідності можу реалізувати