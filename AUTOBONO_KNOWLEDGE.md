# AUTOBONO – working knowledge for Claude

Condensed from every conversation in `Communication/` (June–September 2026). Read this before doing price analyses (PA) or business maths for AUTOBONO. The full transcripts are the source of truth if anything here is unclear.

## The business
- **AUTOBONO s.r.o.**, used-car dealer in **Nitra, Slovakia**. Two owners, 50/50: Samuel and his colleague/partner.
- Mostly VAG (VW, Škoda, Seat, Audi), plus Mazda, Alfa Romeo, Mercedes, some EVs. Typical buy €7k–18k.
- Listings: **autobono.autobazar.eu** and **bazos.sk** (always both, paid/boosted on bazos). A pro photographer takes every photo.
- Sourcing: auctions/B2B platforms (e.g. CarOnSale), bazos, imports (DE/AT/IT/FR/NL), private sellers.
- Its edge is trust: a published, honest **technical report** for every car. Clean, full-history cars over cheap risky ones. "We sell certainty, not excitement."
- **Funding model:** each car is funded by an investor (Samuel or the colleague, separately). Net profit per car is split **50/50 between the investor and the company**. The two partners also each own 50 % of the company.
- Samuel runs a parallel company so he can buy directly at auctions. That avoids paying the 0.4 % bank-transaction tax (max €40 per payment) twice.
- Samuel's spreadsheets are in **Google Drive/Sheets** (not Numbers or Excel). There is an "AUTOBONO" economics sheet and a separate scoreboard sheet (Tabuľka1).

## Standing rules Samuel has set (always apply)
1. **Margin car by default.** Treat a car as margin (no VAT deduction) unless Samuel says "netto", "VAT car" or "VAT-deductible".
2. **Margin-VAT maths:** VAT = (sale price − **supplier purchase price**) × 23/123. Prep costs do **not** reduce the VAT base. Net profit = sale − total costs − margin VAT.
3. **Netto / VAT-deductible maths:** net profit = sale ÷ 1.23 − net total cost.
4. **"Usual costs" = €200** per car (listing, oil and filter, transaction tax, small fees), unless Samuel gives a number.
5. **Never pool facelift and pre-facelift cars as comps**, in any model, even at the same mileage or year. Check the facelift boundary before using a comp. Also check the generation (Mk3 vs Mk4 and so on), body style (Combi/ST/Variant vs hatchback; Samuel prefers comparing combi to combi), power tier (85 vs 110 vs 140 kW), gearbox (DQ200 dry-clutch vs DQ381 wet-clutch DSG vs manual) and drivetrain.
6. **Exclude AUTOBONO's own ads** (seller "AUTOBONO", Nitra, on bazos) from comp sets. Every car is listed on both sites, so its own ads show up in searches.
7. Leave **AAA Auto** out of comps (they have their own pricing rules). When pricing a manual, don't use DSG comps unless asked to.
8. **P2P / personal cars:** when Samuel buys a car privately for himself (for example the Stelvio), no VAT scheme applies. Profit = sale − cost. This applies only to cars he names, not as a general rule.
9. **Consignment ("komisionálny predaj"):** the profit pool (sale − customer's base − costs) is split 50/50 with the customer, with no VAT.
10. Use **net** profit, not gross, for monthly-return comparisons.
11. Samuel's messages are short ("PA:", "invest 9060"). Read them carefully. Don't swap which car a number belongs to (this happened with Leon vs Karoq on 27.09).
12. Challenge his reasoning when the data supports it, but take transacted sales and his market knowledge seriously. Listing prices that are too low look suspicious and get fewer viewings. "Clean" comps are only the seller's claim.

## Acquisition Scoreboard v1.0 (designed with ChatGPT, used for every car)
- **Step 1, NO-GO gate** (any one = pass): structural or serious accident, legal or document problem, major known defect, price can't support the minimum profit.
- **Step 2, score 11 criteria 0/1/2** (max 22): service history, paint/body, technical condition, equipment quantity, spec attractiveness (LED, DSG, 4x4, camera…), expected trading profit, market demand, holding period, mileage vs age, inventory overlap, technical-report confidence.
  - Expected profit (net): **2 = >€2,500 · 1 = €1,700–2,500 · 0 = <€1,700**. Keep these thresholds fixed. 2026 margins are lower, so accepting 1-point deals more often is a *policy* choice, not a rule change.
  - Holding period: 2 = <45–60 days · 1 = 60–90 · 0 = >90.
  - Inventory overlap: ask "does a similar car in stock materially raise risk (is it stagnant?)", not "do we already have one?" (the Karoq lesson).
- **Step 3, zero rule:** 0–1 zeros → GO · 2 zeros → RECONSIDER · 3+ zeros → PASS.
- **Step 4, override:** a one-sentence justification is required. Also log "Biggest risk" and "Selling advantage".
- Paint thickness: under about 220 µm reads as a minor repaint, such as keying.
- Score on the realistic **settle** price, not the asking price.

## Key numbers
- **Sales history** (129 sales Apr 2023 – Jul 2026, from Samuel's sheet): €217.9k profit, 16.2 % weighted margin.

  | Year | Sold | Avg profit/car | Weighted margin | Median days listed→sold |
  |---|---|---|---|---|
  | 2024 | 40 | €1,815 | 16.4 % | 24.5 |
  | 2025 | 52 | €1,739 | 17.5 % | 33 |
  | 2026 to 25.07 | 29 | €1,505 | 15.6 % | 42 |

  Jan–Jul 2026 vs the same period of 2025: −15 % in volume, −28 % in profit. In 2026, more than €2k net per car counts as a very good sale.
- Best repeat models: Audi A4 (19.9 % margin), Octavia, Ateca, Tiguan, Golf. Touran has the thinnest margins (about 10.6 %) but sells fast and predictably.
- **Fixed costs:** €1,148.99/month excluding VAT (garage €515, ELAMI €200, AB.eu €99.83, HU plates €83.33, PZP €54.58, electricity €42.82, Carprofit Club €40.65, Carsonsale €39, Skool €26.50, Partslink24 €23, e-vignette €12.20, Kros €7.09, Jablotron €4.99). With a buffer: about **€15.6k/year**, so roughly 16–18 cars/year to break even for the company.
- **Capital deployment:** 59.7 % on 07.08.2026, including the partner's idle loan. Target band 75–90 %; below 70 % leaves money on the table. Average cash cycle is **84 days**. A rough rule: about €2k gross per €10k per cycle.
- **Samuel personally:**
  - Loans: €14,296.94 left at €551.68/month (28 payments left), and €20,532.61 left at €295.28/month (86 of 96 left; the rate drops 1 %/year after each 12 payments). That is €846.96/month.
  - Living costs: about €960/month (apartment €220, ETF €360, life insurance €130, clothes €50, food/social €200).
  - Total need: **≈ €21.7k/year**. His share was €8k in 2025 (11 cars) and €8,168 in 2026 by mid-September (9 cars). He's short of that, so he's partly living on loan principal.
  - The fix is more volume from his own funded stock (about 24 cars/year at about €900 share each), not just cheaper cars. The company's distributable profit is a flexible extra.

## Lessons from past deals
- **White Karoq (missed):** he hesitated because of overlapping stock and the car sold to someone else, a lost ~€2k. Apply the same discipline to saying yes as to saying no.
- **Stelvio 2.2 JTD (bent rod):** bought €11,700, about €3k engine work, €500 registration, sold €14,900 after **300 days**. A €615 loss plus about €3.5k of missed turnover, so about €4.1k in total. Engine risk costs time, not just the repair bill.
- **Octavia 1.5 TSI consignment:** 130 days, the cosmetic problems were never fixed properly, €553 share. Cosmetically borderline cars kill thin-margin fast flips.
- **Black Touran 1.4 TSI:** enquiry 2 h after listing, sold the next day for €13,500, 31 days purchase→sale, about €2,020 net. The model for the "capital velocity" idea.
- Fresh timing belt or DSG oil service is a concrete selling point worth a higher price.
- EVs: **SoH matters more than mileage** (roughly €500–800 per SoH point on the ID.4). Get an Aviloo test. Some sellers sell ex-lease VAT EVs as margin cars (tax evasion), which makes their prices hard to beat when you do it properly.
- Samuel corrected several of Claude's estimates (Passat, Karoq, Touran, Superb facelift). Weight transacted sales and his comps heavily, and say plainly when a comp set is thin.
- Alfa 2.2 JTD oil pressure: VCDS and the Alfa read **absolute** pressure (subtract 1 bar). Healthy is about 2.6–2.7 bar hot idle and 5.5–6 bar at revs (absolute). A low-pressure Stelvio was fixed by **replacing the oil filter cap and filter** (MANN).

## Stock and open items (as of 29.09.2026 – check with Samuel, this goes out of date)
- **Listed 18.09:**
  - Mazda CX-3 2.0 AT 2016, €13,190
  - Mercedes E53 AMG Kombi 2023, €62,990 incl. VAT
  - Mercedes GLC 300d 2021, €35,900 incl. VAT
  - Seat Ateca 2.0 TDI Xcellence 4Drive 2017, €14,190
  - Golf Variant 2.0 TDI 2017, €12,490 incl. VAT
  - Passat Variant 2.0 TDI 4Motion manual 2016, €13,490. Cost about €9.7k; the advice was to advertise at €12,990.
  - Tiguan 2.0 TDI DSG 2013, €12,490
  - Tiguan 2.0 TDI manual 2011, €10,690 (above market)
  - Gold Touran Highline 2016, €14,490 (cost €10,325)
- **Sold Sep 2026:** Karoq 2019 for €16,000 (net €2,474), Ateca 1.6 TDI for €11,700 (net €1,854), Stelvio for €14,900, Leon ST 2018 for €12,000.
- **Bought:**
  - Black Touran Comfortline 2.0 TDI 7-seat 2016 (25.08, €9,765 + €200, target list €13,000)
  - Superb L&K 147 kW 4x4 2022 (01.09, €18,500 P2P, estimated list €25.5–26.5k)
- **Samuel's own stock (15.09):** winter car €2,900, BMW €4,300, Ibiza Cupra 1.8 TSI €11,500.
- **Pending at end of chat (29.09):**
  - Superb III Combi 2.0 TDI Style manual 2016 auction (planned €10,060; comfortable to about €11,600, hard stop about €12,600)
  - Leon ST 1.5 TSI Style 2019 (€9,060 + €400)
  - Passat B8 Variant 2.0 TDI Comfortline 2016 (€8,613 + €200)
  - Karoq 1.5 TSI Style 2018 (€12,660, tight)
  - Leon 1.5 hatch 2019 (€8,930 netto, thin)
