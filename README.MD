# 🕉️ skt-dhatu-parse (Paninian Sanskrit Engine)

## Overview
`skt-dhatu-parse` is a computational linguistics engine that implements Pāṇini’s *Aṣṭādhyāyī*. Rather than relying on static lookup tables or pre-conjugated dictionaries, this package calculates Sanskrit morphophonemics dynamically in real-time. 

It processes an abstract phonetic root (*Upadeśa*) and runs it through a strict chronological state-machine of 2,500-year-old grammatical rules to generate Verbs (*Tiṅanta*), Participles/Primary Derivatives (*Kṛdanta*), and Secondary Roots/Causatives (*Sanādi*).

It is designed to be fully `pip`-installable, highly usable as a standalone CLI tool, and importable as a Python library for advanced NLP applications.

---

## 📦 Installation & Quickstart

To install the engine locally in editable mode (recommended for development):
```bash
git clone https://github.com/eadaradhiraj/skt-dhatu-parse.git
cd skt-dhatu-parse
pip install -e .
```

### Command Line Interface (CLI)
Once installed, you can access the engine globally from your terminal using the Python module syntax. 

**1. Generate a full 3x3 conjugation table (Tiṅanta):**
```bash
python -m skt_dhatu_parse BU -l laW --table
```

**2. Generate a Participle (Kṛdanta) with Derivation History:**
*(Watch Consonant Sandhi dynamically merge `buD` + `kta` -> `budDa`)*
```bash
python -m skt_dhatu_parse buD --krt kta --history
```

**3. Generate a Secondary Causative Root (Sanādi):**
*(Watch Vṛddhi dynamically lengthen `ram` + `Ric` -> `rAmi`)*
```bash
python -m skt_dhatu_parse ram --causative --history
```

**4. Handle Homonyms Automatically:**
If a root exists in multiple classes (like `div`), the engine warns you and auto-defaults to Gaṇa 1. You can explicitly override this with `-g`:
```bash
python -m skt_dhatu_parse div -l laW -g 4 --table
```

### Python API
You can easily import the engine into your own Python applications:
```python
from skt_dhatu_parse.engine import derive
from skt_dhatu_parse.krdanta import derive_krdanta

# Derive the 3rd person singular future tense of 'bhū'
verb = derive('BU', lakara_name='lfW', purusha='prathama', vacana=0, gana=1)
print(verb.get_current_string())  # Outputs: Bavizyati

# Derive the past participle of 'budh'
participle = derive_krdanta('buD', 'kta', gana=1)
print(participle.get_current_string()) # Outputs: budDa
```

---

## 🛠️ Core Architecture & Design Decisions

1. **Encoding (SLP1):** The engine exclusively uses SLP1 (Sanskrit Library Phonetic Basic). This strictly maps exactly one phoneme to one ASCII character (e.g., `ṛ` = `f`, `ś` = `S`, `ṣ` = `z`), eliminating complex Unicode parsing errors and regex boundary issues.
2. **Database:** Powered by an indexed SQLite database (`dhatupatha.db`) for lightning-fast root lookups. 
3. **Composite Primary Keys:** Safely handles Sanskrit homonyms (e.g., `vid` in Gaṇa 2, 4, 6, and 7) by identifying roots via a composite key of `dhatu_slp1` + `gana`.
4. **State Machine (`Prakriya`):** Built on an Object-Oriented sequence of `Term` objects. Terms inherit tags and mutate in place via *Sthānivadbhāva* (State Inheritance).
5. **TDD (Test-Driven Development):** Guarded by a comprehensive 33-test `unittest` suite simulating boundary cases, class variations, and exact Paninian rule execution.

---

## 🚀 Grammatical Features Implemented (In Detail)

### 1. The Phonological Engine (`shivasutras.py`)
Dynamically queries the Sanskrit alphabet using Pāṇini's 14 Śivasūtras.
* **Pratyāhāras:** Generates arrays of phonemes dynamically (e.g., `ac`, `hal`, `ik`, `yaY`, `iR`, `jhal`, `jhaS`).
* **The 'Ṇ' Edge-Case:** Handles Pāṇini’s duplicate `R` (ṇ) marker—`aR` stops at sutra 1; `iR`/`yaR` continue to sutra 6.

### 2. Meta-Marker Resolution / It-Lopa (`anubandha.py`)
Strips instructional markers (*anubandhas*) from roots and affixes while saving their grammatical implications as tags.
* **1.3.2 (upadeśe'janunāsika it):** Deletes nasalized vowels (`!` or `~`) and tags the term.
* **1.3.3 & 1.3.8:** Deletes terminal and initial consonants (`tip` -> `ti` + `pit`).
* **1.3.4 (na vibhaktau tusmāḥ):** Protects terminal `s`, `m`, and dentals in inflectional affixes.
* **1.3.7 (cuṭū):** Deletes initial palatals and retroflexes (`Ric` -> `ic` + `Rit`).

### 3. Vowel Morphing & Sandhi
* **Guṇa & Vṛddhi:** Strengthens vowels based on `Sārvadhātuka`, `Ardhadhātuka`, `Yit`, and `Rit` triggers (Rules 7.3.84, 7.2.115 *aco ñṇiti*, 7.2.116 *ata upadhāyāḥ*).
* **Guṇa Prevention:** Recognizes `kit` and `Nit` tags to block vowel strengthening (Rule 1.1.5).
* **Vowel Sandhi:** Merges `a+a` (*ato guṇe*) and triggers `ay/av/Ay/Av` replacements (*eco'yavAyAvaH*).

### 4. Consonant Sandhi
* **Retroflexion (Ṣatva/Ṇatva):** Converts `s` to `z` (8.3.59) and `n` to `R` (8.4.1).
* **Assimilation:** Merges `jhaS` and `jhal` consonant boundaries (e.g., `buD` + `ta` -> `budDa`) via Rules 8.2.40 and 8.4.53.
* **Terminal Reductions:** Converts word-final `s` to `H` (8.3.15) and drops trailing consonants in clusters (8.2.23).

### 5. Advanced Augments (Āgamas) & Morphing
* **Kṛdanta Affixes:** 7.1.1 replaces `yu`/`vu` with `ana`/`aka` (`lyuW` -> `ana`).
* **Sanādi Generation:** 3.1.32 merges secondary roots into a single base (`BAvi`).
* **Tiṅanta Augments:** 7.1.58 inserts `m` inside `idit` roots. 6.4.71 prefixes `aW` for Past Tense.
* **Seṭ/Aniṭ Logic:** 7.2.35 & 7.2.10 applies the `iW` augment to `sya` for Future Tense, but actively **blocks** it for *Aniṭ* (anudātta) roots like `ji` (`jezyati`).

---

## 🔬 Verified Derivations
The engine is computationally verified (via unittests) to perfectly derive:
* **Gaṇa 1 Parasmaipada:** `BU` -> `Bavati`, `aBavat`, `Bavizyati`.
* **Gaṇa 1 Ātmanepada:** `aMh` -> `aMhate` (num augment + ṭi substitutions).
* **Gaṇa 4:** `div` -> `dIvyati` (Syan infix + root lengthening).
* **Gaṇa 6:** `tud` -> `tudati` (Sa infix + Nit Guṇa blocking).
* **Aniṭ Roots:** `ji` -> `jezyati` (Augment blocking + ṣ sandhi).
* **Participles:** `buD` + `kta` -> `budDa` (Consonant assimilation).
* **Derivatives:** `ram` + `GaY` -> `rAma` (Vṛddhi). `ram` + `lyuW` -> `ramaRa` (Ṇatva Sandhi).
* **Causatives:** `BU` + `Ric` -> `BAvi`. `ram` + `Ric` -> `rAmi`.

---

## 📁 Project Structure
```text
skt-dhatu-parse/
├── pyproject.toml           # Pip install configuration
├── README.md
├── LICENSE
├── tests/                   # 33-test verification suite
│   ├── test_cli.py
│   ├── test_pipeline.py
│   ├── test_krdanta.py
│   └── test_sanadi.py
└── skt_dhatu_parse/         # The Core Python Package
    ├── __init__.py
    ├── __main__.py          # Allows 'python -m skt_dhatu_parse'
    ├── cli.py               # Command Line Interface
    ├── engine.py            # Tiṅanta state machine orchestrator
    ├── krdanta.py           # Participle state machine
    ├── sanadi.py            # Secondary Root state machine
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

### Phase 1: Reduplication (Abhyāsa)
* Implement root-duplication algorithms to unlock the Perfect Tense (*liW*) and Gaṇa 3 verbs (Juhotyādi).
* Apply shortening/halving rules (`BUBU` -> `baBU`).

### Phase 2: Noun Declensions (Subantas)
* Build a parallel pipeline for Nominal Stems (*Prātipadika*).
* Append the 21 nominal case endings (`su, au, jas...`) to generate outputs like *Rāmaḥ, Rāmam, Rāmeṇa*.

### Phase 3: Recursive Piping
* Pass newly generated Secondary Roots (like the Causative `BAvi`) directly back into the `engine.py` pipeline to seamlessly conjugate `BAvayati` (He causes to be).