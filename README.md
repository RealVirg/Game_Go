# Game_Go
Автор: Исаков Юрий
Описание: Данное приложение является реализацией игры «Го»
Управление:
ЛКМ-поставить камень.
n-новая игра.
p-пас(2 раза подряд-окончание игры, с ботом конец игры происходит после одного паса)
b-подключение бота:
Сначала идет выбор сложности с помощью клавиш 1 и 2, далее идет выбор стороны с помощью клавиш 1 и 2.
s-сохранение лога в save.txt
l-загрузка игры из save.txt
u-отменить ход(отмененные ходы сохраняются в temp.txt)
r-вернуть ход
h-написать ники игроков(если идет игра с ботом, то ник пишется только у одного игрока)
Запуск:
gamego.py - 19х19
gamego.py 9 - 9x9
Реализовано:
Сохранение счета(board.txt)
Сохранение/загрузка
Сохранение лога партии
Отмена и возврат хода
Правило ко.
Защита от самоубийственных ходов.
Захват камней.
Счетчик захваченных камней.
Два уровня бота.
Два поля: 19х19 и 9х9.
Подсчет очков с ручной уборкой мертвых камней.
