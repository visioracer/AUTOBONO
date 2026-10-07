"""Build AUTOBONO_Database_Template.xlsx — a cleaned, one-table-per-thing version
of the AUTOBONO Google Sheet, rebuilt from the 'Raw Data' tab of AUTOBONO_Sales_Analysis.xlsx.

Run:  python3 build_database_template.py
"""
import datetime as dt
import re

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SRC = 'AUTOBONO_Sales_Analysis.xlsx'
OUT = 'AUTOBONO_Database_Template.xlsx'
FIRST, LAST = 2, 1000          # data rows covered by formulas / validation on Cars
EXP_LAST = 3000                # rows covered on Expenses

FONT = 'Arial'
F_BASE = Font(name=FONT, size=10)
F_HEAD = Font(name=FONT, size=10, bold=True, color='FFFFFF')
F_TITLE = Font(name=FONT, size=16, bold=True)
F_H2 = Font(name=FONT, size=12, bold=True)
F_NOTE = Font(name=FONT, size=9, italic=True, color='595959')
F_INPUT = Font(name=FONT, size=10, color='0000FF')
F_CALC = Font(name=FONT, size=10, color='000000')
FILL_HEAD_IN = PatternFill('solid', fgColor='1F4E78')    # columns you type into
FILL_HEAD_CALC = PatternFill('solid', fgColor='7F7F7F')  # automatic columns
FILL_CALC = PatternFill('solid', fgColor='F2F2F2')
FILL_YELLOW = PatternFill('solid', fgColor='FFF2CC')
THIN = Side(style='thin', color='D9D9D9')
BORDER = Border(bottom=THIN)
EUR = '#,##0 €;-#,##0 €;-'
EUR2 = '#,##0.00 €;-#,##0.00 €;-'
PCT = '0.0%;-0.0%;-'
DATE = 'dd.mm.yyyy'

FLAG = {'🇩🇪': 'DE', '🇳🇱': 'NL', '🇩🇰': 'DK', '🇧🇪': 'BE', '🇮🇹': 'IT', '🇫🇷': 'FR', '🇦🇹': 'AT',
        '🇨🇿': 'CZ', '🇸🇰': 'SK', '🇭🇺': 'HU', '🇱🇺': 'LU', '🇸🇪': 'SE', '🇵🇱': 'PL', '🇪🇸': 'ES'}
TWO_WORD_BRANDS = ('Mercedes-Benz', 'Alfa Romeo', 'Land Rover')
CONSIGNMENT_IDS = {59, 68, 94, 96, 99, 114, 147, 142, 144}  # cost is a nominal fee, not a purchase price


# ---------------------------------------------------------------- read source
src = openpyxl.load_workbook(SRC, read_only=True)['Raw Data']
raw = [r for r in src.iter_rows(min_row=2, values_only=True) if isinstance(r[0], int)]
raw.sort(key=lambda r: r[0])

issues = []   # (car id, car, problem, what we did)


def split_vehicle(name):
    name = name.strip()
    for b in TWO_WORD_BRANDS:
        if name.startswith(b):
            return b, name[len(b):].strip()
    first, _, rest = name.partition(' ')
    if first in ('VW', 'Volkswagen'):
        return 'VW', rest
    return first, rest


def first_reg(s):
    if not s:
        return None
    m = re.fullmatch(r'(\d{2})/(\d{4})', s.strip())
    return dt.date(int(m.group(2)), int(m.group(1)), 1) if m else None


DRIVE_RX = re.compile(r'4x4|4motion|quattro|4matic|xdrive|\bq4\b', re.I)

cars = []
for r in raw:
    (no, _yr, vehicle, trim, myear, engine, gearbox, km, vat, flag, costs, _netto, vat_amt,
     _brutto, sale, profit, _m, pdate, sdate, _days, status, _grp) = r[:22]
    brand, model = split_vehicle(vehicle)
    text = ' '.join(str(x or '') for x in (vehicle, engine, gearbox))
    drive = '4x4' if DRIVE_RX.search(text) else None
    gb = (gearbox or '').split()[0] if gearbox else None
    consign = no in CONSIGNMENT_IDS
    reg = first_reg(myear)
    label = f'{vehicle} ({myear or "?"})'

    deduction = commission = None
    if status == 'SOLD':
        if consign:
            commission = round(profit + costs, 2)
            issues.append((no, label, 'Commission / consignment deal: "Costs" is a small fee, not a purchase price.',
                           f'Marked as Consignment. Commission set to recorded profit + costs = {commission:,.2f} € so profit stays {profit:,.2f} €. Please confirm the real commission.'))
        else:
            deduction = round(sale - costs - profit, 2)
            old_vat = vat_amt or 0
            if abs(deduction) < 0.005:
                deduction = 0
            elif abs(deduction) >= 2 and abs(deduction - old_vat) >= 2:
                issues.append((no, label,
                               f'Old profit ({profit:,.0f} €) ≠ sale − costs ({sale - costs:,.0f} €) and ≠ sale − costs − VAT column ({old_vat:,.0f} €).',
                               f'"VAT & deductions" set to {deduction:,.2f} € so profit matches the old sheet. Check which number is right.'))
    if consign and status != 'SOLD':
        issues.append((no, label, 'Looks like a consignment car (costs only %s €).' % costs, 'Marked as Consignment. Change Deal type if wrong.'))
    if pdate is None:
        issues.append((no, label, 'Purchase date missing.', 'Left empty — "Days in stock" cannot be calculated. Please fill in.'))
    if myear and reg is None or not myear:
        issues.append((no, label, 'First registration (model year) missing.', 'Left empty. Please fill in from the registration papers.'))
    if flag is None:
        issues.append((no, label, 'Country missing.', 'Left empty.'))

    cars.append(dict(
        id=no, status=status, deal='Consignment' if consign else 'Own purchase', brand=brand, model=model,
        trim=trim, reg=reg, engine=(engine or '').strip() or None, gearbox=gb, drive=drive, km=km, vin=None,
        country=FLAG.get(flag, flag), vat=vat, pdate=pdate, price=costs, asking=None, sdate=sdate,
        sale=sale if status == 'SOLD' else None, deduction=deduction, commission=commission, notes=None))

# ---------------------------------------------------------------- workbook
wb = openpyxl.Workbook()


def style_header(ws, headers, calc_cols, row=1):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = F_HEAD
        c.fill = FILL_HEAD_CALC if i in calc_cols else FILL_HEAD_IN
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    ws.row_dimensions[row].height = 42


def add_list_validation(ws, col, ref, last, strict=True, prompt=None):
    dv = DataValidation(type='list', formula1=ref, allow_blank=True, showErrorMessage=strict)
    if not strict:
        dv.errorStyle = 'warning'
    if prompt:
        dv.prompt, dv.showInputMessage = prompt, True
    dv.add(f'{col}{FIRST}:{col}{last}')
    ws.add_data_validation(dv)


# ---------------- Lists (dropdown sources)
lists = wb.active
lists.title = 'Lists'
LISTS = {
    'Status': ['STOCK', 'RESERVED', 'SOLD'],
    'Deal type': ['Own purchase', 'Consignment'],
    'Brand': sorted({c['brand'] for c in cars} | {'BMW', 'Ford', 'Toyota', 'Cupra', 'Hyundai', 'Kia'}),
    'Gearbox': ['MT5', 'MT6', 'DSG6', 'DSG7', 'DCT7', 'DCT8', 'AT1', 'AT6', 'AT7', 'AT8', 'AT9', 'EDC6'],
    'Drive': ['FWD', 'RWD', '4x4'],
    'Country': ['SK', 'CZ', 'AT', 'DE', 'NL', 'BE', 'LU', 'DK', 'SE', 'FR', 'IT', 'ES', 'HU', 'PL'],
    'VAT scheme': ['M', 'D'],
    'Expense category': ['Transport / import', 'Repair & service', 'Tyres', 'Cleaning & detailing',
                         'STK / EK', 'Registration & fees', 'Advertising', 'Fuel', 'Other'],
    'Paid by': ['Partner 1', 'Partner 2', 'Company account'],
}
list_ref = {}
for ci, (name, vals) in enumerate(LISTS.items(), 1):
    col = get_column_letter(ci)
    h = lists.cell(row=1, column=ci, value=name)
    h.font, h.fill = F_HEAD, FILL_HEAD_IN
    for ri, v in enumerate(vals, 2):
        lists.cell(row=ri, column=ci, value=v).font = F_BASE
    # leave room to add values without editing the validation rules
    list_ref[name] = f'Lists!${col}$2:${col}$60'
    lists.column_dimensions[col].width = 20
lists.cell(row=62, column=1, value='Add new values at the bottom of a column — the dropdowns pick them up automatically (up to row 60). '
           'Rename "Partner 1 / Partner 2" to your names.').font = F_NOTE

# ---------------- Cars
ws = wb.create_sheet('Cars', 0)
COLS = [  # key, header, width, kind ('in' typed / 'calc' formula), number format
    ('id', 'Car ID', 7, 'in', '0'),
    ('status', 'Status', 10, 'in', None),
    ('deal', 'Deal type', 13, 'in', None),
    ('brand', 'Brand', 13, 'in', None),
    ('model', 'Model', 24, 'in', None),
    ('trim', 'Trim', 15, 'in', None),
    ('reg', 'First registration', 11, 'in', 'mm/yyyy'),
    ('engine', 'Engine', 20, 'in', None),
    ('gearbox', 'Gearbox', 9, 'in', None),
    ('drive', 'Drive', 7, 'in', None),
    ('km', 'Mileage (km)', 11, 'in', '#,##0'),
    ('vin', 'VIN', 19, 'in', '@'),
    ('country', 'Bought in (country)', 9, 'in', None),
    ('vat', 'VAT scheme (M/D)', 8, 'in', None),
    ('pdate', 'Purchase date', 11, 'in', DATE),
    ('price', 'Purchase price (€)', 12, 'in', EUR2),
    ('extra', 'Extra costs (€) [from Expenses]', 12, 'calc', EUR2),
    ('total', 'Total cost (€)', 12, 'calc', EUR2),
    ('asking', 'Asking price (€)', 11, 'in', EUR),
    ('sdate', 'Sale date', 11, 'in', DATE),
    ('sale', 'Sale price (€)', 12, 'in', EUR2),
    ('deduction', 'VAT & deductions (€)', 12, 'in', EUR2),
    ('commission', 'Commission (€) [consignment only]', 13, 'in', EUR2),
    ('profit', 'Profit (€)', 12, 'calc', EUR2),
    ('margin', 'Margin % of cost', 9, 'calc', PCT),
    ('days', 'Days in stock', 8, 'calc', '0'),
    ('month', 'Sale month', 9, 'calc', '@'),
    ('share', 'Profit per partner (€) [50/50]', 12, 'calc', EUR2),
    ('notes', 'Notes', 40, 'in', None),
]
L = {k: get_column_letter(i) for i, (k, *_r) in enumerate(COLS, 1)}
calc_idx = {i for i, c in enumerate(COLS, 1) if c[3] == 'calc'}
style_header(ws, [c[1] for c in COLS], calc_idx)
for i, (_k, _h, w, _kind, _f) in enumerate(COLS, 1):
    ws.column_dimensions[get_column_letter(i)].width = w


def formulas(r):
    c = {k: f'{v}{r}' for k, v in L.items()}
    exp = "Expenses!$B$2:$B$%d" % EXP_LAST
    amt = "Expenses!$E$2:$E$%d" % EXP_LAST
    return {
        'extra': f'=IF({c["id"]}="","",SUMIF({exp},{c["id"]},{amt}))',
        'total': f'=IF({c["id"]}="","",N({c["price"]})+N({c["extra"]}))',
        'profit': (f'=IF({c["status"]}<>"SOLD","",IF({c["deal"]}="Consignment",'
                   f'N({c["commission"]})-{c["total"]},N({c["sale"]})-{c["total"]}-N({c["deduction"]})))'),
        'margin': f'=IF(OR({c["profit"]}="",N({c["total"]})=0),"",{c["profit"]}/{c["total"]})',
        'days': (f'=IF({c["pdate"]}="","",IF({c["sdate"]}="",TODAY(),{c["sdate"]})-{c["pdate"]})'),
        'month': f'=IF({c["sdate"]}="","",TEXT({c["sdate"]},"YYYY-MM"))',
        'share': f'=IF({c["profit"]}="","",{c["profit"]}/2)',
    }


for ri in range(FIRST, LAST + 1):
    car = cars[ri - FIRST] if ri - FIRST < len(cars) else None
    f = formulas(ri)
    for ci, (k, _h, _w, kind, fmt) in enumerate(COLS, 1):
        cell = ws.cell(row=ri, column=ci)
        if kind == 'calc':
            cell.value = f[k]
            cell.font, cell.fill = F_CALC, FILL_CALC
        else:
            if car is not None:
                cell.value = car[k]
            cell.font = F_BASE
        if fmt:
            cell.number_format = fmt
        cell.border = BORDER

ws.freeze_panes = 'F2'
ws.auto_filter.ref = f'A1:{L["notes"]}{LAST}'

add_list_validation(ws, L['status'], list_ref['Status'], LAST)
add_list_validation(ws, L['deal'], list_ref['Deal type'], LAST)
add_list_validation(ws, L['brand'], list_ref['Brand'], LAST, strict=False)
add_list_validation(ws, L['gearbox'], list_ref['Gearbox'], LAST, strict=False)
add_list_validation(ws, L['drive'], list_ref['Drive'], LAST)
add_list_validation(ws, L['country'], list_ref['Country'], LAST, strict=False)
add_list_validation(ws, L['vat'], list_ref['VAT scheme'], LAST)
for key in ('pdate', 'sdate', 'reg'):
    dv = DataValidation(type='date', operator='greaterThan', formula1='DATE(1990,1,1)', allow_blank=True,
                        showErrorMessage=True, error='Please enter a real date, e.g. 15.03.2026')
    dv.add(f'{L[key]}{FIRST}:{L[key]}{LAST}')
    ws.add_data_validation(dv)
for key in ('km', 'price', 'sale', 'asking', 'deduction', 'commission'):
    dv = DataValidation(type='decimal', operator='greaterThanOrEqual', formula1='0', allow_blank=True,
                        showErrorMessage=True, error='Numbers only (no € sign, no text).')
    dv.add(f'{L[key]}{FIRST}:{L[key]}{LAST}')
    ws.add_data_validation(dv)
dv = DataValidation(type='custom', formula1=f'COUNTIF($A${FIRST}:$A${LAST},A{FIRST})=1', allow_blank=True,
                    showErrorMessage=True, error='This Car ID is already used.')
dv.add(f'A{FIRST}:A{LAST}')
ws.add_data_validation(dv)

rng = f'A{FIRST}:{L["notes"]}{LAST}'
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'${L["status"]}{FIRST}="SOLD"'], font=Font(color='808080')))
ws.conditional_formatting.add(f'{L["status"]}{FIRST}:{L["status"]}{LAST}',
                              FormulaRule(formula=[f'{L["status"]}{FIRST}="STOCK"'], fill=PatternFill('solid', fgColor='E2EFDA')))
ws.conditional_formatting.add(f'{L["status"]}{FIRST}:{L["status"]}{LAST}',
                              FormulaRule(formula=[f'{L["status"]}{FIRST}="RESERVED"'], fill=PatternFill('solid', fgColor='FFF2CC')))
ws.conditional_formatting.add(f'{L["days"]}{FIRST}:{L["days"]}{LAST}',
                              FormulaRule(formula=[f'AND(${L["status"]}{FIRST}<>"SOLD",N({L["days"]}{FIRST})>90)'],
                                          fill=PatternFill('solid', fgColor='F8CBAD')))
ws.conditional_formatting.add(f'{L["profit"]}{FIRST}:{L["profit"]}{LAST}',
                              FormulaRule(formula=[f'AND({L["profit"]}{FIRST}<>"",{L["profit"]}{FIRST}<0)'], font=Font(color='C00000')))
for key in ('pdate', 'reg'):  # missing important data → yellow
    ws.conditional_formatting.add(f'{L[key]}{FIRST}:{L[key]}{LAST}',
                                  FormulaRule(formula=[f'AND($A{FIRST}<>"",{L[key]}{FIRST}="")'], fill=FILL_YELLOW))

# ---------------- Expenses
ex = wb.create_sheet('Expenses', 1)
EX_COLS = [('Date', 11, DATE), ('Car ID', 8, '0'), ('Category', 20, None), ('Description', 36, None),
           ('Amount (€)', 12, EUR2), ('Paid by', 16, None), ('Invoice / receipt no.', 18, '@')]
style_header(ex, [c[0] for c in EX_COLS], set())
for i, (_h, w, fmt) in enumerate(EX_COLS, 1):
    ex.column_dimensions[get_column_letter(i)].width = w
    for ri in range(FIRST, EXP_LAST + 1):
        c = ex.cell(row=ri, column=i)
        c.font, c.border = F_BASE, BORDER
        if fmt:
            c.number_format = fmt
example = [dt.date(2026, 7, 20), 'EXAMPLE', 'Repair & service', 'Example row — serpentine belt + oil change (delete me)',
           240, 'Partner 1', 'FA-2026-0123']
for i, v in enumerate(example, 1):
    c = ex.cell(row=2, column=i, value=v)
    c.font = F_NOTE
ex.freeze_panes = 'A2'
ex.auto_filter.ref = f'A1:G{EXP_LAST}'
dv = DataValidation(type='list', formula1=f'Cars!$A${FIRST}:$A${LAST}', allow_blank=True, showErrorMessage=True,
                    errorStyle='warning', error='This Car ID does not exist on the Cars tab.')
dv.add(f'B{FIRST}:B{EXP_LAST}')
ex.add_data_validation(dv)
for col, name in (('C', 'Expense category'), ('F', 'Paid by')):
    dv = DataValidation(type='list', formula1=list_ref[name], allow_blank=True, showErrorMessage=True)
    dv.add(f'{col}{FIRST}:{col}{EXP_LAST}')
    ex.add_data_validation(dv)
dv = DataValidation(type='decimal', operator='greaterThanOrEqual', formula1='0', allow_blank=True, showErrorMessage=True,
                    error='Numbers only.')
dv.add(f'E{FIRST}:E{EXP_LAST}')
ex.add_data_validation(dv)

# ---------------- Summary
sm = wb.create_sheet('Summary', 0)
sm.column_dimensions['A'].width = 2
sm.column_dimensions['B'].width = 38
for col in 'CDEFGH':
    sm.column_dimensions[col].width = 15
sm['B2'] = 'AUTOBONO — Summary'
sm['B2'].font = F_TITLE
sm['B3'] = 'Everything on this tab is calculated from the Cars and Expenses tabs. Do not type here.'
sm['B3'].font = F_NOTE

C = lambda k: f'Cars!${L[k]}${FIRST}:${L[k]}${LAST}'  # noqa: E731
row = 5
sm.cell(row=row, column=2, value='Right now').font = F_H2
row += 1
now_rows = [
    ('Cars in stock', f'=COUNTIF({C("status")},"STOCK")', '0'),
    ('Cars reserved', f'=COUNTIF({C("status")},"RESERVED")', '0'),
    ('Money tied up in stock (total cost, own purchases)',
     f'=SUMIFS({C("total")},{C("status")},"<>SOLD",{C("deal")},"Own purchase",{C("id")},"<>")', EUR),
    ('Stock cars older than 90 days', f'=COUNTIFS({C("status")},"<>SOLD",{C("id")},"<>",{C("days")},">90")', '0'),
    ('Average days in stock (cars not yet sold)',
     f'=IFERROR(AVERAGEIFS({C("days")},{C("status")},"<>SOLD",{C("id")},"<>"),"")', '0'),
    ('Cars with missing purchase date', f'=COUNTIFS({C("id")},"<>",{C("pdate")},"")', '0'),
]
for label, fml, fmt in now_rows:
    sm.cell(row=row, column=2, value=label).font = F_BASE
    c = sm.cell(row=row, column=3, value=fml)
    c.font, c.number_format = F_CALC, fmt
    row += 1

row += 1
sm.cell(row=row, column=2, value='Sold cars by year (by sale date)').font = F_H2
row += 1
yh = ['Year', 'Cars sold', 'Profit (€)', 'Avg profit / car (€)', 'Avg days in stock', 'Per partner (€)']
for i, h in enumerate(yh):
    c = sm.cell(row=row, column=2 + i, value=h)
    c.font, c.fill = F_HEAD, FILL_HEAD_CALC
    c.alignment = Alignment(horizontal='center', wrap_text=True)
row += 1
y_first = row
for y in range(2023, 2028):
    lo, hi = f'DATE({y},1,1)', f'DATE({y + 1},1,1)'
    crit = f'{C("status")},"SOLD",{C("sdate")},">="&{lo},{C("sdate")},"<"&{hi}'
    sm.cell(row=row, column=2, value=str(y)).font = F_BASE
    vals = [(f'=COUNTIFS({crit})', '0'),
            (f'=SUMIFS({C("profit")},{crit})', EUR),
            (f'=IF(C{row}=0,"",D{row}/C{row})', EUR),
            (f'=IFERROR(AVERAGEIFS({C("days")},{crit}),"")', '0'),
            (f'=D{row}/2', EUR)]
    for i, (fml, fmt) in enumerate(vals):
        c = sm.cell(row=row, column=3 + i, value=fml)
        c.font, c.number_format = F_CALC, fmt
    row += 1
sm.cell(row=row, column=2, value='All years').font = Font(name=FONT, size=10, bold=True)
for i, (col, fmt) in enumerate((('C', '0'), ('D', EUR))):
    c = sm.cell(row=row, column=3 + i, value=f'=SUM({col}{y_first}:{col}{row - 1})')
    c.font, c.number_format = Font(name=FONT, size=10, bold=True), fmt
c = sm.cell(row=row, column=5, value=f'=IF(C{row}=0,"",D{row}/C{row})')
c.font, c.number_format = Font(name=FONT, size=10, bold=True), EUR
c = sm.cell(row=row, column=7, value=f'=D{row}/2')
c.font, c.number_format = Font(name=FONT, size=10, bold=True), EUR
row += 2

sm.cell(row=row, column=2, value='Sold cars by brand (all years)').font = F_H2
row += 1
bh = ['Brand', 'Cars sold', 'Profit (€)', 'Avg profit / car (€)', 'Avg days in stock', 'In stock now']
for i, h in enumerate(bh):
    c = sm.cell(row=row, column=2 + i, value=h)
    c.font, c.fill = F_HEAD, FILL_HEAD_CALC
    c.alignment = Alignment(horizontal='center', wrap_text=True)
row += 1
brand_order = ['VW', 'Škoda', 'Seat', 'Audi', 'Mercedes-Benz', 'Mazda', 'Alfa Romeo']
others = sorted({c['brand'] for c in cars} - set(brand_order))
for b in brand_order + others:
    crit = f'{C("status")},"SOLD",{C("brand")},B{row}'
    sm.cell(row=row, column=2, value=b).font = F_BASE
    vals = [(f'=COUNTIFS({crit})', '0'), (f'=SUMIFS({C("profit")},{crit})', EUR),
            (f'=IF(C{row}=0,"",D{row}/C{row})', EUR), (f'=IFERROR(AVERAGEIFS({C("days")},{crit}),"")', '0'),
            (f'=COUNTIFS({C("status")},"<>SOLD",{C("brand")},B{row})', '0')]
    for i, (fml, fmt) in enumerate(vals):
        c = sm.cell(row=row, column=3 + i, value=fml)
        c.font, c.number_format = F_CALC, fmt
    row += 1
row += 1

sm.cell(row=row, column=2, value='Expenses — who paid (to settle between partners)').font = F_H2
row += 1
for i, h in enumerate(['Paid by', 'Total (€)']):
    c = sm.cell(row=row, column=2 + i, value=h)
    c.font, c.fill = F_HEAD, FILL_HEAD_CALC
row += 1
for p in LISTS['Paid by']:
    sm.cell(row=row, column=2, value=p).font = F_BASE
    c = sm.cell(row=row, column=3, value=f'=SUMIFS(Expenses!$E$2:$E${EXP_LAST},Expenses!$F$2:$F${EXP_LAST},B{row},'
                                         f'Expenses!$B$2:$B${EXP_LAST},"<>EXAMPLE")')
    c.font, c.number_format = F_CALC, EUR2
    row += 1

# ---------------- Check these (import findings)
ck = wb.create_sheet('Check these')
ck.column_dimensions['A'].width = 8
ck.column_dimensions['B'].width = 38
ck.column_dimensions['C'].width = 60
ck.column_dimensions['D'].width = 70
ck['A1'] = 'Things found while moving your data — please check and fix on the Cars tab, then delete the line here'
ck['A1'].font = F_H2
style_header(ck, ['Car ID', 'Car', 'What looks wrong', 'What I did'], set(), row=3)
for ri, (no, label, prob, did) in enumerate(sorted(issues, key=lambda x: x[0]), 4):
    for ci, v in enumerate((no, label, prob, did), 1):
        c = ck.cell(row=ri, column=ci, value=v)
        c.font, c.border = F_BASE, BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
ck.freeze_panes = 'A4'

# ---------------- Read me
rm = wb.create_sheet('Read me', 0)
rm.column_dimensions['A'].width = 2
rm.column_dimensions['B'].width = 110
lines = [
    ('AUTOBONO — Car database (clean version)', F_TITLE),
    (f'Built {dt.date.today():%d.%m.%Y} from your AUTOBONO Google Sheet ("2023" + "2024" tabs, data as of 25.07.2026). '
     f'{len(cars)} cars imported. Your original sheet is not changed.', F_NOTE),
    ('', None),
    ('THE TABS', F_H2),
    ('Summary — stock, money tied up, profit per year and brand, per-partner split. Fully automatic.', F_BASE),
    ('Cars — ONE row per car, ever. Never start a new tab for a new year; filter by date instead.', F_BASE),
    ('Expenses — ONE row per bill (transport, repair, tyres, ads…), with the Car ID. Adds up into "Extra costs" on Cars.', F_BASE),
    ('Check these — problems I found in the old data (missing dates, profits that do not add up). Fix them, then delete the line.', F_BASE),
    ('Lists — the values for every dropdown. Add a new brand or country here, never type it freely.', F_BASE),
    ('', None),
    ('HOW TO USE THE CARS TAB', F_H2),
    ('• Dark-blue headers = you type. Grey headers / grey cells = automatic formulas — never type over them.', F_BASE),
    ('• New car bought: next free row, next Car ID (last is %d, so next is %d), Status = STOCK, fill purchase date and price.'
     % (max(c['id'] for c in cars), max(c['id'] for c in cars) + 1), F_BASE),
    ('• Car sold: change Status to SOLD, fill Sale date, Sale price and "VAT & deductions" (VAT you pay on the sale). Profit appears automatically.', F_BASE),
    ('• Consignment / commission car: Deal type = Consignment, put your fee in "Commission". Profit = commission − costs.', F_BASE),
    ('• Every extra cost goes on the Expenses tab with the Car ID — do not add it into Purchase price by hand.', F_BASE),
    ('• Colours: green status = in stock, yellow = reserved, grey row = sold, red "Days in stock" = unsold over 90 days, '
     'yellow date cell = missing.', F_BASE),
    ('', None),
    ('HOW PROFIT IS CALCULATED', F_H2),
    ('Profit = Sale price − (Purchase price + Extra costs) − VAT & deductions.', F_BASE),
    ('In the old sheet profit was typed by hand and not calculated the same way every time: for about 83 sold cars it was sale − costs, '
     'for others the VAT was also subtracted, and about 10 cars match neither. To keep all your old profit figures exactly as they were, '
     'I filled "VAT & deductions" for old cars with whatever difference makes the profit match. Ask your accountant which rule is correct '
     'for M (margin) and D (deductible) cars — then this column can be calculated automatically.', F_BASE),
    ('For old cars, "Purchase price" holds the old "Costs" total (purchase + extras together), because the old sheet did not keep them apart. '
     'From now on keep them separate.', F_BASE),
    ('', None),
    ('MOVING IT TO GOOGLE SHEETS', F_H2),
    ('1. Google Drive → New → File upload → choose this file. 2. Right-click → Open with → Google Sheets. '
     '3. File → Save as Google Sheets. Keep your old sheet as it is and compare the two side by side for a few weeks.', F_BASE),
    ('4. Protect the formulas: select the grey columns on Cars (Q, R, X–AB) → right-click → View more cell actions → Protect range → '
     '"Show a warning when editing this range". Do the same for the whole Summary tab.', F_BASE),
    ('5. Rename "Partner 1 / Partner 2" on the Lists tab to your names.', F_BASE),
    ('6. Agree that only one of you changes the structure (columns, tabs, formulas). Both of you add data.', F_BASE),
    ('', None),
    ('LATER: A PHONE APP ON TOP OF THIS SHEET', F_H2),
    ('Because the data is now one clean table per thing, Google AppSheet (appsheet.com, sign in with Google) can turn this sheet into a phone '
     'app with forms, photos and dropdowns — without moving the data anywhere.', F_BASE),
]
for i, (text, font) in enumerate(lines, 2):
    c = rm.cell(row=i, column=2, value=text)
    if font:
        c.font = font
    c.alignment = Alignment(wrap_text=True, vertical='top')

wb.move_sheet('Summary', offset=-wb.index(wb['Summary']) + 1)
wb.active = 0
for s in wb.worksheets:
    s.sheet_view.showGridLines = s.title in ('Cars', 'Expenses', 'Lists')
wb.save(OUT)
print(f'{OUT}: {len(cars)} cars, {len(issues)} issues listed')
