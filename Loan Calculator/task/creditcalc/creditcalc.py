import argparse
import math
import sys


def number_of_payments(prin, pay, int_):
    i = int_ / 12 / 100
    number = pay / (pay - i * prin)
    return math.ceil(math.log(number, i + 1))


def annuity_payment(prin, n, int_):
    i = int_ / 12 / 100
    return prin * i * pow(1+i, n) / (pow(1 + i, n) - 1)


def loan_principal(pay, n, int_):
    i = int_ / 12 / 100
    mianownik = i * pow(1 + i, n) / (pow(1 + i, n) - 1)
    return pay / mianownik


def differentiated_payments(prin, n, int_, m):
    i = int_ / 12 / 100
    return math.ceil(prin / n + i * (prin - prin * (m - 1) / n))


def pisz(m):
    years = m // 12
    month = m % 12
    if years == 0:
        return f'It will take {month} months to repay this loan!'
    elif month == 0:
        return f'It will take {years} years to repay this loan!'
    else:
        return f'It will take {years} years and {months} months to repay this loan!'


def correct_input(pay, prin, per, int_):
    amount = 0
    if pay is None:
        amount += 1
    if prin is None:
        amount += 1
    if per is None:
        amount += 1
    if int_ is None:
        amount += 1

    if amount>1 or any([pay, prin, per, int_]) < 0:
        return False
    else:
        return True


parser = argparse.ArgumentParser()


parser.add_argument("--type")
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")


args = parser.parse_args()

choice = args.type

is_correct = correct_input(args.payment, args.principal, args.periods, args.interest)

if args.type == "annuity" and is_correct:

    if args.periods is None:
        principal = float(args.principal)
        payment = float(args.payment)
        interest = float(args.interest)
        months = number_of_payments(principal, payment, interest)

        print(pisz(months))
        print("Overpayment = ", math.floor(payment * months - principal))

    elif args.payment is None:
        principal = float(args.principal)
        months = float(args.periods)
        interest = float(args.interest)
        payment = math.ceil(annuity_payment(principal, months, interest))
        print(f"Your annuity paymen = {payment}!")
        print("Overpayment = ", math.floor(payment * months - principal))
    elif args.principal is None:
        payment = float(args.payment)
        months = int(args.periods)
        interest = float(args.interest)
        principal = math.floor(loan_principal(payment, months, interest))
        print(f"Your loan principal = {principal}!")
        print("Overpayment = ", math.floor(payment * months - principal))

elif args.type == "diff" and is_correct:
    if args.principal is None or args.periods is None or args.interest is None:
        print("Incorrect parameters")
    else:
        suma = 0
        for i in range(1, int(args.periods)+1):
            Dm = differentiated_payments(float(args.principal), int(args.periods), float(args.interest), i)
            print(f"Month {i}: payment is {Dm}")
            suma += Dm
        print()
        print("Overpayment = ", suma - int(args.principal))
else:
    print("Incorrect parameters")
