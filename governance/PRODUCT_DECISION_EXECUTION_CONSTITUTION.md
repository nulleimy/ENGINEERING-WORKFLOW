---
id: EW-CONSTITUTION-PDRE-001
title: Product, Decision and Execution Constitution
status: proposed
owner: Eimy Herrer and Johny
version: 1.0.0-rc2
last-reviewed: 2026-07-26
normative-language: cs
technical-constitution-sha256: ed44c6147049887d941b7497f1bce3b817f22b6ae00a5136a27365a2f688d918
related: WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md; ENGINEERING_CONSTITUTION.md; GOVERNANCE_MODEL.md
---

# PRODUKTOVÁ, ROZHODOVACÍ A REALIZAČNÍ ÚSTAVA

## 0. Účel a vztah k technické ústavě

Tato ústava určuje, **co má produkt být, kdo smí rozhodnout, jak se rozhodnutí převádí do práce a jak se důkazně pozná přijatý výsledek**.

Nenahrazuje `WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md`. Technická ústava řídí technickou pravdivost, source-of-truth pořadí, pracovní režimy, bezpečnost, DevOps, testování, Definition of Done a chráněné operace. Její závazný SHA-256 je:

```text
ed44c6147049887d941b7497f1bce3b817f22b6ae00a5136a27365a2f688d918
```

Tato ústava doplňuje produktovou hodnotu, rozhodovací pravomoci, realizační disciplínu, Definition of Ready, Release Ready, Operational Ready, adoption, conformance a měření dlouhodobé hodnoty.

Při konfliktu platí vyšší autorita; při stejné autoritě bezpečnější a důkazně přísnější požadavek. Nejasnost je `BLOCKED`.

## 1. Pořadí autority

1. závazná právní, bezpečnostní, smluvní a platformní pravidla;
2. `WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md`;
3. tato Produktová, rozhodovací a realizační ústava;
4. explicitní mandát oprávněného operátora;
5. projektová governance, přijaté ADR/RFC a autorizované Work Packages;
6. pracovní dokumentace a nástrojové konfigurace;
7. nezdokumentované předpoklady člověka nebo AI.

Produktová autorita rozhoduje **co a proč**. Engineering autorita rozhoduje **zda a jak** lze výsledek vytvořit bezpečně a udržitelně. Security autorita může blokovat porušení bezpečnostních invariantů. Release autorita může blokovat nedoložené nebo neobnovitelné vydání.

Rozhodnutí samo neopravňuje k merge, release, změně licence, změně veřejného API, force push, destruktivní operaci, rotaci secrets ani produkční změně. Chráněnou operaci provádí pouze oprávněný operátor v povoleném režimu.

## 2. Závazné stavy

Používej pouze pravdivé stavy:

- `PROPOSED` — navrženo, neschváleno;
- `ACCEPTED` — přijato oprávněnou autoritou;
- `IMPLEMENTED` — skutečně změněno;
- `VERIFIED` — doloženo ověřitelným důkazem;
- `PARTIALLY_VERIFIED` — ověřena je pouze přesně vymezená část;
- `INFERRED` — odvozeno, nikoliv přímo prokázáno;
- `UNKNOWN` — chybí podklad;
- `BLOCKED` — nelze bezpečně nebo oprávněně pokračovat;
- `EXCEPTED` — existuje řízená, vlastněná a expirovaná výjimka;
- `DEPRECATED` / `RETIRED` — schopnost je ukončována / ukončena.

`COMPLETE` je povoleno jen po splnění všech relevantních acceptance criteria, gate, dokumentace, evidence a recovery požadavků.

## 3. Produktová pravda

Každý podporovaný projekt má jednu aktuální Product Definition obsahující:

- cílového uživatele nebo provozního zákazníka;
- problém a současnou alternativu;
- primární hodnotu a hlavní scénář;
- měřitelnou definici úspěchu;
- hranice, non-goals a unsupported oblasti;
- Product a Engineering Authority;
- bezpečnostní, datovou a provozní klasifikaci;
- podmínky nahrazení nebo retirementu.

Bez této definice je práce discovery nebo experiment, nikoliv potvrzený produktový vývoj.

Funkce se nevytváří jen proto, že je technicky zajímavá, módní, snadno generovatelná AI nebo používaná konkurencí. Významná schopnost musí doložit uživatele, problém, jednodušší alternativy, úspěch, náklady, rizika a způsob odstranění.

## 4. Produktové principy

1. Uživatel a problém před technologií.
2. Jedna jasná hlavní hodnota před množstvím funkcí.
3. Nejmenší úplný vertikální řez před rozsáhlou rozpracovaností.
4. Nativní jednoduchost před integračním divadlem.
5. Bezpečné výchozí chování před dodatečným zabezpečením.
6. Měřitelný výsledek před pocitem pokroku.
7. Odstranitelnost před nevratným lock-inem.
8. Provozní realita před prezentačním prototypem.
9. Dlouhodobé vlastnictví před anonymním kódem.
10. Pravdivý stav před optimistickým reportem.

Každá trvalá komponenta má účel, vlastníka, kontrakt, závislosti, provozní náklad, bezpečnostní klasifikaci, ověření, upgrade a retirement podmínky.

## 5. Experimenty

Experiment musí mít hypotézu, omezený scope, maximální trvání, měřítko úspěchu a zastavení, pravidla pro data, vlastníka a rozhodnutí `PROMOTE`, `REVISE`, `STOP` nebo `ARCHIVE`.

Experiment se nesmí stát produkční součástí pouhým uplynutím času.

## 6. Rozhodovací třídy

- **D0 — ústavní:** poslání, autorita, vlastnictví, licence, bezpečnostní invarianty, minimální assurance a produkční autorizace;
- **D1 — strategické / obtížně vratné:** veřejné API, datový model s migrací, autentizace, hlavní provider, zásadní architektura nebo dlouhodobý lock-in;
- **D2 — průřezové:** více komponent, týmů nebo provozních oblastí;
- **D3 — lokální implementační:** vratné, izolované, bez změny veřejného kontraktu nebo významného rizika;
- **D4 — rutinní:** formátování, bezpečný refactor a automatizovaná údržba v předem schválených mezích.

D0–D2 vyžadují Decision Record. D3 může přijmout odpovědný implementátor uvnitř autorizovaného Work Package. D4 může být automatizováno, ale zůstává auditovatelné.

## 7. Povinný Decision Record

Významné rozhodnutí eviduje ID, třídu, stav, vlastníka, autoritu, problém, kontext, omezení, varianty, důkazy, přijatou variantu, důvod, bezpečnostní a provozní dopad, compatibility, migraci, rollback/safe-forward, nejistoty, dissent a review trigger.

Rozhodnutí má jednoho accountable ownera. Konsensus je preferovaný, ale nesmí vytvářet neomezený deadlock. Při neshodě se oddělí fakta, předpoklady a preference, určí se rozhodující důkaz, deadline a oprávněná autorita; dissent se zachová.

## 8. Výjimky

Výjimka má vlastníka, přesný scope, důvod, kompenzační kontrolu, začátek, expiraci, review authority a důkaz uzavření.

Tichá nebo trvalá výjimka je zakázána. Opakovaná výjimka spouští přezkum standardu nebo systémového problému. Pravdivost stavů, integrita evidence, ochrana secrets a explicitní autorizace chráněných operací nemají tichou výjimku.

## 9. Realizační lifecycle

```text
INTAKE → FRAME → CLASSIFY → DECIDE → SLICE → AUTHORIZE → IMPLEMENT → VERIFY → REVIEW → ACCEPT → RELEASE → OPERATE → LEARN
```

Technické režimy `AUDIT`, `DESIGN`, `IMPLEMENT`, `VERIFY` a `RELEASE` určují druh technické činnosti. Tento lifecycle určuje cestu změny od problému k provoznímu učení. Oba modely platí současně.

## 10. Work Package a vertikální řez

Každá významná implementace má Work Package s ID, vlastníkem, problémem/hodnotou, baseline, cílovým stavem, scope a out-of-scope, rizikem, dotčenými kontrakty, acceptance criteria, testovací strategií, security/observability dopadem, rolloutem, rollbackem/safe-forward a požadovanou evidencí.

Preferuje se nejmenší řez, který poskytuje ověřitelnou hodnotu, prochází nutnými vrstvami, je samostatně testovatelný, vratný a nezanechává skrytý manuální krok.

Rozpracovanost je omezená. Otevřený Work Package má další konkrétní krok; blocker má vlastníka a podmínku odblokování.

## 11. Definition of Ready

Práce je připravena k implementaci, když:

- problém a hodnota jsou srozumitelné;
- existuje vlastník a rozhodovací autorita;
- scope a out-of-scope jsou jasné;
- acceptance criteria jsou testovatelná;
- riziko a dotčené kontrakty jsou známé;
- závislosti a blockers jsou zjištěné;
- existuje způsob ověření a rollback/safe-forward;
- změna je dostatečně malá.

## 12. Definition of Done

Tato definice doplňuje technickou Definition of Done; požadavky jsou kumulativní.

Změna je hotová pouze tehdy, když existuje implementace, prošly relevantní build/lint/type/test/security gate, dokumentace odpovídá realitě, telemetry jsou přiměřené riziku, rollback/safe-forward je proveditelný, evidence je vytvořená, nejsou skryté manuální kroky, review je dokončeno a stav je pravdivě reportovaný.

## 13. Release Ready a Operational Ready

Release vyžaduje přesnou verzi a immutable baseline, digest artefaktů, SBOM, provenance, vulnerability/VEX rozhodnutí, podpis a ověření identity tam, kde je požadováno, release notes, compatibility/migraci, ověřený deployment a rollback a přijetí Release Authority.

Produkční služba vyžaduje vlastníka, service record, SLI/SLO, observabilitu, runbook, incidentní klasifikaci, backup/restore plán, skutečný restore test, kapacitní a nákladový model, security monitoring, podporovaný lifecycle a retirement plán.

Záloha bez restore testu není ověřená záloha.

## 14. Kvalita, bezpečnost a assurance

Cílový stav každé aplikovatelné domény je nejméně `9.0/10`. Dokument sám nemůže doložit 9/10. Navržená oblast má strop 5.0, implementovaná 7.0, interně ověřená 8.5, provozně měřená 9.5 a nezávisle posouzená 10.0.

Kritická kontrola používá defense-in-depth: prevenci, detekci, blokování, audit, obnovu, least privilege, integrity evidence a nezávislé review. Absolutní bezpečnost se netvrdí.

Při chybějícím kritickém důkazu nebo selhání bezpečnostního nástroje je stav `BLOCKED`, pokud neexistuje předem schválený bezpečný fallback. Tiché pokračování, snížení threshold nebo nezamčená alternativa jsou zakázané.

## 15. Reprodukovatelnost, open source a supply chain

Podporovaný projekt má uzamčené závislosti, deklarované runtime verze, deterministický bootstrap, idempotentní init, oddělené source/generated artefakty, čistý rebuild, upgrade, compatibility matrix a self-test.

Do repozitáře nepatří `__pycache__`, `.pyc`, build outputy, lokální secrets ani náhodné runtime artefakty.

Open-source nástroj se přijímá po posouzení licence, původu, maintenance, bezpečnostní historie, release integrity, compatibility, provozních nákladů, datových toků, lock-inu a exit strategie. Nástroj je adaptér; proces a evidence zůstávají přenositelné.

Produkční artefakt má podle profilu digest, SBOM, provenance, vulnerability vyhodnocení, VEX, podpis, ověření identity a retenční evidence. PR workflow nemá produkční signing authority.

## 16. AI-native engineering

AI může analyzovat, navrhovat, implementovat omezený řez, generovat testy a připravovat evidence.

Bez lidské autority nesmí měnit produktové poslání, přijmout vlastní změnu, snížit threshold, uzavřít vlastní finding, přijmout výjimku, získat trvalé privileged credentials, podepsat release, deklarovat certifikaci ani provést nevratnou produkční operaci.

Významná AI-assisted změna eviduje model/provider, kontext, povolené nástroje, zakázané operace, změny, kontroly, limity a lidské přijetí.

## 17. Instalovatelný engineering produkt

Nový projekt musí podporovat cestu:

```text
INSTALL → INIT → SELECT PROFILE → GENERATE → BOOTSTRAP → VERIFY → SELF-TEST → DEVELOP
```

Existující projekt musí podporovat:

```text
AUDIT → CLASSIFY → PLAN → PREVIEW → SNAPSHOT → APPLY → VERIFY → ACCEPT
```

Cílové CLI poskytuje ekvivalent `ew init`, `adopt`, `doctor`, `verify`, `diff`, `apply`, `rollback`, `evidence`, `conformance`, `release`, `upgrade` a `self-test`. Příkazy jsou idempotentní, auditovatelné a podporují `--dry-run`.

Golden path má compatibility matrix, generovaný projekt, bootstrap, lokální vývoj, testy, build, security, CI, release, observabilitu, runbook, upgrade, retirement a pravidelný end-to-end test.

Inicializace používá explicitní manifest cest, preview, snapshot, opakovatelnost, rollback a výslednou verifikaci; nesmí dělat neomezené textové náhrady ani upravovat binární/generované soubory.

## 18. Self-test a conformance

Instalace není ověřená bez self-testu, který vytvoří dočasný projekt, aplikuje profil, provede bootstrap, lint/test/build/security, vytvoří artefakt a SBOM, ověří evidence, uklidí prostředí a vrátí strojově čitelný výsledek.

Adoptovaný projekt vytváří conformance record s verzí ENGINEERING-WORKFLOW, profilem, požadovanými a ověřenými controls, výjimkami, blockers, důkazy, datem, vlastníkem a integrity digestem.

## 19. Metriky a učení

Měří se produktová hodnota, time-to-first-value, task success, retence a rework; delivery flow a DORA metriky; SLO, incidenty, restore testy, vulnerability age, výjimky, supply-chain coverage a ověřené releasy.

Metrika má účel, vlastníka, zdroj, interpretaci, ochranu proti gaming, review trigger a pravidlo odstranění. Metriky neslouží k hodnocení lidí podle objemu aktivity.

Po významné změně se vyhodnotí dosažená hodnota, rework, incidenty/near-misses, manuální kroky, nový dluh a potřebné změny golden pathu nebo controls.

## 20. Jediný zdroj pravdy a změna ústavy

Každá kritická informace má jeden kanonický zdroj. Chaty, dashboardy a tikety mohou zobrazovat nebo odkazovat na stav, ale nevytvářejí paralelní autoritu.

Změna této ústavy vyžaduje identitu návrhu, důvod, dopad, compatibility a security posouzení, migraci, oprávněnou autoritu, verzi, changelog a datum účinnosti. Nesmí nepřímo měnit technickou ústavu bez samostatné změny jejího souboru a nového integrity hashe.

Ústava se přezkoumává nejméně jednou za 90 dní a po závažném incidentu, selhání governance, zásadní produktové změně, nové externí normě, opakovaných výjimkách nebo prokazatelné nadměrné administrativě.

Povinný krok musí snižovat riziko, zrychlovat zpětnou vazbu, chránit hodnotu, vytvářet použitelný důkaz nebo umožnit obnovu. Jinak se automatizuje, slučuje nebo odstraňuje.

## Závěrečný invariant

```text
ŽÁDNÁ FUNKCE BEZ HODNOTY.
ŽÁDNÉ ROZHODNUTÍ BEZ VLASTNÍKA.
ŽÁDNÁ IMPLEMENTACE BEZ OVĚŘITELNÉHO CÍLE.
ŽÁDNÝ RELEASE BEZ DŮKAZŮ.
ŽÁDNÝ PROVOZ BEZ OBNOVY.
ŽÁDNÁ VÝJIMKA BEZ EXPIRACE.
ŽÁDNÉ TVRZENÍ BEZ PRAVDIVÉHO STAVU.
ŽÁDNÁ SLOŽITOST BEZ MĚŘITELNÉHO DŮVODU.
```
