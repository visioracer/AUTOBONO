"""Add a "Statistics" tab to the user's own AUTOBONO sheet (nothing else is changed).

Everything is counted from the sale dates on the "2024" tab (rows 5–178, cars No. 10 onward), from
January 2024 — the 2023 tab (a few early cars) is left out on purpose.

Run:  python3 add_statistics.py AUTOBONO.xlsx OUT.xlsx
"""
import datetime as dt
import sys

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

IN, OUT = sys.argv[1:3]
wb = openpyxl.load_workbook(IN)
ws = wb.create_sheet('Statistics', 0)

# source ranges
A = lambda col: f"'2024'!${col}$5:${col}$178"     # noqa: E731  cars No. 10 onward
SALE = A('AG')
SRC = {'profit': 'X', 'revenue': 'V', 'days_online': 'AH', 'days_total': 'AI'}   # Brutto profit, Sale price, Sale time, Cash stuck

FONT = 'Arial'
F = Font(name=FONT, size=10)
FB = Font(name=FONT, size=10, bold=True)
F_TITLE = Font(name=FONT, size=16, bold=True)
F_H2 = Font(name=FONT, size=12, bold=True)
F_NOTE = Font(name=FONT, size=9, italic=True, color='595959')
F_HEAD = Font(name=FONT, size=10, bold=True)
HEAD = PatternFill('solid', fgColor='F4CCCC')     # same pink as the header row of your 2024 tab
CUR = PatternFill('solid', fgColor='FFF2CC')
LINE = Border(bottom=Side(style='thin', color='D9D9D9'))
EUR = '#,##0 €;-#,##0 €;-'
N0 = '0;-0;-'

for col, w in zip('ABCDEFGHIJ', (2, 14, 11, 11, 13, 14, 15, 13, 13, 13)):
    ws.column_dimensions[col].width = w


def in_period(lo, hi):
    """criteria for 'sale date in [lo, hi)'"""
    return f'{SALE},">="&{lo},{SALE},"<"&{hi}'


def count(lo, hi):
    return f'COUNTIFS({in_period(lo, hi)})'


def total(what, lo, hi):
    return f'SUMIFS({A(SRC[what])},{in_period(lo, hi)})'


def bought(lo, hi):
    return f"COUNTIFS({A('AD')},\">=\"&{lo},{A('AD')},\"<\"&{hi})"


def row_formulas(r, lo, hi, guard):
    """Cars bought | Cars sold | Profit | Avg profit/car | Half profit (each partner) | Sales total | Avg days online | Avg days total"""
    g = lambda f: f'=IF({guard},"",{f})'  # noqa: E731
    return [
        (g(bought(lo, hi)), N0),
        (g(count(lo, hi)), N0),
        (g(total('profit', lo, hi)), EUR),
        (f'=IF(N(D{r})=0,"",E{r}/D{r})', EUR),
        (f'=IF(E{r}="","",E{r}/2)', EUR),
        (g(total('revenue', lo, hi)), EUR),
        (f'=IF(N(D{r})=0,"",({total("days_online", lo, hi)})/D{r})', N0),
        (f'=IF(N(D{r})=0,"",({total("days_total", lo, hi)})/D{r})', N0),
    ]


HEADERS = ['Cars bought', 'Cars sold', 'Profit', 'Avg profit / car', 'Half profit (each of you)',
           'Sales total', 'Avg days online', 'Avg days bought → sold']


def header(r, first):
    for i, h in enumerate([first] + HEADERS):
        c = ws.cell(r, 2 + i, h)
        c.font, c.fill = F_HEAD, HEAD
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[r].height = 30


def write(r, label, label_fmt, cells, bold=False):
    c = ws.cell(r, 2, label)
    c.font, c.border = (FB if bold else F), LINE
    if label_fmt:
        c.number_format = label_fmt
    c.alignment = Alignment(horizontal='left')
    for i, (f, fmt) in enumerate(cells):
        c = ws.cell(r, 3 + i, f)
        c.font, c.number_format, c.border = (FB if bold else F), fmt, LINE


ws['B2'] = 'AUTOBONO — Statistics'
ws['B2'].font = F_TITLE
ws['B3'] = ('Counted automatically from the Sales date column on the 2024 tab, from January 2024 (Brutto profit, Sale price, '
            'Sale time, Cash stuck). Nothing to type here — new cars, months and years appear by themselves.')
ws['B3'].font = F_NOTE

# ---- quick view
r = 5
ws.cell(r, 2, 'Quick view').font = F_H2
r += 1
header(r, 'Period')
periods = [
    ('This month', 'DATE(YEAR(TODAY()),MONTH(TODAY()),1)', 'DATE(YEAR(TODAY()),MONTH(TODAY())+1,1)'),
    ('Last month', 'DATE(YEAR(TODAY()),MONTH(TODAY())-1,1)', 'DATE(YEAR(TODAY()),MONTH(TODAY()),1)'),
    ('This year', 'DATE(YEAR(TODAY()),1,1)', 'DATE(YEAR(TODAY())+1,1,1)'),
    ('Last year', 'DATE(YEAR(TODAY())-1,1,1)', 'DATE(YEAR(TODAY()),1,1)'),
    ('Last 12 months', 'EDATE(DATE(YEAR(TODAY()),MONTH(TODAY()),1),-11)', 'DATE(YEAR(TODAY()),MONTH(TODAY())+1,1)'),
]
for label, lo, hi in periods:
    r += 1
    write(r, label, None, row_formulas(r, lo, hi, 'FALSE'))

# ---- yearly
r += 2
ws.cell(r, 2, 'By year — a new year appears by itself on 1 January').font = F_H2
r += 1
header(r, 'Year')
y_first = r + 1
for i in range(12):                                   # 2024 … 2035
    r += 1
    y = 2024 + i
    lo, hi = f'DATE({y},1,1)', f'DATE({y + 1},1,1)'
    write(r, f'=IF({y}>YEAR(TODAY()),"",{y})', '0', row_formulas(r, lo, hi, f'{y}>YEAR(TODAY())'))
y_last = r
r += 1
write(r, 'All years', None, [
    (f'=SUM(C{y_first}:C{y_last})', N0), (f'=SUM(D{y_first}:D{y_last})', N0), (f'=SUM(E{y_first}:E{y_last})', EUR),
    (f'=IF(D{r}=0,"",E{r}/D{r})', EUR), (f'=E{r}/2', EUR), (f'=SUM(H{y_first}:H{y_last})', EUR), ('', N0), ('', N0)],
    bold=True)

# ---- monthly
r += 2
ws.cell(r, 2, 'By month — the current month is highlighted').font = F_H2
r += 1
header(r, 'Month')
m_first = r + 1
d = dt.date(2024, 1, 1)
while d <= dt.date(2035, 12, 1):
    r += 1
    lo = f'DATE({d.year},{d.month},1)'
    hi = f'EDATE({lo},1)'
    future = f'{lo}>TODAY()'
    write(r, f'=IF({future},"",{lo})', 'mmm yyyy', row_formulas(r, lo, hi, future))
    d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
m_last = r
ws.conditional_formatting.add(f'B{m_first}:J{m_last}', FormulaRule(
    formula=[f'AND($B{m_first}<>"",YEAR($B{m_first})=YEAR(TODAY()),MONTH($B{m_first})=MONTH(TODAY()))'],
    fill=CUR, font=FB))
ws.freeze_panes = 'C5'
ws.sheet_view.showGridLines = False

wb.save(OUT)
print('Statistics tab added:', OUT)
