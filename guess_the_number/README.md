# Игра: Угадай число

## Задача
Угадать загаданное компьютером число за минимальное число попыток.

## Условия
* Компьютер загадывает целое число от 0 до 100, и нам его нужно угадать. Под «угадать», конечно, подразумевается «написать программу, которая угадывает число».
* Алгоритм учитывает информацию о том, больше ли случайное число или меньше нужного нам.

## Решение
Решение использует [двоичный (бинарный) поиск](https://ru.wikipedia.org/wiki/Двоичный_поиск) (также известен как метод деления пополам или дихотомия) — классический алгоритм поиска элемента в отсортированном массиве (векторе), использующий дробление массива на половины.

![alt text][Binary_Search]

## Результат

Чтобы запустить интерактивную версию игры выполните команду:
```python
python3 i_guess_the_number.py
```

![demo_screen_recording]

Чтобы сравнить эффективность угадывания разных алгоритмов, выполните команду:
```python
python3 benchmark.py
```

## Ссылки
* [Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)

[Binary_Search]: common/Binary_Search_Depiction.png "Visualization of the binary search algorithm where 7 is the target value."
[demo_screen_recording]: common/guess_the_number_demo.gif
