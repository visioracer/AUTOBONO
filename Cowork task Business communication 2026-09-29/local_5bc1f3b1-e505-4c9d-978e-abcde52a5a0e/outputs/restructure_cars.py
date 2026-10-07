"""Reorder the Cars tab into clear blocks and make VAT / partner share calculate by themselves.

  Car · Paperwork · Purchase · Sale · Time · Notes · (hidden) Manual corrections

- VAT on sale and Investor / partner share become formulas. Where the old value differs from what the
  formula gives, the old value goes into the hidden "manual" column, so nothing historic changes.
- VIN goes into a collapsed column group; notes are written as plain notes (no author), the way Google
  Sheets exports them, so they come back as notes and not as comments.
- Every other tab's references to Cars are re-pointed to the new column letters.

Run:  python3 restructure_cars.py IN.xlsx RECALCULATED_COPY_OF_IN.xlsx OUT.xlsx
"""
import copy
import re
import sys

import openpyxl
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

IN, CALC, OUT = sys.argv[1:4]
wb = openpyxl.load_workbook(IN)
vals = openpyxl.load_workbook(CALC, data_only=True)['Cars']
old = wb['Cars']
OH = {c.value: c.column for c in old[1] if c.value}
LAST = 1000

# ---- new layout: (header, kind, block)   kind: in = typed, calc = formula
BLOCKS = {'car': '1F4E78', 'paper': '5B4A8B', 'buy': '375623', 'sale': '833C0B', 'time': '595959', 'fix': 'A6A6A6'}
COLS = [
    ('Car ID', 'in', 'car'), ('Status', 'in', 'car'), ('Brand', 'in', 'car'), ('Model', 'in', 'car'),
    ('Trim', 'in', 'car'), ('Deal type', 'in', 'car'), ('Financed by', 'in', 'car'),
    ('First registration', 'in', 'car'), ('Engine', 'in', 'car'), ('Gearbox', 'in', 'car'), ('Drive', 'in', 'car'),
    ('Mileage (km)', 'in', 'car'), ('VIN', 'in', 'car'),
    ('Reg. / STK', 'in', 'paper'), ('To do', 'in', 'paper'), ('STK date', 'in', 'paper'), ('STK fee (350 €)', 'in', 'paper'),
    ('Purchase date', 'in', 'buy'), ('Seller', 'in', 'buy'), ('Country (old "State")', 'in', 'buy'),
    ('Score (/22)', 'in', 'buy'), ('VAT scheme (M/D)', 'in', 'buy'), ('Purchase price (€)', 'in', 'buy'),
    ('Extra costs (€) [from Expenses]', 'calc', 'buy'), ('Total cost (€)', 'calc', 'buy'),
    ('Online since', 'in', 'buy'), ('Asking price (€)', 'in', 'buy'),
    ('Sale date', 'in', 'sale'), ('Buyer', 'in', 'sale'), ('Sold via', 'in', 'sale'), ('Sale price (€)', 'in', 'sale'),
    ('VAT on sale (€)', 'calc', 'sale'), ('Commission (€) [consignment only]', 'in', 'sale'),
    ('Profit (€)', 'calc', 'sale'), ('Margin % of cost', 'calc', 'sale'), ('Investor / partner share (€)', 'calc', 'sale'),
    ('Prep days (bought → online)', 'calc', 'time'), ('Days online', 'calc', 'time'),
    ('Days in stock (total)', 'calc', 'time'), ('Sale month', 'calc', 'time'),
    ('Notes', 'in', 'time'),
    ('VAT – manual (€)', 'in', 'fix'), ('Partner share – manual (€)', 'in', 'fix'), ('Other adjustment (€)', 'in', 'fix'),
]
N = {h: get_column_letter(i) for i, (h, _k, _b) in enumerate(COLS, 1)}
OLD_LETTER = {h: get_column_letter(c) for h, c in OH.items()}
FMT = {'Purchase date': 'dd.mm.yyyy', 'Online since': 'dd.mm.yyyy', 'Sale date': 'dd.mm.yyyy', 'STK date': 'dd.mm.yyyy',
       'First registration': 'mm/yyyy', 'VAT – manual (€)': '#,##0.00 €;-#,##0.00 €;-',
       'Partner share – manual (€)': '#,##0.00 €;-#,##0.00 €;-'}
WIDTH = {'VAT – manual (€)': 12, 'Partner share – manual (€)': 12}
VAT_RATE = 'Monthly!$C$4'

# ---- historic VAT / partner share that the new formulas would not reproduce → manual columns
manual_vat, manual_share = {}, {}
for r in range(2, LAST + 1):
    sale = vals.cell(r, OH['Sale price (€)']).value
    sdate = vals.cell(r, OH['Sale date']).value
    if not sdate:
        continue
    scheme = vals.cell(r, OH['VAT scheme (M/D)']).value
    price = vals.cell(r, OH['Purchase price (€)']).value or 0
    vat = vals.cell(r, OH['VAT on sale (€)']).value or 0
    if isinstance(sale, (int, float)):
        auto = sale * 0.23 / 1.23 if scheme == 'D' else max(0, sale - price) * 0.23 / 1.23
        if abs(auto - vat) > 0.01:
            manual_vat[r] = vat
    profit = vals.cell(r, OH['Profit (€)']).value
    share = vals.cell(r, OH['Investor / partner share (€)']).value
    if isinstance(profit, (int, float)):
        if share is None or not isinstance(share, (int, float)):
            manual_share[r] = 0
        elif abs(profit / 2 - share) > 0.01:
            manual_share[r] = share

# ---- build the new sheet
idx = wb.sheetnames.index('Cars')
new = wb.create_sheet('Cars_new', idx)
for i, (h, kind, block) in enumerate(COLS, 1):
    c = new.cell(1, i, h)
    c._style = copy.copy(old['A1']._style)
    c.fill = PatternFill('solid', fgColor=BLOCKS[block])
    src_col = OLD_LETTER.get(h)
    new.column_dimensions[get_column_letter(i)].width = (
        WIDTH.get(h) or (old.column_dimensions[src_col].width if src_col else 12) or 12)
new.row_dimensions[1].height = old.row_dimensions[1].height


def formulas(r):
    c = {h: f'{L}{r}' for h, L in N.items()}
    end = f'IF({c["Sale date"]}="",TODAY(),{c["Sale date"]})'
    rate = VAT_RATE
    return {
        'Extra costs (€) [from Expenses]': f'=IF({c["Car ID"]}="","",SUMIF(Expenses!$B$2:$B$3000,{c["Car ID"]},Expenses!$E$2:$E$3000))',
        'Total cost (€)': f'=IF({c["Car ID"]}="","",N({c["Purchase price (€)"]})+N({c["Extra costs (€) [from Expenses]"]}))',
        'VAT on sale (€)': (f'=IF(OR({c["Sale date"]}="",{c["Sale price (€)"]}=""),"",IF({c["VAT – manual (€)"]}<>"",'
                            f'{c["VAT – manual (€)"]},IF({c["VAT scheme (M/D)"]}="D",{c["Sale price (€)"]}*{rate}/(1+{rate}),'
                            f'MAX(0,{c["Sale price (€)"]}-N({c["Purchase price (€)"]}))*{rate}/(1+{rate}))))'),
        'Profit (€)': (f'=IF({c["Sale date"]}="","",IF({c["Deal type"]}="Consignment",'
                       f'N({c["Commission (€) [consignment only]"]})-{c["Total cost (€)"]},IF({c["Sale price (€)"]}="","",'
                       f'{c["Sale price (€)"]}-{c["Total cost (€)"]}-N({c["VAT on sale (€)"]})-N({c["Other adjustment (€)"]}))))'),
        'Margin % of cost': f'=IF(OR({c["Profit (€)"]}="",N({c["Total cost (€)"]})=0),"",{c["Profit (€)"]}/{c["Total cost (€)"]})',
        'Investor / partner share (€)': (f'=IF({c["Profit (€)"]}="","",IF({c["Partner share – manual (€)"]}<>"",'
                                         f'{c["Partner share – manual (€)"]},{c["Profit (€)"]}/2))'),
        'Prep days (bought → online)': f'=IF(OR({c["Purchase date"]}="",{c["Online since"]}=""),"",{c["Online since"]}-{c["Purchase date"]})',
        'Days online': f'=IF({c["Online since"]}="","",{end}-{c["Online since"]})',
        'Days in stock (total)': f'=IF({c["Purchase date"]}="","",{end}-{c["Purchase date"]})',
        'Sale month': f'=IF({c["Sale date"]}="","",TEXT({c["Sale date"]},"YYYY-MM"))',
    }


for r in range(2, LAST + 1):
    f = formulas(r)
    for i, (h, kind, block) in enumerate(COLS, 1):
        dst = new.cell(r, i)
        src = old.cell(r, OH[h]) if h in OH else None
        if src is not None:
            dst._style = copy.copy(src._style)
        if kind == 'calc':
            dst.value = f[h]
            if src is None:
                dst._style = copy.copy(old.cell(r, OH['Profit (€)'])._style)
        elif h == 'VAT – manual (€)':
            dst.value = manual_vat.get(r)
        elif h == 'Partner share – manual (€)':
            dst.value = manual_share.get(r)
        elif src is not None:
            dst.value = src.value
        if h in FMT:
            dst.number_format = FMT[h]
        if src is not None and src.comment:      # plain note, no author → Google keeps it as a note
            note = Comment(src.comment.text, '')
            note.width, note.height = src.comment.width, src.comment.height
            dst.comment = note

# formulas used to calc VAT/share were inputs before: style them like the other formula cells
for h in ('VAT on sale (€)', 'Investor / partner share (€)'):
    for r in range(2, LAST + 1):
        new[f'{N[h]}{r}']._style = copy.copy(old.cell(r, OH['Profit (€)'])._style)
        new[f'{N[h]}{r}'].number_format = '#,##0.00 €;-#,##0.00 €;-'

new.freeze_panes = 'E2'
new.auto_filter.ref = f'A1:{N["Other adjustment (€)"]}{LAST}'
new.column_dimensions.group(N['VIN'], N['VIN'], hidden=True, outline_level=1)
new.column_dimensions.group(N['VAT – manual (€)'], N['Other adjustment (€)'], hidden=True, outline_level=1)
new.sheet_properties.outlinePr.summaryRight = False

# ---- validations (same lists as before, new letters)
lists = wb['Lists']
LH = {c.value: c.column_letter for c in lists[1] if c.value}
fin_col = LH['Financed by']
fin_vals = [lists[f'{fin_col}{r}'].value for r in range(2, 61) if lists[f'{fin_col}{r}'].value]
if 'Investor' not in fin_vals:
    lists[f'{fin_col}{len(fin_vals) + 2}'] = 'Investor'
    lists[f'{fin_col}{len(fin_vals) + 2}']._style = copy.copy(lists[f'{fin_col}2']._style)


def dv_list(h, lst, strict=True):
    dv = DataValidation(type='list', formula1=f'Lists!${LH[lst]}$2:${LH[lst]}$60', allow_blank=True, showErrorMessage=True)
    if not strict:
        dv.errorStyle = 'warning'
    dv.add(f'{N[h]}2:{N[h]}{LAST}')
    new.add_data_validation(dv)


for h, lst, strict in (('Status', 'Status', True), ('Deal type', 'Deal type', True), ('Brand', 'Brand', False),
                       ('Gearbox', 'Gearbox', False), ('Drive', 'Drive', True), ('Country (old "State")', 'Country', False),
                       ('VAT scheme (M/D)', 'VAT scheme', True), ('Financed by', 'Financed by', True),
                       ('Sold via', 'Sold via', True), ('STK fee (350 €)', 'STK fee', True)):
    dv_list(h, lst, strict)
dv = DataValidation(type='date', operator='greaterThan', formula1='DATE(1990,1,1)', allow_blank=True, showErrorMessage=True,
                    error='Please enter a real date, e.g. 15.03.2026')
for h in ('First registration', 'STK date', 'Purchase date', 'Online since', 'Sale date'):
    dv.add(f'{N[h]}2:{N[h]}{LAST}')
new.add_data_validation(dv)
dv = DataValidation(type='decimal', operator='greaterThanOrEqual', formula1='0', allow_blank=True, showErrorMessage=True,
                    error='Numbers only (no € sign, no text).')
for h in ('Mileage (km)', 'Purchase price (€)', 'Asking price (€)', 'Sale price (€)', 'Commission (€) [consignment only]',
          'VAT – manual (€)'):
    dv.add(f'{N[h]}2:{N[h]}{LAST}')
new.add_data_validation(dv)
dv = DataValidation(type='custom', formula1=f'COUNTIF($A$2:$A${LAST},A2)=1', allow_blank=True, showErrorMessage=True,
                    error='This Car ID is already used.')
dv.add(f'A2:A{LAST}')
new.add_data_validation(dv)

# ---- conditional formatting (same rules, new letters)
st, sd, model = N['Status'], N['Sale date'], N['Model']
prev = get_column_letter(openpyxl.utils.column_index_from_string(model) - 1)
nxt = get_column_letter(openpyxl.utils.column_index_from_string(model) + 1)
new.conditional_formatting.add(f'A2:{prev}{LAST} {nxt}2:{N["Other adjustment (€)"]}{LAST}',
                               FormulaRule(formula=[f'${st}2="SOLD"'], font=Font(color='808080')))
for val, color in (('STOCK', 'E2EFDA'), ('RESERVED', 'FFF2CC'), ('IN USE', 'DDEBF7')):
    new.conditional_formatting.add(f'{st}2:{st}{LAST}',
                                   FormulaRule(formula=[f'{st}2="{val}"'], fill=PatternFill('solid', fgColor=color)))
d = N['Days in stock (total)']
new.conditional_formatting.add(f'{d}2:{d}{LAST}', FormulaRule(
    formula=[f'AND(${sd}2="",${st}2<>"IN USE",N({d}2)>90)'], fill=PatternFill('solid', fgColor='F8CBAD')))
p = N['Profit (€)']
new.conditional_formatting.add(f'{p}2:{p}{LAST}', FormulaRule(formula=[f'AND({p}2<>"",{p}2<0)'], font=Font(color='C00000')))
for h in ('Purchase date', 'First registration'):
    L = N[h]
    new.conditional_formatting.add(f'{L}2:{L}{LAST}', FormulaRule(formula=[f'AND($A2<>"",{L}2="")'],
                                                                     fill=PatternFill('solid', fgColor='FFF2CC')))

# ---- swap sheets and re-point every reference to Cars
wb.remove(old)
new.title = 'Cars'
remap = {OLD_LETTER[h]: N[h] for h in OLD_LETTER if h in N}
RX = re.compile(r"Cars!\$([A-Z]{1,3})\$(\d+)(?::\$([A-Z]{1,3})\$(\d+))?")


def fix(text):
    def one(m):
        a = remap.get(m.group(1), m.group(1))
        if m.group(3) is None:
            return f'Cars!${a}${m.group(2)}'
        return f'Cars!${a}${m.group(2)}:${remap.get(m.group(3), m.group(3))}${m.group(4)}'
    return RX.sub(one, text)


for ws in wb.worksheets:
    if ws.title == 'Cars':
        continue
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and 'Cars!' in c.value:
                c.value = fix(c.value)
    for dvx in ws.data_validations.dataValidation:
        if dvx.formula1 and 'Cars!' in dvx.formula1:
            dvx.formula1 = fix(dvx.formula1)
    for rng in ws.conditional_formatting:
        for rule in rng.rules:
            rule.formula = [fix(x) for x in rule.formula]

# ---- VAT rate setting on Monthly, next to the STK fee
mo = wb['Monthly']
mo['B4'], mo['C4'] = 'VAT rate (used for new sales)', 0.23
mo['B4']._style = copy.copy(mo['B5']._style)
mo['C4']._style = copy.copy(mo['C5']._style)
mo['C4'].number_format = '0%'

# ---- Read me
rm = wb['Read me']
texts = {
    '• Dark-blue headers': ('• Header colours show the blocks: blue = the car, purple = paperwork / STK, green = purchase, '
                            'brown = sale, grey = time. Grey cells are formulas — never type over them.'),
    '• Car sold:': ('• Car sold: fill Sale date, Buyer, Sold via and Sale price. VAT, profit and partner share are calculated by '
                    'themselves (VAT: D car = sale price × 23/123, M car = (sale price − purchase price) × 23/123; partner share '
                    '= profit ÷ 2). Status = SOLD when everything is dealt with; keep RESERVED (yellow) while something is open.'),
    '• Car bought with Branko': '• "Financed by": Company, Branko, Samko or Investor.',
}
for row in rm.iter_rows():
    for c in row:
        if isinstance(c.value, str):
            for start, text in texts.items():
                if c.value.startswith(start):
                    c.value = text
extra = [
    '• Hidden columns: click the small "+" above the column letters to open them. VIN sits next to Mileage. At the far right, '
    '"Manual corrections" (VAT – manual, Partner share – manual, Other adjustment) override the automatic VAT / share / profit '
    'only when a deal is special — old cars use them so their numbers stay exactly as in your old sheet.',
    '• The VAT rate for new sales is set once on the Monthly tab (cell C4).',
]
last = max(r for r in range(1, rm.max_row + 1) if rm.cell(r, 2).value)
for i, t in enumerate(extra, 1):
    c = rm.cell(last + 1 + i, 2, t)
    c._style = copy.copy(rm.cell(last, 2)._style)
    c.alignment = Alignment(wrap_text=True, vertical='top')

wb.save(OUT)
print(f'columns: {len(COLS)}, manual VAT kept for {len(manual_vat)} cars, manual partner share for {len(manual_share)} cars')
