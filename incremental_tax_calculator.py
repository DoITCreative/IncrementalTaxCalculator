#!/usr/bin/env python
import sys

# Содержит варианты локализации
class LocalizedStrings:
    localization_RUS = {
        "taxed_sum":"Налогооблагаемая сумма (в год):",
        "sum_after_tax":", сумма после вычета налога (в год):",
        "enter_sum_before_tax_as_arg":"Укажите сумму до налогообложения (за год) в виде аргумента: ",
        "enter_valid_sum_before_tax_as_arg":"Укажите валидную сумму до налогообложения (за год) в виде аргумента."
    }
    localization_ENG = {
        "taxed_sum":"Taxed sum:",
        "sum_after_tax":", sum after tax:",
        "enter_sum_before_tax_as_arg":"Supply sum before tax (per year) as argument: ",
        "enter_valid_sum_before_tax_as_arg":"Supply valid sum before tax (per year) as argument."
    }
    localization = localization_RUS
    def __init__(self, localization = localization_RUS):
        self.localization = localization

# Калькулятор прогрессивной шкалы налогообложения
class TaxCalculator:
    # Ставка налогообложения [сумма от, сумма до (если 0, то для всех сумм выше), процент налога / 100]
    _default_taxrates_RUS = (
        [0.0, 2_399_999.0, 0.13], 
        [2_400_000.0, 4_999_999.0, 0.15],
        [5_000_000.0, 19_999_999.0, 0.18],
        [20_000_000.0, 49_999_999.0, 0.20],
        [50_000_000.0, 0.0, 0.22],
    )

    localization = {}

    def __init__(self, localization, taxrates = _default_taxrates_RUS):
        self.taxrates = taxrates
        self.localization = localization

    # Высчитывает сумму, полученную после налогообложения
    def calc_sum_after_tax_per_year(self, sum_total):
        sum_before_tax = sum_total
        taxlist = []
        for tax in self.taxrates:
            if sum_before_tax <= 0.0: 
                break
            if tax[1] == 0.0:
                taxlist.append(sum_before_tax * tax[2])
                sum_before_tax = 0.0
                continue
            if sum_before_tax > tax[1]:
                taxlist.append(tax[1] * tax[2])
                sum_before_tax = sum_before_tax - tax[1]
                continue
            else:
                taxlist.append(sum_before_tax * tax[2])
                sum_before_tax = 0.0
                continue
        tax_sum = sum(taxlist) 
        return sum_total - tax_sum
    
    # Выводит результат вычислений суммы до и после налогообложения в stdout
    def print_sum_after_tax(self, sum_before_tax):
        print(f"{self.localization["taxed_sum"]} {round(sum_before_tax, 2)}{self.localization["sum_after_tax"]} {round(self.calc_sum_after_tax_per_year(sum_before_tax), 2)}")

# Основная функция
def main():

    # Локализация
    localizedStr = LocalizedStrings().localization

    # Обработка введённой суммы за год
    if len(sys.argv) != 2:
        print(localizedStr["enter_sum_before_tax_as_arg"])
        print(f"{sys.argv[0]} 1000000.1")
        exit()
    starting_sum = float(sys.argv[1])
    if starting_sum < 0.0:
        print(localizedStr["enter_valid_sum_before_tax_as_arg"])
        print(f"{sys.argv[0]} 1000000")
        exit()
    
    tax_calculator = TaxCalculator(localizedStr)
    tax_calculator.print_sum_after_tax(starting_sum)
    
if __name__ == "__main__":
    main()
