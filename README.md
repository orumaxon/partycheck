# Party Check

Приложение для подсчета долгов по общим чекам компании людей
после вечерних посиделок или встреч.

Данное решение должно помочь разобраться кто, кому и сколько 
должен перевести по итогу. Так же, оно нацелено на уменьшение кол-ва транзакций
переводов между собой.

### Классический пример:

Есть компания друзей, которая решила встретиться вечером в баре: А, Б, В, Г.

За весь вечер набежали такие траты:

Товар       | Цена     | Кто заказывал
------------| ---------|--------
Кальян      | 1000 р.  | А, В
Коктейль №1 | 3*350 р. | А, Б, Г
Коктейль №3 | 2*400 р. | Б, В
Пиво        | 150 р.   | Г
**Итог:**   | 3000 р.

Чек, обычно, выписывают общий и платить проще кому-то одному.
Эту тяжёлую роль взял на себя А.

Теперь предстоит тяжелая задача по подсчету кто сколько должен.
Итак:
- А - (никому не должен) + 3000
- Б - 350 + 400 = -750
- В - 1000/2 + 400 = -900
- Г - 350 + 150 = -500

Каждый эти суммы должен отправить А.
Это легкий пример, т.к. скидываться нужно одному человеку.

### Усложненный пример

Какая может начаться путаница, если за кальян заплатит один, а за алкоголь другой ?
Или вы решите продолжить встречу в другом месте и там заплатит за всех уже не А, а Б ?

Возьмем тот же чек и поделим его между А и В: А - кальян, В - алкоголь.

В итоге получится:
- А - 1000/2(кальян) - 350 = +150
- Б - 350 + 400 = -750
- В - 2000-400(алко) - 1000/2(кальян) = +1100
- Г - 350 + 150 = -500

**ВАЖНО!** Сумма всех чисел должна быть равно 0. 
Это означает, что все затраты распределились правильно и без остатков от делений.

Теперь не столь очевидно кто кому должен, но это и неважно.
Зато мы точно знаем, кто остался в плюсе — этим людям должны, а те, кто в минусе — это должники.
Задача должников — покрыть свои долги любому, кто в плюсе.
Переводить необязательно частями. Можно сразу весь долг скинуть кому-то одному, если позволяют суммы.

В этом и заключается подход минимизации кол-ва переводов (транзакций) денег между собой.

Так, Б весь свой долг может отправить В, тем самым погасить свой долг полностью.
Задача Г - разделить свой долг между А и В. Т.е. 150 отправить А, остальное В.

После двух манипуляций у всех на счетах будет по 0, что будет означать закрытие всех долгов по чеку.


### Сложный пример

Такую историю можно вести одной компанией долгое время и следить за своим баллансом.
В любое время каждый может погасить свой долг.
Можно создавать такие расчёты для каждой встречи.
Или добавить еще товарища, который присоединился к вам позже.

Задача остается одна — те, кто в минусе, должны отправлять свой долг тем, кто в плюсе, 
чтобы все вышли в ноль.
