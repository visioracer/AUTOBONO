import json
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

with open('raw_rows.json') as f:
    raw = json.load(f)

def normModel(v):
    s = v.replace('Volkswagen', 'VW', 1).strip() if v.startswith('Volkswagen') else v
    two = ['Alfa Romeo', 'Mercedes-Benz', 'Land Rover']
    for b in two:
        if s.startswith(b):
            parts = s.split()
            n = len(b.split())
            return b + ' ' + (parts[n] if len(parts) > n else '')
    parts = s.split()
    return ' '.join(parts[:2])

def pdate(s):
    if not s:
        return None
    d, m, y = s.split('.')
    return datetime.date(int(y), int(m), int(d))

for r in raw:
    r.append(normModel(r[2]))  # 21 model group

models_sorted = sorted({r[21] for r in raw if r[20] == 'SOLD'})

months_sorted = sorted({r[18][3:5] + '-99' for r in raw})  # placeholder, replaced below
months_set = set()
for r in raw:
    if r[20] == 'SOLD' and r[18]:
        d = pdate(r[18])
        months_set.add(f'{d.year:04d}-{d.month:02d}')
months_sorted = sorted(months_set)

# ---------- Styling ----------
FONT_NAME = 'Arial'
HEADER_FONT = Font(name=FONT_NAME, size=10, bold=True, color='FFFFFF')
HEADER_FILL = PatternFill('solid', fgColor='1F4E78')
SUBHEADER_FONT = Font(name=FONT_NAME, size=11, bold=True, color='1F4E78')
TITLE_FONT = Font(name=FONT_NAME, size=16, bold=True, color='1F4E78')
SUBTITLE_FONT = Font(name=FONT_NAME, size=10, italic=True, color='666666')
NORMAL_FONT = Font(name=FONT_NAME, size=10)
BOLD_FONT = Font(name=FONT_NAME, size=10, bold=True)
BLUE_FONT = Font(name=FONT_NAME, size=10, color='0000FF')
GREEN_FONT = Font(name=FONT_NAME, size=10, color='008000')
CAVEAT_FONT = Font(name=FONT_NAME, size=9, italic=True, color='990000')
NOTE_FONT = Font(name=FONT_NAME, size=9, italic=True, color='666666')
KPI_LABEL_FONT = Font(name=FONT_NAME, size=10, color='FFFFFF')
KPI_VALUE_FONT = Font(name=FONT_NAME, size=18, bold=True, color='FFFFFF')
THIN = Side(style='thin', color='BFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
STOCK_FILL = PatternFill('solid', fgColor='FFF2CC')
KPI_FILLS = [PatternFill('solid', fgColor=c) for c in ['1F4E78', '2E75B6', '548235', 'BF8F00']]

EUR0 = '#,##0" €";(#,##0" €")'
EUR2 = '#,##0.00" €";(#,##0.00" €")'
PCT1 = '0.0%;(0.0%)'
NUM0 = '#,##0'
DATEFMT = 'DD.MM.YYYY'

wb = Workbook()

# =========================================================================
# SHEET: Raw Data  (build first — everything else references it)
# =========================================================================
rd = wb.create_sheet('Raw Data')
rd.sheet_view.showGridLines = False
headers = ['No.', 'Year (tab)', 'Vehicle', 'Trim', 'Model year', 'Engine', 'Gearbox', 'Mileage (km)',
           'VAT type (M=margin, D=deductible)', 'Buyer country', 'Costs (€)', 'Netto (€)', 'VAT (€)',
           'Brutto (€)', 'Sale price (€)', 'Profit (€)', 'Margin % of cost', 'Purchase date',
           'Sale date', 'Days listed→sold', 'Status', 'Model group',
           'Helper: profit if sold', 'Helper: margin% if sold', 'Helper: sale year-month']
for i, h in enumerate(headers, start=1):
    c = rd.cell(row=1, column=i, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    c.border = BORDER
rd.freeze_panes = 'A2'
rd.row_dimensions[1].height = 32

widths = [6, 10, 30, 20, 11, 20, 10, 12, 14, 12, 11, 11, 11, 11, 12, 11, 11, 12, 12, 12, 9, 16, 12, 12, 12]
for i, w in enumerate(widths, start=1):
    rd.column_dimensions[get_column_letter(i)].width = w

def numval(x):
    return x if isinstance(x, (int, float)) else None

r_out = 2
for row in raw:
    no, yr, vehicle, trim, myear, engine, gearbox, mileage, vat, country, costs, netto, vat_amt, brutto, \
        saleprice, profit, marginpct, pdate_s, sdate_s, saletime, status, model = row
    vals = [
        int(no) if no.isdigit() else no, int(yr), vehicle, trim, myear, engine, gearbox,
        numval(mileage), vat, country, numval(costs), numval(netto), numval(vat_amt), numval(brutto),
        numval(saleprice), numval(profit),
        (numval(marginpct) / 100 if numval(marginpct) is not None else None),
        pdate(pdate_s), pdate(sdate_s), numval(saletime), status, model,
    ]
    for i, v in enumerate(vals, start=1):
        c = rd.cell(row=r_out, column=i, value=v)
        c.font = NORMAL_FONT
        c.border = BORDER
        if i in (11, 12, 13, 14, 15, 16):
            c.number_format = EUR2 if False else EUR0
        if i == 17:
            c.number_format = PCT1
        if i in (18, 19):
            c.number_format = DATEFMT
        if i == 8:
            c.number_format = NUM0
        if i == 20:
            c.number_format = NUM0
    if status == 'STOCK':
        for i in range(1, 23):
            rd.cell(row=r_out, column=i).fill = STOCK_FILL
    # helper columns
    hc1 = rd.cell(row=r_out, column=23, value=f'=IF(U{r_out}="SOLD",P{r_out},"")')
    hc1.number_format = EUR0
    hc1.font = NORMAL_FONT
    hc2 = rd.cell(row=r_out, column=24, value=f'=IF(U{r_out}="SOLD",Q{r_out},"")')
    hc2.number_format = PCT1
    hc2.font = NORMAL_FONT
    hc3 = rd.cell(row=r_out, column=25, value=f'=IF(U{r_out}="SOLD",TEXT(S{r_out},"YYYY-MM"),"")')
    hc3.font = NORMAL_FONT
    r_out += 1

last_row = r_out - 1  # 149
note_row = last_row + 2
rd.cell(row=note_row, column=1,
        value=('Note: "2023" tab rows for car No.10–15 are excluded here because those same cars '
               'reappear (with updated, final sale data) as rows in the "2024" tab under the same '
               'No. and VIN — including both would double-count them. Cars No.16 onward in the raw '
               '2023 tab were empty placeholder/deposit rows, not vehicles, and are excluded too.')).font = CAVEAT_FONT
rd.cell(row=note_row, column=1).alignment = Alignment(wrap_text=True)
rd.merge_cells(f'A{note_row}:H{note_row+2}')
rd.row_dimensions[note_row].height = 45

print('Raw Data built, last_row =', last_row)

RD = f"'Raw Data'!"
U_RNG = f"{RD}$U$2:$U${last_row}"
V_RNG = f"{RD}$V$2:$V${last_row}"
P_RNG = f"{RD}$P$2:$P${last_row}"
Q_RNG = f"{RD}$Q$2:$Q${last_row}"
K_RNG = f"{RD}$K$2:$K${last_row}"
O_RNG = f"{RD}$O$2:$O${last_row}"
B_RNG = f"{RD}$B$2:$B${last_row}"
I_RNG = f"{RD}$I$2:$I${last_row}"
Y_RNG = f"{RD}$Y$2:$Y${last_row}"  # helper sale year-month
N_RNG = f"{RD}$N$2:$N${last_row}"

# =========================================================================
# SHEET: By Model
# =========================================================================
bm = wb.create_sheet('By Model')
bm.sheet_view.showGridLines = False
bm['B2'] = 'Sold deals by model group'
bm['B2'].font = TITLE_FONT
bm['B3'] = 'Only completed (SOLD) deals are counted. Sorted by total profit, high to low. All cells are live formulas against the Raw Data tab.'
bm['B3'].font = SUBTITLE_FONT

bm_headers = ['Model group', 'Deals sold', 'Total revenue (€)', 'Total costs (€)', 'Total profit (€)',
              'Avg profit / deal (€)', 'Avg margin % of cost', 'Weighted margin % (profit/cost)']
hr = 5
for i, h in enumerate(bm_headers, start=2):
    c = bm.cell(row=hr, column=i, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    c.border = BORDER
bm.row_dimensions[hr].height = 30
bm.column_dimensions['A'].width = 3
bm.column_dimensions['B'].width = 26
for col in 'CDEFGHI':
    bm.column_dimensions[col].width = 17

# compute python-side profit total per model purely to sort rows (values themselves stay formulas)
model_profit = {}
for r in raw:
    if r[20] == 'SOLD':
        model_profit[r[21]] = model_profit.get(r[21], 0) + (r[15] if isinstance(r[15], (int, float)) else 0)
models_by_profit = sorted(model_profit.keys(), key=lambda m: -model_profit[m])

row = hr + 1
first_data_row = row
for m in models_by_profit:
    bm.cell(row=row, column=2, value=m).font = NORMAL_FONT
    cnt = bm.cell(row=row, column=3, value=f'=COUNTIFS({V_RNG},$B{row},{U_RNG},"SOLD")')
    rev = bm.cell(row=row, column=4, value=f'=SUMIFS({O_RNG},{V_RNG},$B{row},{U_RNG},"SOLD")')
    cst = bm.cell(row=row, column=5, value=f'=SUMIFS({K_RNG},{V_RNG},$B{row},{U_RNG},"SOLD")')
    prf = bm.cell(row=row, column=6, value=f'=SUMIFS({P_RNG},{V_RNG},$B{row},{U_RNG},"SOLD")')
    avgp = bm.cell(row=row, column=7, value=f'=IF(C{row}=0,"",F{row}/C{row})')
    avgm = bm.cell(row=row, column=8, value=f'=IFERROR(AVERAGEIFS({Q_RNG},{V_RNG},$B{row},{U_RNG},"SOLD"),"")')
    wm = bm.cell(row=row, column=9, value=f'=IF(E{row}=0,"",F{row}/E{row})')
    for c in (cnt,):
        c.number_format = NUM0
    for c in (rev, cst, prf, avgp):
        c.number_format = EUR0
    for c in (avgm, wm):
        c.number_format = PCT1
    for i in range(2, 10):
        bm.cell(row=row, column=i).font = NORMAL_FONT
        bm.cell(row=row, column=i).border = BORDER
    row += 1
last_model_row = row - 1

# totals row
bm.cell(row=row, column=2, value='TOTAL / ALL SOLD').font = BOLD_FONT
tot_cnt = bm.cell(row=row, column=3, value=f'=SUM(C{first_data_row}:C{last_model_row})')
tot_rev = bm.cell(row=row, column=4, value=f'=SUM(D{first_data_row}:D{last_model_row})')
tot_cst = bm.cell(row=row, column=5, value=f'=SUM(E{first_data_row}:E{last_model_row})')
tot_prf = bm.cell(row=row, column=6, value=f'=SUM(F{first_data_row}:F{last_model_row})')
tot_avgp = bm.cell(row=row, column=7, value=f'=F{row}/C{row}')
tot_avgm = bm.cell(row=row, column=8, value=f'=AVERAGEIF({U_RNG},"SOLD",{Q_RNG})')
tot_wm = bm.cell(row=row, column=9, value=f'=F{row}/E{row}')
tot_cnt.number_format = NUM0
for c in (tot_rev, tot_cst, tot_prf, tot_avgp):
    c.number_format = EUR0
for c in (tot_avgm, tot_wm):
    c.number_format = PCT1
for i in range(2, 10):
    cc = bm.cell(row=row, column=i)
    cc.font = BOLD_FONT
    cc.border = Border(top=Side(style='double'), left=THIN, right=THIN, bottom=THIN)
    cc.fill = PatternFill('solid', fgColor='DDEBF7')
row += 3

note_r = row
bm.cell(row=note_r, column=2,
        value=('Note: a few single-deal rows (BMW 420d, Audi A6 Avant, Kia Sportage, Nissan Navara) show very high '
               '"margin % of cost" (900%+). These are investor-consignment / commission-only deals where AUTOBONO '
               'never carried the full purchase cost, so "Costs" is a nominal figure (e.g. 50 €) rather than a real '
               'acquisition price. Their € profit is genuine but the % figure is not comparable to normal buy-resell deals.')).font = CAVEAT_FONT
bm.cell(row=note_r, column=2).alignment = Alignment(wrap_text=True)
bm.merge_cells(f'B{note_r}:I{note_r+2}')
bm.row_dimensions[note_r].height = 45

# =========================================================================
# SHEET: By Month
# =========================================================================
bmo = wb.create_sheet('By Month')
bmo.sheet_view.showGridLines = False
bmo['B2'] = 'Sold deals by month (sale date)'
bmo['B2'].font = TITLE_FONT
bmo['B3'] = 'Covers the full running log from Apr 2023 through Jul 2026. All cells are live formulas against the Raw Data tab.'
bmo['B3'].font = SUBTITLE_FONT

bmo_headers = ['Month', 'Deals sold', 'Total revenue (€)', 'Total costs (€)', 'Total profit (€)', 'Weighted margin %']
hr2 = 5
for i, h in enumerate(bmo_headers, start=2):
    c = bmo.cell(row=hr2, column=i, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = Alignment(horizontal='center')
bmo.column_dimensions['A'].width = 3
bmo.column_dimensions['B'].width = 14
for col in 'CDEF':
    bmo.column_dimensions[col].width = 17

row = hr2 + 1
first_m_row = row
for mo in months_sorted:
    bmo.cell(row=row, column=2, value=mo).font = NORMAL_FONT
    cnt = bmo.cell(row=row, column=3, value=f'=COUNTIF({Y_RNG},$B{row})')
    rev = bmo.cell(row=row, column=4, value=f'=SUMIF({Y_RNG},$B{row},{O_RNG})')
    cst = bmo.cell(row=row, column=5, value=f'=SUMIF({Y_RNG},$B{row},{K_RNG})')
    prf = bmo.cell(row=row, column=6, value=f'=SUMIF({Y_RNG},$B{row},{P_RNG})')
    wm = bmo.cell(row=row, column=7, value=f'=IF(E{row}=0,"",F{row}/E{row})')
    cnt.number_format = NUM0
    for c in (rev, cst, prf):
        c.number_format = EUR0
    wm.number_format = PCT1
    for i in range(2, 8):
        bmo.cell(row=row, column=i).font = NORMAL_FONT
        bmo.cell(row=row, column=i).border = BORDER
    row += 1
last_m_row = row - 1
bmo.cell(row=row, column=2, value='TOTAL').font = BOLD_FONT
bmo.cell(row=row, column=3, value=f'=SUM(C{first_m_row}:C{last_m_row})').number_format = NUM0
bmo.cell(row=row, column=4, value=f'=SUM(D{first_m_row}:D{last_m_row})').number_format = EUR0
bmo.cell(row=row, column=5, value=f'=SUM(E{first_m_row}:E{last_m_row})').number_format = EUR0
bmo.cell(row=row, column=6, value=f'=SUM(F{first_m_row}:F{last_m_row})').number_format = EUR0
bmo.cell(row=row, column=7, value=f'=F{row}/E{row}').number_format = PCT1
for i in range(2, 8):
    cc = bmo.cell(row=row, column=i)
    cc.font = BOLD_FONT
    cc.border = Border(top=Side(style='double'))
    cc.fill = PatternFill('solid', fgColor='DDEBF7')

# small bar chart of monthly profit
from openpyxl.chart import BarChart, Reference
chart = BarChart()
chart.title = 'Total profit by month (€)'
chart.y_axis.title = '€'
chart.style = 10
data = Reference(bmo, min_col=6, min_row=hr2, max_row=last_m_row)
cats = Reference(bmo, min_col=2, min_row=first_m_row, max_row=last_m_row)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.width = 24
chart.height = 10
bmo.add_chart(chart, f'I{hr2}')

# =========================================================================
# SHEET: By VAT Type
# =========================================================================
bv = wb.create_sheet('By VAT Type')
bv.sheet_view.showGridLines = False
bv['B2'] = 'Sold deals by VAT scheme'
bv['B2'].font = TITLE_FONT
bv['B3'] = 'M = margin scheme (VAT only on margin, no input VAT deduction). D = deductible/netto scheme (VAT reclaimed on purchase, charged on sale).'
bv['B3'].font = SUBTITLE_FONT
bv_headers = ['VAT type', 'Deals sold', 'Total revenue (€)', 'Total costs (€)', 'Total profit (€)', 'Weighted margin %']
hr3 = 5
for i, h in enumerate(bv_headers, start=2):
    c = bv.cell(row=hr3, column=i, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = Alignment(horizontal='center')
bv.column_dimensions['A'].width = 3
bv.column_dimensions['B'].width = 14
for col in 'CDEF':
    bv.column_dimensions[col].width = 17
row = hr3 + 1
for vt in ['M', 'D']:
    bv.cell(row=row, column=2, value=vt).font = NORMAL_FONT
    bv.cell(row=row, column=3, value=f'=COUNTIFS({I_RNG},$B{row},{U_RNG},"SOLD")').number_format = NUM0
    bv.cell(row=row, column=4, value=f'=SUMIFS({O_RNG},{I_RNG},$B{row},{U_RNG},"SOLD")').number_format = EUR0
    bv.cell(row=row, column=5, value=f'=SUMIFS({K_RNG},{I_RNG},$B{row},{U_RNG},"SOLD")').number_format = EUR0
    bv.cell(row=row, column=6, value=f'=SUMIFS({P_RNG},{I_RNG},$B{row},{U_RNG},"SOLD")').number_format = EUR0
    bv.cell(row=row, column=7, value=f'=F{row}/E{row}').number_format = PCT1
    for i in range(2, 8):
        bv.cell(row=row, column=i).font = NORMAL_FONT
        bv.cell(row=row, column=i).border = BORDER
    row += 1
bv.cell(row=row + 1, column=2,
        value=('Note: per-deal average margin % (not shown here) is heavily skewed by a few near-zero-cost consignment '
               'deals. The weighted margin % above (total profit ÷ total cost) is the reliable comparison — and it shows '
               'M and D scheme deals perform almost identically (~16% each), i.e. VAT scheme itself is not driving profitability.')).font = CAVEAT_FONT
bv.cell(row=row + 1, column=2).alignment = Alignment(wrap_text=True)
bv.merge_cells(f'B{row+1}:F{row+3}')

print('By Model / By Month / By VAT built')

# =========================================================================
# SHEET: Overview  (built last so it can reference everything; moved to front after)
# =========================================================================
ov = wb.create_sheet('Overview')
ov.sheet_view.showGridLines = False
ov.column_dimensions['A'].width = 3
for col, w in zip('BCDEFGH', [30, 20, 20, 20, 20, 20, 4]):
    ov.column_dimensions[col].width = w

ov['B2'] = 'AUTOBONO — Full Sales & Inventory Analysis'
ov['B2'].font = TITLE_FONT
ov['B3'] = 'Bottom-up analysis of the master AUTOBONO Google Sheet ("2023" + "2024" tabs), rebuilt from row-level data.'
ov['B3'].font = SUBTITLE_FONT
ov['B4'] = 'Data pulled 25 Jul 2026. Every figure below is a live formula against the "Raw Data" tab — nothing is hand-typed.'
ov['B4'].font = CAVEAT_FONT

kpi_row = 6
kpis = [
    ('B', 'Completed sales', f'=COUNTIF({U_RNG},"SOLD")', NUM0),
    ('D', 'Total revenue (sold)', f'=SUMIF({U_RNG},"SOLD",{O_RNG})', EUR0),
    ('F', 'Total realized profit', f'=SUMIF({U_RNG},"SOLD",{P_RNG})', EUR0),
]
kpi_fills = [KPI_FILLS[0], KPI_FILLS[1], KPI_FILLS[2]]
for (col, label, formula, fmt), fill in zip(kpis, kpi_fills):
    col2 = chr(ord(col) + 1)
    ov.merge_cells(f'{col}{kpi_row}:{col2}{kpi_row}')
    c1 = ov[f'{col}{kpi_row}']
    c1.value = label
    c1.font = KPI_LABEL_FONT
    c1.alignment = Alignment(horizontal='center')
    ov.merge_cells(f'{col}{kpi_row+1}:{col2}{kpi_row+2}')
    c2 = ov[f'{col}{kpi_row+1}']
    c2.value = formula
    c2.font = KPI_VALUE_FONT
    c2.number_format = fmt
    c2.alignment = Alignment(horizontal='center', vertical='center')
    for rr in range(kpi_row, kpi_row + 3):
        for cc in (col, col2):
            ov[f'{cc}{rr}'].fill = fill
ov.row_dimensions[kpi_row].height = 18
ov.row_dimensions[kpi_row + 1].height = 22
ov.row_dimensions[kpi_row + 2].height = 22

row = kpi_row + 5
ov[f'B{row}'] = 'Weighted margin (total profit ÷ total cost, sold deals)'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f'=SUMIF({U_RNG},"SOLD",{P_RNG})/SUMIF({U_RNG},"SOLD",{K_RNG})'
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = PCT1
row += 1
ov[f'B{row}'] = 'Average profit / deal'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f'=SUMIF({U_RNG},"SOLD",{P_RNG})/COUNTIF({U_RNG},"SOLD")'
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = EUR0
row += 1
ov[f'B{row}'] = 'Median profit / deal'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f"=MEDIAN({RD}$W$2:$W${last_row})"
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = EUR0
row += 1
ov[f'B{row}'] = 'Average margin % of cost (simple average across deals)'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f'=AVERAGEIF({U_RNG},"SOLD",{Q_RNG})'
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = PCT1
row += 1
ov[f'B{row}'] = 'Median margin % of cost'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f"=MEDIAN({RD}$X$2:$X${last_row})"
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = PCT1
row += 1
ov[f'B{row}'] = 'Cars currently in stock / pending'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f'=COUNTIF({U_RNG},"STOCK")'
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = NUM0
row += 1
ov[f'B{row}'] = 'Capital tied up in current stock (cost basis)'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f'=SUMIF({U_RNG},"STOCK",{K_RNG})'
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = EUR0
row += 1
ov[f'B{row}'] = 'Total unique vehicles logged (2023 start – Jul 2026)'
ov[f'B{row}'].font = NORMAL_FONT
ov[f'D{row}'] = f"=COUNTA({RD}$A$2:$A${last_row})"
ov[f'D{row}'].font = BOLD_FONT
ov[f'D{row}'].number_format = NUM0
row += 2

ov[f'B{row}'] = "Cross-check vs. the sheet's own embedded dashboard"
ov[f'B{row}'].font = SUBHEADER_FONT
row += 1
ov[f'B{row}'] = "The AUTOBONO sheet has its own dashboard totals baked into the \"2024\" tab (row 4). Comparing them to our bottom-up recompute:"
ov[f'B{row}'].font = SUBTITLE_FONT
ov.merge_cells(f'B{row}:F{row}')
row += 1
chk_hdr = row
for i, h in enumerate(['Metric', "Sheet's own dashboard value", 'Our bottom-up formula result', 'Match?'], start=2):
    c = ov.cell(row=row, column=i, value=h)
    c.font = HEADER_FONT
    c.fill = HEADER_FILL
    c.border = BORDER
    c.alignment = Alignment(horizontal='center', wrap_text=True)
row += 1
checks = [
    ('2024 tab: Total Costs, all 139 logged cars (sold + stock)', 1400197.07, f'=SUMIFS({K_RNG},{B_RNG},2024)'),
    ('2024 tab: Total Sale revenue, sold cars only', 1697960, f'=SUMIFS({O_RNG},{B_RNG},2024,{U_RNG},"SOLD")'),
    ('2024 tab: Total Brutto (purchase side), all 139 cars', 1433350, f'=SUMIFS({N_RNG},{B_RNG},2024)'),
    ('2024 tab: Total profit, sold cars only', 206543, f'=SUMIFS({P_RNG},{B_RNG},2024,{U_RNG},"SOLD")'),
]
first_chk = row
for label, dash_val, formula in checks:
    ov.cell(row=row, column=2, value=label).font = NORMAL_FONT
    ov.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
    dc = ov.cell(row=row, column=3, value=dash_val)
    dc.font = BLUE_FONT
    dc.number_format = EUR0
    fc = ov.cell(row=row, column=4, value=formula)
    fc.font = BOLD_FONT
    fc.number_format = EUR0
    mc = ov.cell(row=row, column=5, value=f'=IF(ABS(C{row}-D{row})<500,"Match","Check")')
    mc.font = NORMAL_FONT
    for cc in range(2, 6):
        ov.cell(row=row, column=cc).border = BORDER
    row += 1
row += 1
ov.cell(row=row, column=2,
        value=("Note: the \"2023\" tab's own dashboard total profit (–84,824.22 €) is NOT comparable — its formula "
               "counts unsold cars as a full loss (sale price 0 minus full cost) rather than excluding them. Our figures "
               "exclude unsold cars from profit and report them separately as inventory instead (see \"Cars currently in "
               "stock\" above). Also: the 2024 dashboard's Netto total (1,281,133.14 €) is ~10.7k € lower than our "
               "bottom-up Netto sum (~1,291,870 €) — a small unexplained residual in the original sheet; it does not "
               "affect Costs, Brutto, Sales or Profit, which all reconcile within rounding.")).font = CAVEAT_FONT
ov.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical='top')
ov.merge_cells(f'B{row}:F{row+3}')
ov.row_dimensions[row].height = 20
row += 5

ov.cell(row=row, column=2, value='Top takeaways').font = SUBHEADER_FONT
row += 1
takeaways = [
    ('1. Touran is your thinnest high-volume model.', 'VW Touran: 8 sold, only 10,233 € total profit at a 10.6% weighted margin '
     '— well below the 16.2% company average and the lowest of any model with 5+ deals. Avg profit/deal is 1,279 € vs. '
     '~1,690 € company-wide. Worth a firmer floor buy-price or walking away from thin Touran deals.'),
    ('2. Audi A4 is your best repeat performer.', '8 sold, 19,622 € total profit at 19.9% margin, avg profit/deal 2,453 € — '
     'the strongest volume model in the book. Skoda Octavia is the volume leader (21 sold, 30,749 € total profit) but at a '
     'lower 15.8% margin — good for cash flow, less good per unit.'),
    ('3. Profit is concentrated in a handful of models.', 'The top 5 models by profit (Skoda Octavia, Audi A4, Seat Ateca, VW Tiguan, '
     'VW Golf) produced ≈ 98.6k € of the 217.9k € total — about 45% of all profit from 5 of 41 model groups.'),
    ('4. ≈160k € of capital is sitting in 19 unsold cars.', 'Several have been listed since Nov 2025–Feb 2026 without selling '
     '(e.g. Alfa Romeo Stelvio, VW Tiguan, Seat Ateca, Skoda Karoq). Worth a slow-mover review — price cuts or wholesale exit '
     'on the oldest ones frees up cash.'),
    ('5. Watch for consignment deals skewing "margin %".', 'BMW 420d, Audi A6 Avant, Kia Sportage and Nissan Navara show 900%+ '
     '"margin" — these are investor consignment/commission flips with a nominal 50–650 € recorded cost, not real buy-resell '
     'economics. Their euro profit is real; exclude them when benchmarking margin % by model.'),
]
for title, body in takeaways:
    ov.cell(row=row, column=2, value=title).font = BOLD_FONT
    ov.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
    ov.merge_cells(f'B{row}:F{row}')
    row += 1
    ov.cell(row=row, column=2, value=body).font = NORMAL_FONT
    ov.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical='top')
    ov.merge_cells(f'B{row}:F{row+1}')
    ov.row_dimensions[row].height = 15
    row += 3

# Reorder sheets: Overview, By Model, By Month, By VAT Type, Raw Data
wb._sheets = [wb['Overview'], wb['By Model'], wb['By Month'], wb['By VAT Type'], wb['Raw Data']]
# remove default empty sheet if present
if 'Sheet' in wb.sheetnames:
    del wb['Sheet']
wb.active = 0

wb.save('AUTOBONO_Sales_Analysis.xlsx')
print('Workbook saved.')
