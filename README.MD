


Here is the complete, fully updated **`README.md`** reflecting your new professional package architecture, your passing 28-test suite, and every grammatical feature you have implemented so far. 

You can copy and paste this directly into your `README.md` file in the root of your project.

***

```markdown
# 🕉️ skt-dhatu-parse (Paninian Sanskrit Engine)

## Overview
`skt-dhatu-parse` is a computational linguistics engine that implements Pāṇini’s *Aṣṭādhyāyī*. Rather than relying on static lookup tables or pre-conjugated dictionaries, this package calculates Sanskrit morphophonemics dynamically in real-time. 

It processes an abstract phonetic root (*Upadeśa*) and an abstract tense/mood marker (*Lakāra*) through a strict chronological state-machine of 2,500-year-old grammatical rules to generate mathematically perfect verbal paradigms.

It is designed to be fully `pip`-installable, highly usable as a standalone CLI tool, and importable as a Python library for advanced NLP applications.

---

## 📦 Installation & Quickstart

To install the engine locally in editable mode (recommended for development):
```bash
git clone https://github.com/yourusername/skt-dhatu-parse.git
cd skt-dhatu-parse
pip install -e .
```

### Command Line Interface (CLI)
Once installed, you can access the engine globally from your terminal using the Python module syntax. 

**Generate a full 3x3 conjugation table:**
```bash
python -m skt_dhatu_parse BU -l laW --table
```

**Generate a specific word and view Pāṇini's step-by-step derivation history:**
```bash
python -m skt_dhatu_parse BU -l lfW -p prathama -v 0 --history
```

**Handle Homonyms:**
If a root exists in multiple classes (like `div`), the engine warns you and auto-defaults to the most common Gaṇa. You can explicitly override this with `-g`:
```bash
python -m skt_dhatu_parse div -l laW -g 4 --table
```

### Python API
You can easily import the engine into your own Python applications:
```python
from skt_dhatu_parse.engine import derive

# Derive the 3rd person singular future tense of 'bhū'
prakriya = derive('BU', lakara_name='lfW', purusha='prathama', vacana=0, gana=1)

print(prakriya.get_current_string())  # Outputs: Bavizyati
prakriya.print_history()              # Prints the applied Sūtras
```

---

## 🛠️ Core Architecture & Design Decisions

1. **Encoding (SLP1):** The engine exclusively uses SLP1 (Sanskrit Library Phonetic Basic). This strictly maps exactly one phoneme to one ASCII character (e.g., `ṛ` = `f`, `ś` = `S`, `ṣ` = `z`), eliminating complex Unicode parsing errors and regex boundary issues.
2. **Database:** Powered by an indexed SQLite database (`dhatupatha.db`) for lightning-fast root lookups. 
3. **Composite Primary Keys:** Safely handles Sanskrit homonyms (e.g., `vid` in Gaṇa 2, 4, 6, and 7) by identifying roots via a composite key of `dhatu_slp1` + `gana`.
4. **State Machine (`Prakriya`):** Built on an Object-Oriented sequence of `Term` objects. Terms inherit tags and mutate in place via *Sthānivadbhāva* (State Inheritance).
5. **TDD (Test-Driven Development):** Guarded by a comprehensive 28-test `unittest` suite simulating boundary cases, class variations, and exact Paninian rule execution.

---

## 🚀 Grammatical Features Implemented (In Detail)

### 1. The Phonological Engine (`shivasutras.py`)
Dynamically queries the Sanskrit alphabet using Pāṇini's 14 Śivasūtras.
* **Pratyāhāras:** Generates arrays of phonemes dynamically (e.g., `ac` for vowels, `hal` for consonants, `ik`, `yaY`, `iR`).
* **The 'Ṇ' Edge-Case:** Handles Pāṇini’s duplicate `R` (ṇ) marker—`aR` stops at sutra 1; `iR`/`yaR` continue to sutra 6.

### 2. Meta-Marker Resolution / It-Lopa (`anubandha.py`)
Strips instructional markers (*anubandhas*) from roots and affixes while saving their grammatical implications as tags.
* **1.3.2 (upadeśe'janunāsika it):** Deletes nasalized vowels (`!` or `~`) and tags the term (e.g., `ahi!` -> `ah` + `idit`).
* **1.3.3 (hal antyam):** Deletes terminal consonants (`tip` -> `ti` + `pit`).
* **1.3.4 (na vibhaktau tusmāḥ):** Protects terminal `s`, `m`, and dentals in inflectional affixes (`tas`, `vas`, `mas`).
* **1.3.8 (laśakvataddhite):** Deletes initial `l`, `S`, and velars (`Sap` -> `a` + `Sit` + `pit`).

### 3. The Grammatical Rule Engine (`rules.py`)
Applies context-sensitive, chronologically ordered Pāṇinian Sūtras:
* **Lakāra Substitution:** (3.4.78) Replaces `laW` with 18 Tiṅ affixes. The new affix inherits properties from `laW` via rule 1.1.56.
* **Class Infixes (Vikaraṇas):** Dynamically inserts `Sap` (Gaṇa 1), `Syan` (Gaṇa 4), `Sa` (Gaṇa 6), or `sya` (Future tense).
* **Guṇa & Prevention:** (7.3.84) Strengthens `ik` vowels before *Sārvadhātuka* affixes (`BU` -> `Bo`). (1.1.5) Blocks Guṇa if the affix is `Nit` (which correctly handles Gaṇa 6 `tud`).
* **Sandhi (Phonetics):** 
    * 6.1.78: `eco'yavAyAvaH` (`Bo + a` -> `Bava`).
    * 6.1.97: `ato guNe` merges consecutive `a`'s.
    * 8.3.59: `AdeSapratyayayoH` dynamically changes `s` to `z` (ṣ) after `iR` vowels across both intra-term and cross-term boundaries (`jezyati`, `Bavizyati`).
    * 8.2.23: `saMyogAntasya lopaH` drops terminal consonants in clusters (`aBavant` -> `aBavan`).
    * 8.3.15: `rutva` converts terminal `s` to Visarga `H`.
* **Voice Morphing (Ātmanepada):** (3.4.79) `ta` -> `te`. (3.4.80) `TAs` -> `se`. (7.2.81) `a + Ate` -> `ete`.
* **Advanced Augments (Āgamas):** 
    * 7.1.58: `idito num dhAtoH` inserts nasal `m` inside `idit` roots (`ah` -> `aMh`).
    * 6.4.71: `aW` augment prefixes the root for Past Tense.
    * 3.4.101: `tasthasthamipāṃ...` Replaces dual/plural affixes for `laN`.
    * 7.2.35 & 7.2.10: Applies `iW` augment to `sya` for Future Tense, but actively **blocks** it for *Aniṭ* (anudātta) roots like `ji` (`jezyati`).

### 4. Verified Conjugations
The engine currently derives mathematically perfect 3x3 tables for:
* **Gaṇa 1 Parasmaipada:** `BU` -> `Bavati` (Present), `aBavat` (Past), `Bavizyati` (Future).
* **Gaṇa 1 Ātmanepada:** `aMh` -> `aMhate` (num augment + ṭi substitutions).
* **Gaṇa 4:** `div` -> `dIvyati` (Syan infix + root lengthening).
* **Gaṇa 6:** `tud` -> `tudati` (Sa infix + Nit Guṇa blocking).
* **Aniṭ Roots:** `ji` -> `jezyati` (Augment blocking + ṣ sandhi).

---

## 📁 Project Structure
```text
skt-dhatu-parse/
├── pyproject.toml           # Pip install configuration
├── README.md
├── LICENSE
├── tests/                   # 28-test verification suite
│   ├── test_cli.py
│   ├── test_pipeline.py
│   └── ...
└── skt_dhatu_parse/         # The Core Python Package
    ├── __init__.py
    ├── __main__.py          # Allows 'python -m skt_dhatu_parse'
    ├── cli.py               # Command Line Interface
    ├── engine.py            # Derivation state machine orchestrator
    ├── conjugate.py         # 3x3 Table generator
    ├── rules.py             # Library of Paninian Sutras
    ├── models.py            # Term and Prakriya OOP Classes
    ├── dhatu_loader.py      # SQLite Database fetcher
    ├── shivasutras.py       # Phonological Pratyahara logic
    ├── anubandha.py         # It-Lopa marker resolution
    └── data/
        ├── dhatupatha.tsv
        └── dhatupatha.db
```

---

## 🗺️ Roadmap & Next Steps

### Phase 1: Subanta (Nominal Declensions)
* Build a parallel pipeline for Nominal Stems (*Prātipadika*).
* Append the 21 nominal endings (`su, au, jas...`) to generate cases like *Rāmaḥ, Rāmam, Rāmeṇa*.

### Phase 2: Kṛdanta & Taddhita (Derivatives)
* **Participles:** Apply Kṛt affixes to generate adjectives/participles (e.g., `kR` + `kta` -> *kṛta*, `kR` + `tavatu` -> *kṛtavān*).
* **Nominal Derivatives:** Apply rules to generate patronymics or abstracts (e.g., `dazaratha` + `iY` -> *dāśarathi*).

### Phase 3: Advanced Consonant Sandhi
* Implement rules like *jhalām jaś jhaśi* and *ṣṭunā ṣṭuḥ* to handle complex root/suffix boundaries (e.g., `budh` + `ta` -> *buddha*).
* Support remaining class infixes (e.g., Gaṇa 2 `luk`, Gaṇa 3 reduplication, Gaṇa 10 `Ric`).
* Integrate a complete classical *Dhātupāṭha* dataset for total engine coverage.
```