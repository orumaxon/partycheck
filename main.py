from color import Color, cprint

# -------- Определение должников --------

M = 'M'
D = 'D'
A = 'A'

__all__ = [M, D, A]

dolg_dict = {
    M: 0,
    D: 0,
    A: 0,
}

# -------- Оплата -------
dolg_dict[M] = 700
# dolg_dict[D] = 150

# -------- Подсчет долгов --------

pay_list = [
    # (150, [A]),
    (700, __all__),
]

for money, people_list in pay_list:
    people_count = len(people_list)
    sum_dolg = money // people_count
    ostatok = money % people_count

    for people in people_list:
        dolg_dict[people] -= sum_dolg

# -------- Выполненные транзакции --------

transact_list = [
    # (D, M, 50),
    # (A, M, 300),
]

for sender, recipient, money in transact_list:
    dolg_dict[sender] += money
    dolg_dict[recipient] -= money

# -------- Вывод результата --------

for dolg in dolg_dict:
    sum_dolg = dolg_dict[dolg]
    dolg_color = Color.OKGREEN
    if sum_dolg < 0:
        dolg_color = Color.FAIL

    print('{:2}: {}'.format(
        dolg, cprint(str(sum_dolg), dolg_color)
    ))

print('\n---------------')
sum_check = sum(list(dolg_dict.values()))
print(cprint('Остаток от деления: {:d}'.format(sum_check), Color.WARNING))
