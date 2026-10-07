"""Build AUTOBONO_Database.xlsx — a clean, one-table-per-thing version of the AUTOBONO Google Sheet.

Reads the AUTOBONO.xlsx export of the Google Sheet (tabs "2024" and "2023") and writes:
  Read me · Summary · Cars · Expenses · Check these · Lists

Run:  python3 build_database_template.py /path/to/AUTOBONO.xlsx
"""
import datetime as dt
import re
import sys

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

SRC = sys.argv[1] if len(sys.argv) > 1 else 'AUTOBONO.xlsx'
OUT = 'AUTOBONO_Database.xlsx'
FIRST, LAST = 2, 1000          # data rows covered by formulas / validation on Cars
EXP_LAST = 3000                # rows covered on Expenses

FONT = 'Arial'
F_BASE = Font(name=FONT, size=10)
F_HEAD = Font(name=FONT, size=10, bold=True, color='FFFFFF')
F_TITLE = Font(name=FONT, size=16, bold=True)
F_H2 = Font(name=FONT, size=12, bold=True)
F_BOLD = Font(name=FONT, size=10, bold=True)
F_NOTE = Font(name=FONT, size=9, italic=True, color='595959')
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
DRIVE_RX = re.compile(r'4x4|4motion|quattro|4matic|xdrive|\bq4\b', re.I)
FIRST_NUM_RX = re.compile(r'^=\(*(\d+(?:\.\d+)?)(?=[+)])')   # leading purchase price in "=9020+410+40"
CELL_REF_RX = re.compile(r'^=\$?([A-Z]{1,2})\$?(\d+)$')        # "=R190"


# ---------------------------------------------------------------- read source
vals_wb = openpyxl.load_workbook(SRC, data_only=True)
fml_wb = openpyxl.load_workbook(SRC)

issues = []   # (car id, car, problem, what we did)


def clean(v):
    if isinstance(v, str):
        v = v.strip()
        return None if v in ('', '–', '-') else v
    return v


def num(v):
    v = clean(v)
    return float(v) if isinstance(v, (int, float)) else None


def split_vehicle(name):
    name = ' '.join(name.split())
    for b in TWO_WORD_BRANDS:
        if name.startswith(b):
            return b, name[len(b):].strip()
    first, _, rest = name.partition(' ')
    if first in ('VW', 'Volkswagen'):
        return 'VW', rest
    return first, rest


def first_reg(v):
    if isinstance(v, dt.datetime):
        return v.date() if v.year > 1950 else None
    if isinstance(v, (int, float)) and 1950 < v < 2100:
        return dt.date(int(v), 1, 1)
    if isinstance(v, str):
        m = re.fullmatch(r'(\d{1,2})/(\d{4})', v.strip())
        if m:
            return dt.date(int(m.group(2)), int(m.group(1)), 1)
    return None


def to_date(v):
    return v.date() if isinstance(v, dt.datetime) else None


def cost_formula(sheet, col, row, depth=0):
    """Follow '=R190'-style links and return the formula that itemises the costs (or None)."""
    f = fml_wb[sheet][f'{col}{row}'].value
    if not isinstance(f, str) or not f.startswith('='):
        return None
    m = CELL_REF_RX.match(f.replace(' ', ''))
    if m and depth < 3:
        return cost_formula(sheet, m.group(1), int(m.group(2)), depth + 1)
    return f.replace(' ', '')


def split_costs(total, formula):
    """Purchase price = first amount in the old cost formula; the rest = extra costs."""
    if total is None:
        return None, 0, None
    m = FIRST_NUM_RX.match(formula or '')
    if m:
        price = float(m.group(1))
        if 0.5 * total <= price <= total + 0.005:
            return price, round(total - price, 2), formula
    return total, 0, formula


# "2024" tab: one row per car from row 5 (cars No. 10 onward). Rows below the first empty block are
# side calculations and an old copy of the 2023 tab, so we stop at the first gap in "No.".
src = []
ws, wsv = fml_wb['2024'], vals_wb['2024']
for r in range(5, wsv.max_row + 1):
    no = wsv.cell(r, 3).value
    if not isinstance(no, (int, float)):
        break
    vehicle = clean(wsv.cell(r, 4).value)
    if not vehicle:
        continue
    g = lambda c: wsv[f'{c}{r}'].value  # noqa: E731
    src.append(dict(
        no=int(no), vehicle=vehicle, trim=clean(g('E')), myear=g('F'), engine=clean(g('G')), gearbox=clean(g('H')),
        km=num(g('I')), vin=clean(g('J')), reg_status=clean(g('K')), todo=clean(g('L')), buyer=clean(g('M')),
        flag=clean(g('N')), source=clean(g('O')), score=num(g('P')), vat=clean(g('Q')), costs=num(g('R')),
        vat_amt=num(g('T')), sale=num(g('V')), profit=num(g('X')), partner=num(g('Z')),
        pdate=to_date(g('AD')), online=to_date(g('AF')), sdate=to_date(g('AG')),
        cost_f=cost_formula('2024', 'R', r), tab='2024'))
in_2024 = {c['no'] for c in src}

# "2023" tab (Slovak headers): only cars not already continued on the 2024 tab.
wsv = vals_wb['2023']
for r in range(4, wsv.max_row + 1):
    no = wsv.cell(r, 2).value
    vehicle = clean(wsv.cell(r, 3).value)
    if not isinstance(no, (int, float)) or not vehicle or int(no) in in_2024:
        continue
    g = lambda c: wsv[f'{c}{r}'].value  # noqa: E731
    src.append(dict(
        no=int(no), vehicle=vehicle, trim=clean(g('D')), myear=g('E'), engine=clean(g('F')), gearbox=clean(g('G')),
        km=num(g('H')), vin=clean(g('I')), reg_status=None, todo=None, buyer=clean(g('J')), flag=clean(g('K')),
        source=clean(g('L')), score=None, vat=clean(g('M')), costs=num(g('N')), vat_amt=num(g('P')),
        sale=num(g('R')), profit=num(g('S')), partner=num(g('T')), pdate=None, online=to_date(g('U')),
        sdate=to_date(g('V')), cost_f=cost_formula('2023', 'N', r), tab='2023'))
src.sort(key=lambda c: c['no'])

cars, imported_expenses = [], []
for s in src:
    no = s['no']
    brand, model = split_vehicle(s['vehicle'])
    text = ' '.join(str(x or '') for x in (s['vehicle'], s['engine'], s['gearbox']))
    sold = s['sdate'] is not None
    costs, sale, profit = s['costs'], s['sale'], s['profit']
    consign = costs is not None and (costs < 1000 or (sold and (not sale or costs < 0.25 * sale)))
    reg = first_reg(s['myear'])
    label = f'{s["vehicle"]} ({reg.year if reg else "?"})'

    if consign:
        price, extra, cost_f = costs, 0, None
    else:
        price, extra, cost_f = split_costs(costs, s['cost_f'])
    if extra:
        imported_expenses.append([s['pdate'], no, 'Other',
                                  f'Imported: extra costs from old cost formula {cost_f}', extra, None, None])

    deduction = commission = None
    if sold:
        if profit is None or sale is None:
            issues.append((no, label, 'Sale date filled, but sale price or profit missing.', 'Imported as SOLD. Please fill in.'))
        elif consign:
            commission = round(profit + costs, 2)
            issues.append((no, label, f'Commission / consignment deal: costs {costs:,.0f} €, sale price {sale or 0:,.0f} €.',
                           f'Marked as Consignment. Commission = profit + costs = {commission:,.2f} € so profit stays {profit:,.2f} €. Confirm the real commission.'))
        else:
            deduction = round(sale - costs - profit, 2)
            old_vat = s['vat_amt'] or 0
            if abs(deduction) < 0.005:
                deduction = 0
            elif abs(deduction) >= 2 and abs(deduction - old_vat) >= 2:
                issues.append((no, label,
                               f'Profit ({profit:,.0f} €) ≠ sale − costs ({sale - costs:,.0f} €) and ≠ sale − costs − VAT column ({old_vat:,.0f} €).',
                               f'"VAT & deductions" set to {deduction:,.2f} € so profit matches the old sheet. Check which is right.'))
    else:
        if consign:
            issues.append((no, label, f'Looks like a consignment car (costs only {costs:,.0f} €).',
                           'Marked as Consignment. Change Deal type if wrong.'))
        if s['tab'] == '2023':
            issues.append((no, label, 'Only on the old 2023 tab and no sale date — is it really still in stock?',
                           'Imported as STOCK. Change to SOLD (with date and price) or delete the row.'))
    if s['pdate'] is None:
        issues.append((no, label, 'Purchase date missing.', 'Left empty — days in stock cannot be calculated.'))
    if sold and s['online'] is None:
        issues.append((no, label, 'Sold, but "Online since" date missing.', 'Left empty — days online cannot be calculated.'))
    if reg is None:
        issues.append((no, label, 'First registration (model year) missing or not a date.', 'Left empty. Fill in from the papers.'))
    if not s['vin']:
        issues.append((no, label, 'VIN missing.', 'Left empty.'))

    src_val = s['source']
    if isinstance(src_val, float):
        src_val = str(int(src_val))
    cars.append(dict(
        id=no, status='SOLD' if sold else 'STOCK', deal='Consignment' if consign else 'Own purchase',
        brand=brand, model=model, trim=s['trim'], reg=reg, engine=s['engine'],
        gearbox=(s['gearbox'] or '').split()[0] or None if s['gearbox'] else None,
        drive='4x4' if DRIVE_RX.search(text) else None, km=s['km'], vin=s['vin'],
        reg_status=s['reg_status'], todo=s['todo'], country=FLAG.get(s['flag'], s['flag']), source=src_val,
        score=s['score'], vat=s['vat'], pdate=s['pdate'], online=s['online'], price=price,
        asking=sale if not sold and sale else None, sdate=s['sdate'], sale=sale if sold else None,
        deduction=deduction, commission=commission, buyer=s['buyer'] if sold else None,
        partner=s['partner'] if sold else None, notes=None))

# ---------------------------------------------------------------- workbook
wb = openpyxl.Workbook()


def style_header(ws, headers, calc_cols, row=1):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = F_HEAD
        c.fill = FILL_HEAD_CALC if i in calc_cols else FILL_HEAD_IN
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    ws.row_dimensions[row].height = 42


def add_list_validation(ws, col, ref, last, strict=True):
    dv = DataValidation(type='list', formula1=ref, allow_blank=True, showErrorMessage=True)
    if not strict:
        dv.errorStyle = 'warning'
    dv.add(f'{col}{FIRST}:{col}{last}')
    ws.add_data_validation(dv)


# ---------------- Lists (dropdown sources)
lists = wb.active
lists.title = 'Lists'
LISTS = {
    'Status': ['STOCK', 'RESERVED', 'SOLD'],
    'Deal type': ['Own purchase', 'Consignment'],
    'Brand': sorted({c['brand'] for c in cars} | {'BMW', 'Ford', 'Toyota', 'Cupra', 'Hyundai', 'Kia'}),
    'Gearbox': sorted({c['gearbox'] for c in cars if c['gearbox']}),
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
    list_ref[name] = f'Lists!${col}$2:${col}$60'   # room to add values without touching the rules
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
    ('vin', 'VIN', 20, 'in', '@'),
    ('reg_status', 'Reg. / STK', 9, 'in', None),
    ('todo', 'To do', 11, 'in', None),
    ('country', 'Country (old "State")', 9, 'in', None),
    ('source', 'Origin / seller', 14, 'in', None),
    ('score', 'Score (/22)', 7, 'in', '0'),
    ('vat', 'VAT scheme (M/D)', 8, 'in', None),
    ('pdate', 'Purchase date', 11, 'in', DATE),
    ('online', 'Online since', 11, 'in', DATE),
    ('price', 'Purchase price (€)', 12, 'in', EUR2),
    ('extra', 'Extra costs (€) [from Expenses]', 12, 'calc', EUR2),
    ('total', 'Total cost (€)', 12, 'calc', EUR2),
    ('asking', 'Asking price (€)', 11, 'in', EUR),
    ('sdate', 'Sale date', 11, 'in', DATE),
    ('sale', 'Sale price (€)', 12, 'in', EUR2),
    ('deduction', 'VAT & deductions (€)', 12, 'in', EUR2),
    ('commission', 'Commission (€) [consignment only]', 13, 'in', EUR2),
    ('buyer', 'Buyer', 20, 'in', None),
    ('profit', 'Profit (€)', 12, 'calc', EUR2),
    ('margin', 'Margin % of cost', 9, 'calc', PCT),
    ('prep', 'Prep days (bought → online)', 8, 'calc', '0'),
    ('daysonline', 'Days online', 8, 'calc', '0'),
    ('days', 'Days in stock (total)', 8, 'calc', '0'),
    ('month', 'Sale month', 9, 'calc', '@'),
    ('partner', 'Investor / partner share (€)', 12, 'in', EUR2),
    ('notes', 'Notes', 40, 'in', None),
]
L = {k: get_column_letter(i) for i, (k, *_r) in enumerate(COLS, 1)}
calc_idx = {i for i, c in enumerate(COLS, 1) if c[3] == 'calc'}
style_header(ws, [c[1] for c in COLS], calc_idx)
for i, (_k, _h, w, _kind, _f) in enumerate(COLS, 1):
    ws.column_dimensions[get_column_letter(i)].width = w


def formulas(r):
    c = {k: f'{v}{r}' for k, v in L.items()}
    exp = f'Expenses!$B$2:$B${EXP_LAST}'
    amt = f'Expenses!$E$2:$E${EXP_LAST}'
    end = f'IF({c["sdate"]}="",TODAY(),{c["sdate"]})'
    return {
        'extra': f'=IF({c["id"]}="","",SUMIF({exp},{c["id"]},{amt}))',
        'total': f'=IF({c["id"]}="","",N({c["price"]})+N({c["extra"]}))',
        'profit': (f'=IF({c["status"]}<>"SOLD","",IF({c["deal"]}="Consignment",'
                   f'N({c["commission"]})-{c["total"]},N({c["sale"]})-{c["total"]}-N({c["deduction"]})))'),
        'margin': f'=IF(OR({c["profit"]}="",N({c["total"]})=0),"",{c["profit"]}/{c["total"]})',
        'prep': f'=IF(OR({c["pdate"]}="",{c["online"]}=""),"",{c["online"]}-{c["pdate"]})',
        'daysonline': f'=IF({c["online"]}="","",{end}-{c["online"]})',
        'days': f'=IF({c["pdate"]}="","",{end}-{c["pdate"]})',
        'month': f'=IF({c["sdate"]}="","",TEXT({c["sdate"]},"YYYY-MM"))',
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
for key in ('pdate', 'online', 'sdate', 'reg'):
    dv = DataValidation(type='date', operator='greaterThan', formula1='DATE(1990,1,1)', allow_blank=True,
                        showErrorMessage=True, error='Please enter a real date, e.g. 15.03.2026')
    dv.add(f'{L[key]}{FIRST}:{L[key]}{LAST}')
    ws.add_data_validation(dv)
for key in ('km', 'price', 'sale', 'asking', 'commission'):
    dv = DataValidation(type='decimal', operator='greaterThanOrEqual', formula1='0', allow_blank=True,
                        showErrorMessage=True, error='Numbers only (no € sign, no text).')
    dv.add(f'{L[key]}{FIRST}:{L[key]}{LAST}')
    ws.add_data_validation(dv)
dv = DataValidation(type='custom', formula1=f'COUNTIF($A${FIRST}:$A${LAST},A{FIRST})=1', allow_blank=True,
                    showErrorMessage=True, error='This Car ID is already used.')
dv.add(f'A{FIRST}:A{LAST}')
ws.add_data_validation(dv)

st = L['status']
ws.conditional_formatting.add(f'A{FIRST}:{L["notes"]}{LAST}',
                              FormulaRule(formula=[f'${st}{FIRST}="SOLD"'], font=Font(color='808080')))
ws.conditional_formatting.add(f'{st}{FIRST}:{st}{LAST}',
                              FormulaRule(formula=[f'{st}{FIRST}="STOCK"'], fill=PatternFill('solid', fgColor='E2EFDA')))
ws.conditional_formatting.add(f'{st}{FIRST}:{st}{LAST}',
                              FormulaRule(formula=[f'{st}{FIRST}="RESERVED"'], fill=FILL_YELLOW))
ws.conditional_formatting.add(f'{L["days"]}{FIRST}:{L["days"]}{LAST}',
                              FormulaRule(formula=[f'AND(${st}{FIRST}<>"SOLD",N({L["days"]}{FIRST})>90)'],
                                          fill=PatternFill('solid', fgColor='F8CBAD')))
ws.conditional_formatting.add(f'{L["profit"]}{FIRST}:{L["profit"]}{LAST}',
                              FormulaRule(formula=[f'AND({L["profit"]}{FIRST}<>"",{L["profit"]}{FIRST}<0)'], font=Font(color='C00000')))
for key in ('pdate', 'reg', 'vin'):  # missing important data → yellow
    ws.conditional_formatting.add(f'{L[key]}{FIRST}:{L[key]}{LAST}',
                                  FormulaRule(formula=[f'AND($A{FIRST}<>"",{L[key]}{FIRST}="")'], fill=FILL_YELLOW))

# ---------------- Expenses
ex = wb.create_sheet('Expenses', 1)
EX_COLS = [('Date', 11, DATE), ('Car ID', 8, '0'), ('Category', 20, None), ('Description', 60, None),
           ('Amount (€)', 12, EUR2), ('Paid by', 16, None), ('Invoice / receipt no.', 18, '@')]
style_header(ex, [c[0] for c in EX_COLS], set())
example = [dt.date(2026, 10, 1), 'EXAMPLE', 'Repair & service', 'Example row — serpentine belt + oil change (delete me)',
           240, 'Partner 1', 'FA-2026-0123']
exp_rows = [example] + imported_expenses
for i, (_h, w, fmt) in enumerate(EX_COLS, 1):
    ex.column_dimensions[get_column_letter(i)].width = w
    for ri in range(FIRST, EXP_LAST + 1):
        c = ex.cell(row=ri, column=i)
        if ri - FIRST < len(exp_rows):
            c.value = exp_rows[ri - FIRST][i - 1]
        c.font = F_NOTE if ri == FIRST else F_BASE
        c.border = BORDER
        if fmt:
            c.number_format = fmt
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
sm.column_dimensions['B'].width = 44
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
    ('Stock cars not yet online', f'=COUNTIFS({C("status")},"<>SOLD",{C("id")},"<>",{C("online")},"")', '0'),
    ('Stock cars older than 90 days', f'=COUNTIFS({C("status")},"<>SOLD",{C("id")},"<>",{C("days")},">90")', '0'),
    ('Average days in stock (cars not yet sold)',
     f'=IFERROR(AVERAGEIFS({C("days")},{C("status")},"<>SOLD",{C("id")},"<>"),"")', '0'),
]
for label, fml, fmt in now_rows:
    sm.cell(row=row, column=2, value=label).font = F_BASE
    c = sm.cell(row=row, column=3, value=fml)
    c.font, c.number_format = F_CALC, fmt
    row += 1


def table_header(row, headers):
    for i, h in enumerate(headers):
        c = sm.cell(row=row, column=2 + i, value=h)
        c.font, c.fill = F_HEAD, FILL_HEAD_CALC
        c.alignment = Alignment(horizontal='center', wrap_text=True)


row += 1
sm.cell(row=row, column=2, value='Sold cars by year (by sale date)').font = F_H2
row += 1
table_header(row, ['Year', 'Cars sold', 'Profit (€)', 'Avg profit / car (€)', 'Avg days in stock',
                   'Avg days online', 'Investor / partner share (€)'])
row += 1
y_first = row
for y in range(2023, max(dt.date.today().year, 2026) + 1):
    lo, hi = f'DATE({y},1,1)', f'DATE({y + 1},1,1)'
    crit = f'{C("status")},"SOLD",{C("sdate")},">="&{lo},{C("sdate")},"<"&{hi}'
    sm.cell(row=row, column=2, value=str(y)).font = F_BASE
    vals = [(f'=COUNTIFS({crit})', '0'),
            (f'=SUMIFS({C("profit")},{crit})', EUR),
            (f'=IF(C{row}=0,"",D{row}/C{row})', EUR),
            (f'=IFERROR(AVERAGEIFS({C("days")},{crit}),"")', '0'),
            (f'=IFERROR(AVERAGEIFS({C("daysonline")},{crit}),"")', '0'),
            (f'=SUMIFS({C("partner")},{crit})', EUR)]
    for i, (fml, fmt) in enumerate(vals):
        c = sm.cell(row=row, column=3 + i, value=fml)
        c.font, c.number_format = F_CALC, fmt
    row += 1
sm.cell(row=row, column=2, value='All years').font = F_BOLD
for col_i, fml, fmt in ((3, f'=SUM(C{y_first}:C{row - 1})', '0'), (4, f'=SUM(D{y_first}:D{row - 1})', EUR),
                        (5, f'=IF(C{row}=0,"",D{row}/C{row})', EUR), (8, f'=SUM(H{y_first}:H{row - 1})', EUR)):
    c = sm.cell(row=row, column=col_i, value=fml)
    c.font, c.number_format = F_BOLD, fmt
row += 2

sm.cell(row=row, column=2, value='Sold cars by brand (all years)').font = F_H2
row += 1
table_header(row, ['Brand', 'Cars sold', 'Profit (€)', 'Avg profit / car (€)', 'Avg days in stock', 'In stock now'])
row += 1
brand_order = ['VW', 'Škoda', 'Seat', 'Audi', 'Mercedes-Benz', 'Mazda', 'Alfa Romeo']
for b in brand_order + sorted({c['brand'] for c in cars} - set(brand_order)):
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
table_header(row, ['Paid by', 'Total (€)'])
row += 1
for p in LISTS['Paid by'] + ['(not filled in)']:
    sm.cell(row=row, column=2, value=p).font = F_BASE
    who = '""' if p.startswith('(') else f'B{row}'
    c = sm.cell(row=row, column=3, value=f'=SUMIFS(Expenses!$E$2:$E${EXP_LAST},Expenses!$F$2:$F${EXP_LAST},{who},'
                                         f'Expenses!$B$2:$B${EXP_LAST},"<>EXAMPLE")')
    c.font, c.number_format = F_CALC, EUR2
    row += 1

# ---------------- Check these (import findings)
ck = wb.create_sheet('Check these')
for col, w in zip('ABCD', (8, 38, 60, 70)):
    ck.column_dimensions[col].width = w
ck['A1'] = 'Things found while moving your data — fix them on the Cars tab, then delete the line here'
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
next_id = max(c['id'] for c in cars) + 1
grey_cols = ', '.join(L[k] for k, *_r in COLS if _r[2] == 'calc')
lines = [
    ('AUTOBONO — Car database (clean version)', F_TITLE),
    (f'Built {dt.date.today():%d.%m.%Y} from your AUTOBONO Google Sheet ("2024" and "2023" tabs). '
     f'{len(cars)} cars imported. Your original sheet is not changed.', F_NOTE),
    ('', None),
    ('THE TABS', F_H2),
    ('Summary — stock, money tied up, profit per year and brand, days online, investor/partner share. Fully automatic.', F_BASE),
    ('Cars — ONE row per car, ever. Never start a new tab for a new year; filter by date instead.', F_BASE),
    ('Expenses — ONE row per bill (transport, repair, tyres, ads…), with the Car ID. Adds up into "Extra costs" on Cars.', F_BASE),
    ('Check these — problems found in the old data (missing dates, profits that do not add up). Fix them, then delete the line.', F_BASE),
    ('Lists — the values for every dropdown. Add a new brand or country here, never type it freely.', F_BASE),
    ('', None),
    ('HOW TO USE THE CARS TAB', F_H2),
    ('• Dark-blue headers = you type. Grey headers / grey cells = automatic formulas — never type over them.', F_BASE),
    (f'• New car bought: next free row, next Car ID ({next_id}), Status = STOCK, fill purchase date and purchase price '
     '(the price for the car only).', F_BASE),
    ('• Car goes online: fill "Online since". Prep days and days online are then counted automatically.', F_BASE),
    ('• Car sold: Status = SOLD, fill Sale date, Sale price, Buyer and "VAT & deductions" (VAT you pay on the sale). '
     'Profit appears automatically. Fill the investor / partner share.', F_BASE),
    ('• Consignment / commission car: Deal type = Consignment, put your fee in "Commission". Profit = commission − costs.', F_BASE),
    ('• Every extra cost (transport, repair, STK, ads…) is a line on the Expenses tab with the Car ID — no more long "=9020+410+40" '
     'formulas in one cell; you will see what each number was.', F_BASE),
    ('• Colours: green status = in stock, yellow = reserved, grey row = sold, red "Days in stock" = unsold over 90 days, '
     'yellow cell = missing purchase date, first registration or VIN.', F_BASE),
    ('', None),
    ('WHAT CHANGED COMPARED TO THE OLD SHEET', F_H2),
    ('• Costs: your old cost cells were formulas like "=(9020+410)+300+40". The first amount became "Purchase price"; '
     'everything after it became one line on the Expenses tab (with the original formula in the description), so each car\'s '
     'total cost is exactly the same as before. From now on, enter extras one by one with a category.', F_BASE),
    ('• Profit: the old profit was calculated differently for different cars (sale − costs, netto − costs, '
     'sale/1.2 − costs, sometimes + or − a fixed amount). To keep every profit exactly as before, "VAT & deductions" '
     'holds whatever difference makes it match. Ask your accountant for one rule for M and D cars — then this column can be automatic.', F_BASE),
    ('• Investor / partner share: imported as typed in "Profit investor" (it includes your manual corrections, so it is not '
     'always exactly half).', F_BASE),
    ('• Flags became country codes (🇩🇪 → DE). The "Origin" column (1, 2, 3, 4 or a seller name) is kept as it was in "Origin / seller".', F_BASE),
    ('• Not imported: the unnumbered side calculations below the car list on the 2024 tab, the old copy of the 2023 tab under it, '
     'and the statistics columns (median, Ø per month, cash stuck…) — the Summary tab replaces them.', F_BASE),
    ('', None),
    ('MOVING IT TO GOOGLE SHEETS', F_H2),
    ('1. Google Drive → New → File upload → choose this file. 2. Right-click → Open with → Google Sheets. '
     '3. File → Save as Google Sheets. Keep your old sheet as it is and compare the two side by side for a few weeks.', F_BASE),
    (f'4. Protect the formulas: on Cars select the grey columns ({grey_cols}) → right-click → View more cell actions → Protect range → '
     '"Show a warning when editing this range". Do the same for the whole Summary tab.', F_BASE),
    ('5. Rename "Partner 1 / Partner 2" on the Lists tab to your names.', F_BASE),
    ('6. Agree that only one of you changes the structure (columns, tabs, formulas). Both of you add data.', F_BASE),
    ('7. The file contains buyers\' names and VINs (personal data) — share it only between the two of you.', F_BASE),
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
print(f'{OUT}: {len(cars)} cars ({sum(c["status"] == "SOLD" for c in cars)} sold), '
      f'{len(imported_expenses)} expense lines, {len(issues)} issues listed')
