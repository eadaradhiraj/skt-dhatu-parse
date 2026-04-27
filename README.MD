# 🕉️ Paninian Sanskrit Derivation Engine (`skt-dhatu-parse`)

## Overview
This project is a computational implementation of Pāṇini’s *Aṣṭādhyāyī*. Rather than relying on static lookup tables or pre-conjugated word lists, this engine calculates Sanskrit morphophonemics dynamically in real-time. It takes an abstract phonetic root (*Upadeśa*) and an abstract tense/mood marker (*Lakāra*), and processes them through a strict chronological state-machine of 2,500-year-old grammatical rules to generate mathematically perfect verbal paradigms.

## 🛠️ Core Architecture & Design Decisions
1. **Encoding:** Exclusively uses **SLP1** (Sanskrit Library Phonetic Basic). This maps exactly one phoneme to one ASCII character (e.g., `ṛ` = `f`, `ś` = `S`, `ṣ` = `z`), eliminating complex multi-byte Unicode/Regex parsing issues.
2. **Database:** SQLite (`dhatupatha.db`) for O(1) lightning-fast root lookups. 
3. **Primary Keys:** Because Sanskrit contains homonyms (e.g., `vid` exists in 4 different classes), the engine identifies roots uniquely via a composite key: `dhatu_slp1` + `gana`.
4. **State Machine:** Built on an Object-Oriented `Prakriya` (Derivation) class containing a list of `Term` objects. Terms inherit tags and mutate in place via *Sthānivadbhāva* (Inheritance).
5. **Test-Driven Development:** Covered by a 28-test `unittest` suite simulating boundary cases and edge logic.

---

## 🚀 What Has Been Built So Far (In Great Detail)

### 1. The Phonological Engine (`shivasutras.py`)
The engine is capable of dynamically querying the Sanskrit alphabet using Pāṇini's 14 Śivasūtras.
* **Pratyāhāra Generation:** Can generate sets like `ac` (vowels), `hal` (consonants), `ik` (simple vowels), `ec` (diphthongs), `yaY`, etc.
* **The 'Ṇ' Edge-Case:** Successfully handles Pāṇini’s duplicate `R` (ṇ) marker, knowing that `aR` stops at sutra 1, while `iR` and `yaR` continue to sutra 6.

### 2. The Database Layer (`db_setup.py` & `dhatu_loader.py`)
* Converts a standard Tab-Separated `dhatupatha.tsv` into an indexed SQLite database.
* Loads roots alongside their **pedagogical meta-markers** (e.g., `akzU!`, `divu~`, `ahi!`).
* Auto-resolves homonym collisions by warning the user and safely defaulting to Gaṇa 1 if a specific class is not requested.

### 3. Meta-Marker Resolution / It-Lopa (`anubandha.py`)
Automatically strips instructional markers (*anubandhas*) from roots and affixes while saving their grammatical implications as tags.
* **Rule 1.3.2 (*upadeśe'janunāsika it*):** Identifies nasalized vowels (`!` or `~`), deletes them, and tags the term (e.g., `ahi!` -> `ah` + `idit`).
* **Rule 1.3.3 (*hal antyam*):** Deletes terminal consonants and applies tags (e.g., `tip` -> `ti` + `pit`).
* **Rule 1.3.4 (*na vibhaktau tusmāḥ*):** Exception logic to protect the terminal `s`, `m`, and dentals in inflectional affixes (protects `tas`, `vas`, `mas`).
* **Rule 1.3.8 (*laśakvataddhite*):** Deletes initial `l`, `z` (`S`), and velars (e.g., `Sap` -> `ap` -> `a` + `Sit` + `pit`).

### 4. The Grammatical Rule Engine (`rules.py`)
Implemented a library of context-sensitive, chronological Pāṇinian Sūtras:
* **Substitution & State Inheritance:** Rule 3.4.78 (replaces `laW` with 18 Tiṅ affixes). Rule 1.1.56 (the new affix inherits the `Wit` tag from `laW`).
* **Class Infixes (Vikaraṇas):** Dynamically inserts `Sap` (Gaṇa 1), `Syan` (Gaṇa 4), `Sa` (Gaṇa 6), or `sya` (Future tense).
* **Guṇa & Prevention:** Rule 7.3.84 strengthens `ik` vowels before *Sārvadhātuka* affixes (`BU` -> `Bo`). Rule 1.1.5 blocks Guṇa if the affix is `Nit` (which correctly handles Gaṇa 6 `tud`).
* **Sandhi (Phonetics):** 
    * 6.1.78: `eco'yavAyAvaH` (`Bo + a` -> `Bava`).
    * 6.1.97: `ato guNe` merges consecutive `a`'s.
    * 8.3.59: `AdeSapratyayayoH` changes `s` to `z` (ṣ) after `iR` vowels (handles `jezyati` and `Bavizyati` boundary issues).
    * 8.2.23: `saMyogAntasya lopaH` drops terminal consonants in clusters (`aBavant` -> `aBavan`).
    * 8.3.15: `rutva` converts terminal `s` to Visarga `H`.
* **Ātmanepada (Middle Voice) Morphing:** Rule 3.4.79 (`wita AtmanepadAnAM were`) turns `ta` into `te`. Rule 3.4.80 changes `TAs` to `se`. Rule 7.2.81 morphs `a + Ate` to `ete`.
* **Advanced Augments (Āgamas):** 
    * 7.1.58: `idito num dhAtoH` inserts nasal `m` inside `idit` roots (`ah` -> `aMh`).
    * 6.4.71: `aW` augment prefixes the root for Past Tense.
    * 7.2.35 & 7.2.10: Applies the `iW` augment to `sya` for Future Tense, but actively **blocks** it for *Aniṭ* (anudātta) roots like `ji` (`jezyati`).

### 5. Derivation Pipeline & User Interface (`engine.py`, `cli.py`, `conjugate.py`)
* **Pipeline:** An orchestrator that guarantees rules fire in the strict sequence Pāṇini intended (Initialization -> Substitution -> Vikaraṇa -> Guna/Sandhi -> Word-Final).
* **CLI App:** A robust `argparse` terminal application allowing users to generate step-by-step history logs or fully formatted 3x3 conjugation tables with color-coded warnings for homonyms.

### 6. Verified Grammatical Milestones
The engine currently perfectly derives the 3x3 tables for:
✅ **Gaṇa 1 Parasmaipada:** `BU` -> `Bavati` (Present), `aBavat` (Past), `Bavizyati` (Future).
✅ **Gaṇa 1 Ātmanepada:** `aMh` -> `aMhate` (Includes *num* augment and *ṭi* substitutions).
✅ **Gaṇa 4:** `div` -> `dIvyati` (Includes `Syan` infix and root lengthening).
✅ **Gaṇa 6:** `tud` -> `tudati` (Includes `Sa` infix and `Nit` Guṇa blocking).
✅ **Aniṭ Roots:** `ji` -> `jezyati` (Correctly blocks the `iṭ` augment and triggers `z` sandhi).

---

## 🗺️ Next Steps & Roadmap

### Phase 1: Expansion of the Verbal System (Tiṅanta)
* **Consonant Sandhi:** Implement advanced consonant-to-consonant rules (e.g., *jhalām jaś jhaśi*, *ṣṭunā ṣṭuḥ*) to support complex roots.
* **Support all 10 Gaṇas:** Add logic for the remaining class infixes: Gaṇa 2 (deletion/luk), Gaṇa 3 (reduplication), Gaṇa 5 (`Snu`), Gaṇa 7 (`Snam` infix), Gaṇa 8 (`u`), Gaṇa 9 (`SnA`), and Gaṇa 10 (`Ric`).
* **More Lakāras:** Add Imperative (`loW`), Potential (`liN`), and Perfect (`liW` - requiring root reduplication logic).
* **Dynamic Seṭ/Aniṭ Resolution:** Currently, *Aniṭ* roots are hardcoded in a python list. Move this data to an `is_anit` boolean column in the SQLite DB based on historical accent data.

### Phase 2: The Nominal System (Subanta)
* **Noun Declension:** Build a parallel pipeline that takes a Nominal Stem (*Prātipadika*) like `rAma` or `hari`.
* **SuP Affixes:** Append the 21 nominal endings (`su, au, jas...`) and write the vowel sandhi and gender-specific rules required to output forms like *Rāmaḥ, Rāmam, Rāmeṇa*.

### Phase 3: Primary & Secondary Derivatives (Kṛdanta & Taddhita)
* **Participles:** Apply the verb engine to generate words using Kṛt affixes (e.g., `kR` + `kta` -> *kṛta*, `kR` + `tavatu` -> *kṛtavān*).
* **Nominal Derivatives:** Apply rules to generate patronymics or abstracts (e.g., `dazaratha` + `iY` -> *dāśarathi*, `pARini` + `aR` -> *pāṇinīya*).

### Phase 4: Packaging & Distribution
* **Pip Installable Package:** Structure the project using modern `pyproject.toml` standards so it can be installed directly from the GitHub repository via `pip install git+https://github.com/yourusername/skt-dhatu-parse.git`.
* **Global CLI Tool:** Expose the command-line interface via Python entry points, allowing users to run derivations globally from their terminal (e.g., `skt-derive BU -l laN --table`) without needing to clone the source code manually.
* **Importable Python API:** Ensure the core architecture (`derive()`, `get_dhatu()`, `Prakriya`) is cleanly exposed as a library. Other developers will be able to run `from skt_dhatu_parse import derive` to integrate Pāṇinian morphophonemics directly into their own NLP applications.
* **Full Dhātupāṭha Import:** Clean and package a complete list of 2,000+ classical Sanskrit roots as bundled package data, so the engine works out-of-the-box post-installation.