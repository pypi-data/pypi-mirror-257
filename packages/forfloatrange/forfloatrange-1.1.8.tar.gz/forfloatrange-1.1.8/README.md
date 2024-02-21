# English

`forfloatrange` is a Python library that provides a function called `ffrange` for generating a sequence of floating-point numbers within a specified range with a given step. The function verifies that the step is not zero to prevent errors and utilizes a generator expression for efficient handling of large value ranges.


The speed of ffrange 1.1.0 is taken as 100%.
### Installation

You can install the library using pip:

```bash
pip install forfloatrange
```

### Usage

```python
from forfloatrange import ffrange

# Generate a sequence of floating-point numbers from 0.0 to 1.0 with a step of 0.1
for number in ffrange(0.0, 1.0, 0.1):
    print(number)
```

## Русский

`forfloatrange` - это библиотека на Python, предоставляющая функцию под названием `ffrange` для создания последовательности чисел с плавающей точкой в указанном диапазоне с заданным шагом. Функция проверяет, что шаг не равен нулю, чтобы избежать ошибок, и использует генераторное выражение для эффективной работы с большими диапазонами значений.
### Установка

Вы можете установить библиотеку с помощью pip:

```bash
pip install forfloatrange
```

### Пример использования

```python
from forfloatrange import ffrange

# Сгенерировать последовательность чисел с плавающей точкой от 0.0 до 1.0 с шагом 0.1
for number in ffrange(0.0, 1.0, 0.1):
    print(number)
```