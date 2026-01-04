# Visualització de Dades - PRAC 2
Anàlisi de les Competències Bàsiques de Sisè de Primària a Catalunya (2009-2023)

## Descripció del Projecte

Aquest projecte implementa una visualització interactiva completa per analitzar com influeixen el gènere, el territori i l'entorn en els resultats escolars dels alumnes de sisè de primària a Catalunya. S'utilitzen quatre visualitzacions diferents per explorar les dades:

### 1. Gràfic de Barres Agrupades
Mostra l'evolució de la diferència entre rendiment en llengües i matemàtiques (LING_MAT) al llarg dels anys, discretitzat per gènere. Els valors positius indiquen millor rendiment en llengües, mentre que els negatius indiquen millor rendiment en matemàtiques.

### 2. Gràfic de Línies
Analitza com evoluciona la mitjana global de cada àrea territorial en funció de l'edat relativa dels alumnes, permetent identificar patrons territorials i l'impacte de l'edat dins del mateix curs.

### 3. Heatmaps Interactius (Dual)
Compara el rendiment en llengües (PLING) i matemàtiques (PMAT) segons la naturalesa del centre (públic/privat) i el gènere, amb un dropdown per filtrar per àrea territorial o veure la mitjana de tots els territoris.

### 4. Barres Apilades
Mostra l'evolució dels nivells d'assoliment (Alt, Mitja, Baix) al llarg dels anys en percentatge, amb filtratge per territori per avaluar la qualitat educativa.

## Fonts de Dades

### Dades educatives de Catalunya
**Font:** Portal de dades obertes de la Generalitat de Catalunya
- **URL:** https://analisi.transparenciacatalunya.cat/
- **Dataset:** Avaluació de competències bàsiques de sisè d'educació primària
- **Període:** 2009-2023
- **Registres analitzats:** 864,311 alumnes
- **Àrees territorials:** 10
- **Fitxer:** `Avaluació_de_sisè_d'educació_primària_20251201_mod.csv`

## Execució

**Important**: cal primer descomprimir la base de dades (ha calgut pujar-la comprimida en .7z ja que el tamany no permetia pujar la original.

```bash
python generate_visualization.py
```

El programa genera una visualització interactiva completa en format HTML:
- `RitaRocaTaxonera_PRAC2_Storytelling.html`

Aquest fitxer HTML conté:
- 4 visualitzacions interactives de Plotly
- Estadístiques clau del dataset
- Interpretacions i punts clau de cada gràfic
- Disseny responsive i professional

## Eines utilitzades

- **Python 3.7+**
- **Pandas** - Manipulació i neteja de dades
- **Plotly** - Visualitzacions interactives
- **NumPy** - Operacions numèriques
- **PlotlyJSONEncoder** - transformació JSON per generar HTML

## Estructura del Projecte

```
Prac2/
├── generate_visualization.py           # Script principal de generació
├── Avaluació_de_sisè_d'educació_primària_20251201_mod.csv  # Dataset
├── RitaRocaTaxonera_PRAC2_Storytelling.html  # Visualització final
└── README.md                           # Aquest fitxer
└── requirements.txt                    # conté les llibreries emprades
```

## Autora

**Rita Roca Taxonera**  
Visualització de Dades - UOC  
Gener 2026

