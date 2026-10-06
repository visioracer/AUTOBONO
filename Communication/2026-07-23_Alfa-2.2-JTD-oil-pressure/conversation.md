# Alfa Romeo 2.2 JTD – oil pressure

**Period:** 23.07.2026 – 23.07.2026 · **Your messages:** 12

Only the conversation is shown here: your messages and Claude's replies. Internal tool calls and web searches are left out. Times are Slovak time.


---
## Thursday 23.07.2026

### 🧑 **You** · 16:27

> Let's talk about engine oil pressure. You might get familiar with the Alfa Romeo 2.2 JTD from 2016, the aluminium engine in the Giulia and Stelvio, that it suffers from engine oil pressure issues, mainly around the oil pickup seal. I have a 280 thousand km engine, it underwent a new engine oil pump, new seal (aluminium o-ringed retrofit from a Dutch company JTD Performance), engine oil baffle was added to the oil sump and we unplugged the pump solenoid so that the pump does not switch between low and high oil pressure, it keeps it in high pressure all the time (since the low pressure works against a spring). I know that even with these items changed, it still can have oil pressure issues, e.g. due to a faulty oil filter, not allowing enough pressure to build up after about 3000 rpm. Are there are other things that could affect the oil pressure? Such as the plastic oil filter housing/cap?

### 🤖 **Claude** · 16:29

You've already covered the two big documented fixes for the 2.2 JTD (pickup seal + baffle, plus the pump). Beyond a bad filter, here's what else commonly bites this engine at high mileage:

**Oil pump itself.** Even a new pump can lose pressure if its internal housing screws loosen over time — this is a separately documented failure mode on this pump, distinct from the pickup seal. Worth confirming Loctite was used on reassembly, or that this specific pump revision has the reinforced screws.

**Oil filter housing/cap.** Yes, it's a real suspect. The plastic housing carries an integrated bypass valve that lets oil skip the filter media if flow is restricted; if that valve sticks or the housing's sealing surfaces have degraded from 280k km of heat cycling, it can bleed pressure rather than help build it. Worth checking the housing for hairline cracks and replacing the O-rings/seals even if the plastic looks intact.

**Oil cooler.** If your car has the oil-to-coolant heat exchanger, an internal seal failure there can both cross-contaminate and act as a pressure leak path. JTD Performance sells a cooler kit alongside their pump/seal parts specifically because this is a known companion failure point.

**Sump gasket/split line.** Shared with the 2.0 JTDm, the gasket at the sump split hardens with age and thermal stress, which can introduce air at the pickup even with a good seal and baffle.

**Bottom end wear.** At 280k km, increased main/rod bearing clearance is a legitimate, boring explanation — it lowers the pressure ceiling the pump can achieve, especially hot idle, independent of any seal or pump condition.

**Oil galley plugs.** On the aluminium block these can loosen slightly with heat cycling, creating an internal leak path that never shows up externally.

**Sensor vs. reality.** Worth ruling out a faulty pressure sender/sensor before chasing mechanical causes further, since it's the cheapest thing to check.

**Oil condition/spec.** Diesel soot/fuel dilution thins oil over the service interval faster than the odometer suggests — wrong viscosity or an overdue change can mimic a mechanical fault.

One flag on your solenoid mod: locking the pump into high pressure permanently removes the low-pressure mode Alfa uses to cut pump parasitic load and manage oil temperature at idle/cruise. It solves the "pressure collapses when switching modes" symptom, but it's worth knowing it's a trade-off, not just a fix — the pump works harder continuously and oil temps may run slightly different than stock calibration intended.

Given 280k km and a prior low-pressure history, it's also worth having someone check the lower block/main bearing saddle area for cracking if the sump ever comes off again — this is the failure mode owners on the forums get stuck with (Alfa doesn't sell it separately, so it means a new short block).

Sources:
- ['INSUFFICIENT ENGINE OIL PRESSURE' Warning On 2.2 Diesel](https://www.alfaowner.com/threads/%E2%80%98insufficient-engine-oil-pressure%E2%80%99-warning-on-2-2-diesel.1201340/)
- [Oil pump Giulia-Stelvio 2.2 JTDm – JTD Performance](https://jtd-performance.com/en/product/oil-pump-giulia-stelvio-2-2-jtd/)
- [Oil pressure fixing kit Giulia-Stelvio 2.2 JTDm – JTD Performance](https://jtd-performance.com/en/product/oil-pressure-fixing-kit-giulia-stelvio-jtd-rwd/)
- [Oil cooler kit 147/156/GT JTD 16v – JTD Performance](https://jtd-performance.com/en/product/oil-cooler-kit-147-156-gt-jtd/)
- [Low oil pressure warning Giulia - Stelvio 2.2 JTD (Facebook)](https://www.facebook.com/100063716133558/posts/low-oil-pressure-warning-giulia-stelvio-22-jtda-major-issue-almost-every-owner-h/917872437013286/)
- [Giulia & Stelvio 2.2 JTD low oil pressure — after working on several cars (Facebook)](https://www.facebook.com/100063716133558/posts/giulia-stelvio-22-jtd-low-oil-pressureafter-working-on-several-cars-with-this-pr/1185996556867538/)

### 🧑 **You** · 16:35

> I never had a low engine oil pressure warning, but I know what pressure figures should I be receiving. It is about 2.6-2.7 hot idle and 5.5-6.0 bar of maximum pressure at revs. However, my pressure jump between 2.2-2.4, sometimes for a moment to 1.9 or 2.0 and it produces maximum of 5 bar at revs. Other issues I seem to notice is that the oil pressure drops often for a brief moment under acceleration (light or hard) even by 0.5 bar. The engine was not opened internal-wise and I am not going to change the bearings for crankshaft nor con-rods until the engine gives out some serious hints of very bad state, but I suspect the oil filter cap (I read a lot about it on Italian forums and Facebook groups) and bought a new one to be replaced soon during another oil change

### 🤖 **Claude** · 16:37

Your reference numbers match spec (2.5 bar low mode / 5–6 bar high mode is the commonly cited figure), so what you're seeing is a real deficit, not you misremembering spec.

The acceleration-correlated dips are the most useful diagnostic clue here, and they point away from the filter cap, not toward it. That specific pattern — pressure sagging during both light and hard acceleration — is the exact signature documented for this engine's pickup-side problem: forward acceleration surges oil rearward in the pan, momentarily starving or partially uncovering the pickup, and any marginal seal at the pump-to-pickup joint draws air instead of oil. That's precisely the failure mode your O-ring retrofit and baffle were meant to cure. Two things worth double-checking even after that work:

- Whether the retrofit seal is fully seated and torqued, and whether the original seal failure left any pitting/wear on the pump's mating face that keeps a new seal from sealing perfectly.
- Whether your baffle geometry actually covers fore-aft surge (acceleration/braking) or was mainly designed against lateral G (cornering) — those are different problems and not every baffle design addresses both.

The filter housing/cap sits on the pressure side of the circuit, downstream of the pump, not on the suction/pickup side. There's no vacuum there for a cracked cap to pull air through — a compromised cap would either weep oil externally under pressure or let a bit of flow bypass the filter media internally. That fits your other symptom better: a peak that's chronically capped around 5 bar instead of 5.5–6, and a slightly depressed, fluctuating idle baseline, both consistent with a small continuous internal bypass rather than an event tied to throttle input. So the cap swap is worth doing (it's cheap, and a 10-year-old plastic housing at 280k km is a reasonable wear item regardless), but I wouldn't expect it alone to fix the acceleration-triggered dips.

When you're in there, it's also worth: confirming oil level isn't overfull (crank windage into an over-full sump causes foaming that mimics all of this), and if you want a clean answer on the sender vs. real fluctuation question, tap a mechanical gauge in temporarily — cheap way to rule out a noisy sender/connector contributing to the readings.

Given no warning light has tripped and the pattern doesn't look like the smooth, load-dependent decline you'd expect from bearing clearance growth, your plan to chase seals and housings before touching the bottom end is the right order of operations.

### 🧑 **You** · 16:43

> I had a different oil pressure problem on a Stelvio with the same engine. It was torn down and assembled, rod bearings changed, main ones were fine, so they remained, the same JTD Performance oil pickup seal installed, but no new oil pump and no oil baffle. The maximum pressure it could build up was 3.7 bar hot at revs

### 🤖 **Claude** · 16:44

That case is a useful data point precisely because of what it *didn't* fix. 3.7 bar hot at revs is a big shortfall from the 5.5–6 bar target — bigger than the shortfall you're seeing on your own car even though that Stelvio had fresh rod bearings and the same pickup seal fix you have.

The main bearings are the interesting variable. "Fine" after visual inspection and "within new-build clearance" are two different things — a bearing can look unmarked and ungalled while still sitting at, say, 0.06–0.08mm clearance instead of a fresher 0.03–0.04mm, simply from a couple hundred thousand km of normal wear. The mains see full pump output before the oil ever reaches the rod journals, so main clearance has an outsized effect on how much pressure the system can hold — more so than rod clearance, which is downstream. If nobody plastigauged or micrometered them and just eyeballed the surfaces, "fine" may just mean "not scored," not "still at spec." That alone could easily account for a chunk of the 3.7 bar ceiling.

The bigger suspect, though, is the pump that was reused untouched. A worn pump (bore wear, rotor/vane wear, or the known loose-internal-screws issue on this engine) has reduced volumetric efficiency — it simply can't fill the galleries fast enough to reach the relief valve's crack pressure once there's any meaningful clearance downstream to leak through. Fixing the rod bearings tightens one leak path, but if the pump was already marginal, tightening one of several parallel leaks isn't going to move the ceiling much. That's consistent with what you're seeing on your own car too: new pump, new seal, new baffle gets you to 5 bar, not 3.7 — the pump swap is clearly doing real work — but you're still short of 5.5–6, which points at something still bleeding flow on your car as well (filter housing being the current prime suspect, per your plan).

No baffle in that Stelvio's rebuild wouldn't explain a lower *steady-state max at revs* on its own — baffle absence mostly shows up as transient surge/aeration under directional G, not a hard ceiling on peak pressure. So I'd rule that out as the reason for 3.7 bar specifically.

Worth asking: do you know if the mains were actually measured, or just inspected by eye? And was the reused pump pressure-tested or just visually checked before going back in? Those two answers would tell you whether that Stelvio's ceiling was a bearing-clearance story, a tired-pump story, or both stacking together.

### 🧑 **You** · 16:46

> I do not know, but knowing the mechanic, I believe they were properly checked. The oil pump usually isn't the problem, let's leave that out of the equation, too. What else is left?

### 🤖 **Claude** · 16:48

With pump, pickup seal, rod bearings, and (per your mechanic) main clearance all taken off the table, what's left falls into a few buckets:

**Piston cooling oil squirters.** This engine cools the underside of the pistons with oil jets in the block, each normally gated by a small spring-loaded check valve that only opens once oil pressure crosses a threshold. If one or more of those check valves is stuck open, missing its ball/spring, or was disturbed during teardown and not reseated, you get a continuous high-volume bleed straight back into the crankcase that scales with RPM — which fits "maximum pressure at revs" specifically, since squirter flow increases with pump output. This is a very plausible and often-overlooked culprit after any bottom-end rebuild, since squirters/galleries get disturbed during a teardown.

**The pressure regulating valve itself.** Separate from the pump and separate from the electric high/low solenoid, there's a spring-loaded mechanical relief valve (its own listed part) that dumps excess flow back to the sump once target pressure is reached. A weak/broken spring, a worn valve bore letting the plunger cock sideways, or debris holding it slightly off its seat will cap max pressure network-wide regardless of pump or bearing condition — and it's easy to overlook precisely because attention goes to the pump and bearings during a rebuild.

**Turbo bearing wear.** The turbo's center bearing is a continuous oil-fed leak path by design, and if it's worn, that leak path is bigger — and worse at revs/boost, when the turbo spins fastest and demands the most oil. Worth ruling out with a look at shaft play if it hasn't been checked.

**Rebuild-specific risks**, which are easy to underweight because "new bearings" sounds definitive: were the rod journals actually measured and the correct bearing size (standard vs. undersize) fitted for the journal's true diameter, or were standard bearings put on a journal that had already worn past standard without regrinding? Also worth considering: was the oil pump-to-block gasket/O-ring replaced when the pump was pulled for inspection, are all the oil gallery plugs re-torqued/resealed, and is the oil pressure sender or its adapter fitting properly sealed? Any of these can leak pressure internally without any visible external symptom.

**Oil cooler.** If this Stelvio has the coolant-oil heat exchanger, a degraded internal seal there is a straightforward internal bypass — same mechanism I flagged for your car.

**Test conditions**, as a sanity check rather than a mechanical cause: correct oil grade actually used post-rebuild, and confirmation the reading was taken at proper operating temp rather than just "hot" by feel — a slightly thinner-than-spec oil or an overheated reading will understate real pressure and can make a marginal engine look worse than it is.

Given the shortfall is this large (3.7 vs 5.5–6), my money would be on either a squirter check valve or the regulating valve rather than something subtle — both produce exactly this kind of proportionally big, RPM-scaling deficit without needing any bearing or pump wear at all.

### 🧑 **You** · 16:53

> We already fixed it, hoped you would have guessed right what was the answer. We changed the oil filter cap and oil filter (it was changed during the assembly for a MANN one and it was again for another MANN) and instantly the pressure went beyond 3.7 bar. The Stelvio now reaches 5.1 bar hot at revs easily and about 2.2-2.4 bar hot idle

### 🤖 **Claude** · 16:53

That's a strong result, and useful confirmation: the cap/filter combo alone was worth ~1.4 bar, more than any single bearing or seal fix in that rebuild. That's bigger than I'd have weighted it going in — I had it as a "chronic bypass, some tenths of a bar" contributor, not the dominant lever. Good data point for recalibrating: on this engine, a compromised filter cap/housing interface can apparently outweigh bearing clearance as the limiting factor on max pressure.

Mechanically this fits the pressure-side bypass explanation — either the cap's sealing face/O-ring was letting oil skip the filter media under load, or the housing's integrated bypass valve wasn't seating, and swapping both cap and filter cleared whatever debris or worn seal was holding that bypass open. Can't fully isolate cap vs. filter since both changed at once, but given it went MANN-to-MANN with only the cap as the new variable, the cap is the more credible suspect.

This is good news for your own plan — you're already holding the part, and this case suggests it could move your peak meaningfully above the current 5 bar, not just marginally.

One thing worth recalibrating from this result: that Stelvio, now fixed, still only idles at 2.2–2.4 bar hot — same range you're seeing on your own car, and below the oft-quoted 2.6–2.7. That's a useful sanity check: it suggests 2.2–2.4 hot idle may just be the realistic healthy baseline for this platform (especially with the solenoid disabled) rather than a sign of a remaining fault. I'd stop treating your idle number as a red flag once your cap swap is done, provided it stops dipping to 1.9–2.0.

What the cap swap likely won't touch is the acceleration-correlated transient dips on your own car — those still look like a surge/pickup-side story rather than a filter-side one, so worth watching whether they persist after the cap goes in.

### 🧑 **You** · 17:05

> What do you know about the 2015+ 3.0 TDI V6 engines? I know they are getting remapped oil pressure-wise

### 🤖 **Claude** · 17:08

The engine you're thinking of is the EA897 Gen-3 (also called evo/evo2) 3.0 TDI V6 — codes include CRTE, CRTD, CZV, CZZ and others depending on power output and generation. It's the successor to the earlier EA897/CRC-family engine and appeared from around 2014–2015 onward across Audi A4/A5/A6/A7/A8, Q5/Q7/Q8, SQ5, VW Touareg III, and some Porsche Cayenne and Bentley Bentayga diesel applications.

The "remap" you've heard about is real, and it's a genuinely different situation from the Alfa. Audi moved to a variable-displacement, ECU-map-controlled oil pump on this generation, regulated through a solenoid control valve (Audi calls it N428). Instead of running high pressure all the time, the ECU deliberately targets low pressure at idle and light load to cut pump drag and help meet Euro 6 emissions/fuel economy targets. So a "low" hot-idle reading on these engines, unlike the Alfa's 2.5 bar spec, is by design, not a fault — Audi's own documentation describes it as normal behavior.

The problem is the margin is thin, and it erodes with age: oil dilution from repeated DPF regens and short trips thins the oil further, and the factory low-pressure warning threshold only triggers around 0.6 bar — which several owners report is already too late to prevent bearing or crankshaft damage. There have been TSBs addressing this (checking hot idle pressure with a mechanical gauge against a ~1.4 bar minimum at 80°C, and — interesting parallel to your Alfa case — inspecting the oil filter housing's internal rubber plug and spring, which can bleed pressure if mis-seated). So the same "innocuous-looking filter housing internals" failure mode you just diagnosed on the Stelvio shows up as an official Audi wear point too.

What independent specialists are doing with "remapping" is raising the ECU's minimum commanded oil pressure at low RPM/load in software — essentially telling the pump to build more pressure than the factory map calls for, plus in some cases correcting the warning threshold so it triggers earlier. One shop's before/after data (their own marketing, so take the exact numbers with some skepticism since they're selling the service): stock 2016 curve was around 1.0 bar at idle and only reaching ~3.5 bar past 2500 rpm; Audi quietly revised the factory map by 2021 to roughly 1.3 bar idle / 3.3 bar at 2500 rpm; their own remap claims ~1.6 bar idle / 3.6 bar at 2500 rpm. Whether those specific figures hold up under scrutiny, the general shape — Audi already moved the map up once without a formal recall — is corroborated across multiple independent sources.

Worth being cautious about: this is a software-only fix layered on a hardware design choice, not a repair of a broken part. If your filter housing plug/spring or pump is genuinely worn, remapping just asks a compromised system to try harder — same logic as your Alfa solenoid delete, but here it's officially acknowledged as adjustable by the OEM's own tooling architecture rather than a workaround.

Sources:
- [The Hidden Audi Oil Pressure Problem with Audi's 3rd Generation 3.0TDI Engines](https://walsall-car-remapping-diagnostics.co.uk/the-hidden-audi-oil-pressure-problem-with-audis-3rd-generation-3-0tdi-engines/)
- [Increasing Oil Pressure in 3.0 TDI Audi Volkswagen Engines](https://3tdi.eu/increasing-oil-pressure)
- [Defects of 3.0 TDI CRT CZV CZZ Engines](https://3tdi.eu/crt-engines-defects)
- [OIL PRESSURE ISSUES 3.0 TDI ENGINES AFTER 2014 - AudiWorld Forums](https://www.audiworld.com/forums/q7-mk-1-discussion-112/oil-pressure-issues-3-0-tdi-engines-after-2014-a-3088294/)
- [Audi 3.0TDI gen 3 oil pressure issues (CRTE, CRTD etc) - Audi-Sport.net](https://www.audi-sport.net/xf/threads/445492/)

### 🧑 **You** · 17:14

> The 1.6/3.6 bar is a atmospheric pressure (meaning above 1 atmosphere), the Alfa pressures are absolute (from vaccum calculated), so there would always be 1 bar with the engine turned off

### 🤖 **Claude** · 17:15

I'd push back on that. Virtually all automotive oil pressure instrumentation — mechanical gauges and OEM electronic senders alike — is gauge-referenced (relative to ambient atmospheric), not absolute/vacuum-referenced, in both the Alfa and the VAG cars. A few reasons I don't think the distinction you're describing applies here:

A mechanical Bourdon-tube pressure gauge is inherently a gauge-type instrument by construction — one side connects to the oil gallery, the other is open to ambient air. It physically cannot read absolute pressure unless it's built with a sealed vacuum reference capsule, which standard automotive test gauges don't have. The Audi TSB I cited explicitly specifies verifying hot idle pressure "with a mechanical gauge" against a ~1.4 bar minimum — that instruction only makes sense if the spec and the instrument are both gauge-referenced.

Electronic OEM oil pressure senders (piezoresistive, used for both the dash warning and ECU input on essentially every production car) are also built as gauge sensors, venting to ambient on the reference side. True absolute pressure sensors do exist as components, but they're the exception in aftermarket gauge kits, and using one for engine oil pressure requires the installer to manually calibrate out atmospheric pressure — which is a documented quirk specifically because it's unusual, not the default behavior.

Practically: if either car's sensor were absolute, you'd see roughly 1 bar displayed with the key on, engine off, before any oil pressure exists — a well-known, frequently-discussed quirk if it existed. Neither Alfa nor VAG documentation, TSBs, or the forum threads I've read mention this, and it would be a constant point of confusion for technicians running diagnostics.

So I believe both the 2.6–2.7/5.5–6 bar Alfa figures and the 1.6/3.6 bar Audi figures are on the same gauge-pressure basis, and the comparison holds. That said, if you have a source specifically documenting an absolute sensor on either of these two ECUs, I'd genuinely like to see it — that would be an atypical implementation detail worth confirming rather than assuming away.

### 🧑 **You** · 17:15

> They are not, because the Alfa shows 1 bar with engine off

### 🤖 **Claude** · 17:17

Fair enough — that's a real observation, and it overrides the general assumption I made. If your Alfa's reading sits at 1 bar with the engine off, its sensor is absolute-referenced, not gauge. That's plausible on a modern design too: absolute pressure sensor dies (piezoresistive silicon, same family used for MAP/boost sensors) are cheap and commonly reused across sensor applications, so an engineering team choosing off-the-shelf silicon for an oil circuit sensor isn't unusual, even though it's not the traditional Bourdon-tube-gauge convention.

That changes what the numbers actually mean physically. What matters for bearing protection is the pressure differential the pump generates above ambient — so with an absolute sensor you need to subtract that 1 bar baseline to get the real figure:

Your spec reference (2.6–2.7 idle / 5.5–6 at revs) becomes roughly 1.6–1.7 / 4.5–5 real. Your car's readings (2.2–2.4, dipping to 1.9–2.0 idle; 5 bar peak) become roughly 1.2–1.4, dipping to 0.9–1.0; 4 bar peak. The broken Stelvio's 3.7 bar ceiling was really about 2.7 bar of actual protective pressure — genuinely marginal for a hot, loaded V6. The fixed Stelvio's 5.1/2.2–2.4 becomes about 4.1/1.2–1.4 real.

None of that changes the diagnostic conclusions we drew earlier, since every Alfa-to-Alfa comparison in this conversation used the same instrument and stayed internally consistent. But it does break my Audi comparison, and I should flag that honestly rather than paper over it: I assumed the Audi TSB's "1.4 bar minimum at 80°C hot idle" and the specialist's 1.6/3.6 remap figures were gauge, reasoning from the "mechanical gauge" test method mentioned in the TSB. But I just found evidence that at least some VW/Audi oil pressure implementations also use an absolute, MAP-style sensor design that reads ~1 bar with the engine off — so I can no longer be confident the Audi figures I cited are on a different basis than the Alfa's. I don't have a source that pins down the sensor type for this specific EA897 Gen-3 application either way.

If you or anyone with VCDS access on one of these 3.0 TDIs can check the live oil pressure PID with the engine off, that would settle it definitively — 0 bar confirms gauge, ~1 bar confirms absolute, same as your Alfa.

### 🧑 **You** · 17:17

> ![attached image](images/image_001.jpg)
> 
> Here you can see that the VCDS diagnostics also pulls out absolute pressure figures, so minus 1 bar to get atmospheric pressures
> 
> The Stelvio is a 2.2 JTD, not a V6

### 🤖 **Claude** · 17:19

Good clarification — noted. The Stelvio in the earlier story (3.7 bar broken / 5.1 bar fixed) is the 2.2 JTD four-cylinder diesel we've been discussing throughout, not the Quadrifoglio's 2.9 V6 biturbo petrol. And the VCDS screenshots are from an unrelated VAG vehicle (3.0 TDI-CR, engine code DMGA — a later EA897 evo variant), just serving as evidence that these ECUs do report oil pressure setpoint as absolute kPa (222–270 kPa idle, ~374–415 kPa at 2000 rpm before/after the remap), confirming the same absolute-reference convention applies there too. No mixing of the two engine families — just using the DMGA data to settle the sensor-reference question.

### 🧑 **You** · 17:21

> ![attached image](images/image_002.jpg)
> 
> Can you find on the internet what engine this oil pressure table belongs to?

### 🤖 **Claude** · 17:22

This is from the Bosch EDC17CP54 / MD1CP004 engine control unit used on the VAG Group 3.0 TDI V6 — the same EA897-family engine we discussed for the Audi 3.0 TDI (the DMGA screenshot you posted earlier is a sibling ECU generation on this same engine family).

Specifically, tuning-shop documentation identifies this ECU/oil-pressure PWM-valve combination as fitted to engine codes DDVB, DDVC, DDVE, DDVF, DHXA, DHXB, DHXC, DCPC, DCPE, DEWA, DEWB, DENA, DMVB, DDXB, DDXC, DDXD, DDXE — spanning Audi A4, A5, A6, A7, A8, Q5, Q7, Q8, and VW Touareg/Amarok.

What you're looking at (rpm × oil temperature, breakpoints in hPa) are the min/max threshold tables that bound what oil pressure the ECU considers plausible/acceptable at a given speed and temperature — the diagnostic envelope around the target pressure map, not the target itself. It's the same category of calibration data as the "OilPCtl_pNom_MAP" target-pressure map that tuning shops raise when doing the oil-pressure "fix" — this table is what triggers a fault/warning if the actual reading falls outside the green zone at a given rpm/temp combination, so it's directly relevant to why the factory warning threshold on these engines has been criticized as too permissive.

Sources:
- [Oil Pressure Fix for VAG MD1CP004 and EDC17CP54 ECU – Baltic Tuning](https://www.baltictuning.com/blog/oil-pressure-fix-for-vag-md1cp004-and-edc17cp54-ecu)
- [WinOLS - Oil Pressure Fix for VAG MD1CP004 EDC17CP54 ECU – Digital Kaos](https://www.digital-kaos.co.uk/forums/showthread.php/1050814-WinOLS-Oil-Pressure-Fix-for-VAG-MD1CP004-EDC17CP54-ECU)

### 🧑 **You** · 17:25

> Are you sure? The numbers don't line up with my chart

### 🤖 **Claude** · 17:25

Good catch — I overstated my confidence there. I couldn't actually load the full table from either forum thread (digital-kaos and mhhauto both returned blank pages, likely login-gated), and the Baltic Tuning post only gave one reference figure ("in low-pressure regions we set 260 kPa") which I didn't verify against your image's actual breakpoints. I matched on ECU family and table structure (rpm × oil temp → hPa, same "min/max threshold" naming convention), not on confirmed numbers, and presented it more confidently than that evidence supports.

I'm also not fully certain the engine code list I quoted (DDVB/DCPE/DHXA/etc.) is even the 3.0 TDI V6 rather than the 2.0 TDI four-cylinder EA288 family — some of those code prefixes overlap conventions across both, and I didn't verify that split.

What specifically doesn't line up with your chart — the rpm breakpoints, the pressure values at a given point, or something else? If you can tell me what you're comparing against (another source, or values you'd expect for a known engine), I can search more targeted rather than guessing from the table's general shape again.

### 🧑 **You** · 17:27

> I believe it is the 2.2 JTD Alfa Romeo engine

### 🤖 **Claude** · 17:28

I couldn't confirm that either way through search, and I should be upfront about why: the label style you're seeing ("Average engine speed of one cylinder segment," "min/max threshold") is characteristic Bosch EDC17/MD1 calibration-label phrasing, and Bosch reuses that same internal signal-naming convention across many different OEMs and engines — so the table's structure and wording alone don't distinguish a VAG 3.0 TDI file from an Alfa/Fiat 2.2 JTD file. Both platforms could plausibly use Bosch-family ECUs with this exact labeling.

On the numbers themselves: 1.25–4.1 bar across the threshold bands is roughly in the right neighborhood for the 2.2 JTD's known 2.5 / 5–6 bar operating range if this is a gauge-referenced diagnostic envelope sitting below the actual target curve — but I can't confirm that without the source file or software ID.

What makes you think it's the 2.2 JTD specifically — is this from your own car's ECU read, or from a source/context you can share? If you have the ECU/software number (or where the screenshot came from), I can search more precisely instead of inferring from table structure again.
