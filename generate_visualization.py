"""
Generació HTML de la Visualització de les avaluacions de sisè d'educació primària
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from plotly.utils import PlotlyJSONEncoder
import json
import numpy as np

# Carreguem el dataset final amb les noves columnes incloses
print("Carregant dataset...")
df = pd.read_csv('Avaluació_de_sisè_d\'educació_primària_20251201_mod.csv', low_memory=False)

# Eliminem files amb valors nuls en les competències principals
df_clean = df.dropna(subset=['PLING', 'PMAT', 'Mitjana_Global', 'LING_MAT'])

print(f"Total d'alumnes: {len(df_clean):,}")
print(f"Anys disponibles: {sorted(df_clean['ANY'].unique())}")

# ==============================================================================
# Càlcul d'estadístiques bàsiques
# ==============================================================================
total_students = len(df_clean)
num_territories = df_clean['AREA_TERRITORIAL'].nunique()
mitjana_global = df_clean['Mitjana_Global'].mean()

# Calcular creixement percentual respecte l'any anterior
# Agrupem per any i calculem la mitjana global
yearly_avg = df_clean.groupby('ANY')['Mitjana_Global'].mean().sort_index()

current_year = yearly_avg.index[-1]
previous_year = yearly_avg.index[-2]
creixement_percentual = ((yearly_avg[current_year] - yearly_avg[previous_year]) / yearly_avg[previous_year]) * 100

print(f"Mitjana global: {mitjana_global:.2f}")
print(f"Creixement percentual respecte any anterior: {creixement_percentual:.2f}%")

# ==============================================================================
# Visualització 1: Gràfic de barres - Evolució de LING_MAT al llarg dels anys per gènere
# ==============================================================================
print("Visualització 1: Evolució LING_MAT per anys i gènere")

# Calcular mitjana de LING_MAT per any i gènere
ling_mat_gender = df_clean.groupby(['ANY', 'GENERE'])['LING_MAT'].mean().reset_index()
ling_mat_gender = ling_mat_gender.sort_values('ANY')

# Separar dades per gènere
ling_mat_dones = ling_mat_gender[ling_mat_gender['GENERE'] == 'Dona'].sort_values('ANY')
ling_mat_homes = ling_mat_gender[ling_mat_gender['GENERE'] == 'Home'].sort_values('ANY')

# Colors per gènere i valor positiu/negatiu
colors_dones = ['#C8A2E0' if x >= 0 else '#8B5CF6' for x in ling_mat_dones['LING_MAT']]
colors_homes = ['#A8E6A3' if x >= 0 else '#4CAF50' for x in ling_mat_homes['LING_MAT']]

fig1 = go.Figure()

# Barres per Dones
fig1.add_trace(go.Bar(
    x=ling_mat_dones['ANY'],
    y=ling_mat_dones['LING_MAT'],
    name='Dones',
    marker_color=colors_dones,
    hovertemplate='<b>Any: %{x}</b><br>' +
                  'Dones<br>' +
                  'LING_MAT: %{y:.2f}<br>' +
                  '<extra></extra>'
))

# Barres per Homes
fig1.add_trace(go.Bar(
    x=ling_mat_homes['ANY'],
    y=ling_mat_homes['LING_MAT'],
    name='Homes',
    marker_color=colors_homes,
    hovertemplate='<b>Any: %{x}</b><br>' +
                  'Homes<br>' +
                  'LING_MAT: %{y:.2f}<br>' +
                  '<extra></extra>'
))

# Anotació per zona positiva (millor en llengües) - dalt del gràfic
fig1.add_annotation(
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.98,
    text="Millor en llengües",
    showarrow=False,
    bgcolor="#4A4949",
    font=dict(color="white", size=11, family="Arial"),
    bordercolor="#4A4949",
    borderwidth=2,
    borderpad=6,
    opacity=0.9
)

# Anotació per zona negativa (millor en matemàtiques) - baix del gràfic
fig1.add_annotation(
    xref="paper",
    yref="paper",
    x=0.5,
    y=0.02,
    text="Millor en matemàtiques",
    showarrow=False,
    bgcolor="#4A4949",
    font=dict(color="white", size=11, family="Arial"),
    bordercolor="#4A4949",
    borderwidth=2,
    borderpad=6,
    opacity=0.9
)

# Afegir línia de referència en y=0
fig1.add_hline(y=0, line_dash="dash", line_color="gray", 
               annotation_text="Equilibri", annotation_position="right")

fig1.update_layout(
    xaxis_title='Any',
    yaxis_title='Diferència Llengües - Matemàtiques',
    height=550,
    margin=dict(l=80, r=50, t=80, b=80),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    yaxis=dict(gridcolor='rgba(200, 200, 200, 0.3)', zeroline=True, zerolinecolor='gray'),
    xaxis=dict(dtick=1),
    barmode='group',  # Barres agrupades per any
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        bgcolor='rgba(255, 255, 255, 0.9)',
        bordercolor='gray',
        borderwidth=1
    )
)

# Convertir a diccionari JSON per generar HTML
chart1_json = json.dumps(fig1.to_plotly_json(), cls=PlotlyJSONEncoder)

# ==============================================================================
# Visualització 2: Gràfic de línies - Mitjana Global per territori en funció de l'edat relativa
# ==============================================================================
print("Visualització 2: Mitjana Global per territori i edat relativa")

# Calcular mitjana per territori i edat relativa
territory_age_data = df_clean.groupby(['AREA_TERRITORIAL', 'Edat_Relativa'])['Mitjana_Global'].mean().reset_index()

fig2 = go.Figure()

colors_territories = px.colors.qualitative.Set3[:10]

for i, territory in enumerate(sorted(df_clean['AREA_TERRITORIAL'].unique())):
    territory_data = territory_age_data[territory_age_data['AREA_TERRITORIAL'] == territory]
    territory_data = territory_data.sort_values('Edat_Relativa')
    
    fig2.add_trace(go.Scatter(
        x=territory_data['Edat_Relativa'],
        y=territory_data['Mitjana_Global'],
        name=territory,
        mode='lines+markers',
        line=dict(width=2.5, color=colors_territories[i]),
        marker=dict(size=6),
        hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Edat Relativa: %{x}<br>' +
                      'Mitjana Global: %{y:.2f}<br>' +
                      '<extra></extra>'
    ))

fig2.update_layout(
    xaxis_title='Edat Relativa',
    yaxis_title='Mitjana Global',
    height=550,
    margin=dict(l=80, r=50, t=30, b=80),
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="gray",
        borderwidth=1
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    yaxis=dict(gridcolor='rgba(200, 200, 200, 0.3)', range=[65, 85]),
    xaxis=dict(gridcolor='rgba(200, 200, 200, 0.3)', dtick=1)
)

chart2_json = json.dumps(fig2.to_plotly_json(), cls=PlotlyJSONEncoder)

# ==============================================================================
# Visualització 3: Heatmap doble amb dropdown per territori - PLING
# ==============================================================================
print("Visualització 3: Heatmaps interactius per territori")

territories = sorted(df_clean['AREA_TERRITORIAL'].unique())

# Preparar dades per Llengües (PLING)
pling_naturalesa_data = []
for territory in territories:
    territory_df = df_clean[df_clean['AREA_TERRITORIAL'] == territory]
    
    for naturalesa in ['Public', 'Privat']:
        naturalesa_label = 'Públic' if naturalesa == 'Public' else 'Privat'
        for gender in ['Home', 'Dona']:
            subset = territory_df[(territory_df['NATURALESA'] == naturalesa) & 
                                  (territory_df['GENERE'] == gender)]
            if len(subset) > 0:
                mean_val = subset['PLING'].mean()
                pling_naturalesa_data.append({
                    'AREA_TERRITORIAL': territory,
                    'Categoria': naturalesa_label,
                    'Gènere': gender,
                    'Valor': mean_val
                })

df_pling_nat = pd.DataFrame(pling_naturalesa_data)

# Preparar dades per Matemàtiques (PMAT)
pmat_naturalesa_data = []
for territory in territories:
    territory_df = df_clean[df_clean['AREA_TERRITORIAL'] == territory]
    
    for naturalesa in ['Public', 'Privat']:
        naturalesa_label = 'Públic' if naturalesa == 'Public' else 'Privat'
        for gender in ['Home', 'Dona']:
            subset = territory_df[(territory_df['NATURALESA'] == naturalesa) & 
                                  (territory_df['GENERE'] == gender)]
            if len(subset) > 0:
                mean_val = subset['PMAT'].mean()
                pmat_naturalesa_data.append({
                    'AREA_TERRITORIAL': territory,
                    'Categoria': naturalesa_label,
                    'Gènere': gender,
                    'Valor': mean_val
                })

df_pmat_nat = pd.DataFrame(pmat_naturalesa_data)

# Calcular escala comuna per als dos heatmaps
min_val = min(df_pling_nat['Valor'].min(), df_pmat_nat['Valor'].min())
max_val = max(df_pling_nat['Valor'].max(), df_pmat_nat['Valor'].max())
# Arrodonim valors de l'escala (múltiples de 5)
min_val = np.floor(min_val / 5) * 5
max_val = np.ceil(max_val / 5) * 5

# Calculem mitjana de tots els territoris per a l'opció "Tots"
pling_tots_data = []
pmat_tots_data = []

for naturalesa in ['Public', 'Privat']:
    naturalesa_label = 'Públic' if naturalesa == 'Public' else 'Privat'
    for gender in ['Home', 'Dona']:
        subset = df_clean[(df_clean['NATURALESA'] == naturalesa) & 
                          (df_clean['GENERE'] == gender)]
        if len(subset) > 0:
            pling_tots_data.append({
                'AREA_TERRITORIAL': 'Tots',
                'Categoria': naturalesa_label,
                'Gènere': gender,
                'Valor': subset['PLING'].mean()
            })
            pmat_tots_data.append({
                'AREA_TERRITORIAL': 'Tots',
                'Categoria': naturalesa_label,
                'Gènere': gender,
                'Valor': subset['PMAT'].mean()
            })

# Afegir les mitjanes "Tots" als dataframes
df_pling_nat = pd.concat([df_pling_nat, pd.DataFrame(pling_tots_data)], ignore_index=True)
df_pmat_nat = pd.concat([df_pmat_nat, pd.DataFrame(pmat_tots_data)], ignore_index=True)

# Crear subplot amb 2 heatmaps
fig3 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Puntuació en Llengües', 'Puntuació en Matemàtiques'),
    horizontal_spacing=0.15
)

# Crear un heatmap per cada territori amb dropdown
# Opció "Tots" per defecte
default_territory = 'Tots'

# PLING Heatmap
df_pling_pivot = df_pling_nat[df_pling_nat['AREA_TERRITORIAL'] == default_territory].pivot(
    index='Categoria', columns='Gènere', values='Valor'
).reindex(['Públic', 'Privat'])

# PMAT Heatmap
df_pmat_pivot = df_pmat_nat[df_pmat_nat['AREA_TERRITORIAL'] == default_territory].pivot(
    index='Categoria', columns='Gènere', values='Valor'
).reindex(['Públic', 'Privat'])

# Crear text per mostrar a les caselles i hover text per PLING
text_display_pling = []
for i, cat in enumerate(df_pling_pivot.index):
    text_row = []
    hover_row = []
    for j, gen in enumerate(df_pling_pivot.columns):
        val = df_pling_pivot.iloc[i, j]
        text_row.append(f'{val:.1f}')
    text_display_pling.append(text_row)

# Crear text per mostrar a les caselles i hover text per PMAT
text_display_pmat = []
for i, cat in enumerate(df_pmat_pivot.index):
    text_row = []
    hover_row = []
    for j, gen in enumerate(df_pmat_pivot.columns):
        val = df_pmat_pivot.iloc[i, j]
        text_row.append(f'{val:.1f}')
    text_display_pmat.append(text_row)

fig3.add_trace(
    go.Heatmap(
        z=df_pling_pivot.values,
        x=df_pling_pivot.columns,
        y=df_pling_pivot.index,
        colorscale='RdYlGn',
        text=text_display_pling,
        texttemplate='%{text}',
        textfont={"size": 16, "color": "black"},
        showscale=False,
        zmin=min_val,
        zmax=max_val,
        name='PLING'
    ),
    row=1, col=1
)

fig3.add_trace(
    go.Heatmap(
        z=df_pmat_pivot.values,
        x=df_pmat_pivot.columns,
        y=df_pmat_pivot.index,
        colorscale='RdYlGn',
        text=text_display_pmat,
        texttemplate='%{text}',
        textfont={"size": 16, "color": "black"},
        colorbar=dict(title='Puntuació', x=1.05),
        zmin=min_val,
        zmax=max_val,
        name='PMAT'
    ),
    row=1, col=2
)

# Crear els botons del dropdown per canviar de territori
buttons = []
for territory in ['Tots'] + list(territories):
    # Pivot per aquest territori
    df_pling_t = df_pling_nat[df_pling_nat['AREA_TERRITORIAL'] == territory].pivot(
        index='Categoria', columns='Gènere', values='Valor'
    ).reindex(['Públic', 'Privat'])
    
    df_pmat_t = df_pmat_nat[df_pmat_nat['AREA_TERRITORIAL'] == territory].pivot(
        index='Categoria', columns='Gènere', values='Valor'
    ).reindex(['Públic', 'Privat'])
    
    # Text per mostrar i hover text per aquest territori
    text_pling_t = []
    hover_pling_t = []
    for i, cat in enumerate(df_pling_t.index):
        text_row = []
        hover_row = []
        for j, gen in enumerate(df_pling_t.columns):
            val = df_pling_t.iloc[i, j]
            text_row.append(f'{val:.1f}')
        text_pling_t.append(text_row)
    
    text_pmat_t = []
    hover_pmat_t = []
    for i, cat in enumerate(df_pmat_t.index):
        text_row = []
        hover_row = []
        for j, gen in enumerate(df_pmat_t.columns):
            val = df_pmat_t.iloc[i, j]
            text_row.append(f'{val:.1f}')
        text_pmat_t.append(text_row)
    
    button = dict(
        label=territory,
        method='update',
        args=[
            {
                'z': [df_pling_t.values, df_pmat_t.values],
                'text': [text_pling_t, text_pmat_t],
            },
            {
                'title': f'Comparativa Llengües vs Matemàtiques - {territory}'
            }
        ]
    )
    buttons.append(button)

fig3.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.5,
            xanchor="center",
            y=1.20,
            yanchor="top",
            bgcolor="white",
            bordercolor="gray",
            borderwidth=2
        )
    ],
    title=f'Comparativa Llengües vs Matemàtiques - {default_territory}',
    height=500,
    margin=dict(l=100, r=150, t=120, b=80),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)

fig3.update_xaxes(title_text='Gènere', row=1, col=1)
fig3.update_yaxes(title_text='Naturalesa Centre', row=1, col=1)
fig3.update_xaxes(title_text='Gènere', row=1, col=2)

chart3_json = json.dumps(fig3.to_plotly_json(), cls=PlotlyJSONEncoder)

# ==============================================================================
# Visualització 4: Distribució per Nivell d'Assoliment
# ==============================================================================
print("Visualització 4: Distribució per Nivell d'Assoliment")

# Preparar dades per territori amb opció "Tots"
def get_nivell_data(territory=None):
    if territory == 'Tots' or territory is None:
        subset = df_clean
    else:
        subset = df_clean[df_clean['AREA_TERRITORIAL'] == territory]
    
    nivell_data = subset.groupby(['ANY', 'Nivell_Assoliment']).size().reset_index(name='count')
    nivell_pivot = nivell_data.pivot(index='ANY', columns='Nivell_Assoliment', values='count').fillna(0)
    nivell_pivot_pct = nivell_pivot.div(nivell_pivot.sum(axis=1), axis=0) * 100
    return nivell_pivot_pct

# Dades per defecte: "Tots"
default_territory_chart4 = 'Tots'
nivell_pivot_pct = get_nivell_data(default_territory_chart4)

fig4 = go.Figure()

colors_nivell = {'Alt': '#2ecc71', 'Mitja': '#f39c12', 'Baix': '#e74c3c'}

for nivell in ['Alt', 'Mitja', 'Baix']:
    if nivell in nivell_pivot_pct.columns:
        fig4.add_trace(go.Bar(
            x=nivell_pivot_pct.index,
            y=nivell_pivot_pct[nivell],
            name=nivell,
            marker_color=colors_nivell[nivell],
            hovertemplate='<b>Any: %{x}</b><br>' +
                          f'{nivell}: %{{y:.1f}}%<br>' +
                          '<extra></extra>'
        ))

# Crear botons per al dropdown de Chart 4
buttons_chart4 = []
for territory in ['Tots'] + list(territories):
    nivell_pct_t = get_nivell_data(territory)
    
    y_data = []
    for nivell in ['Alt', 'Mitja', 'Baix']:
        if nivell in nivell_pct_t.columns:
            y_data.append(nivell_pct_t[nivell].tolist())
        else:
            y_data.append([0] * len(nivell_pct_t.index))
    
    button = dict(
        label=territory,
        method='update',
        args=[
            {'y': y_data},
            {'title': f'Distribució per Nivell d\'Assoliment - {territory}'}
        ]
    )
    buttons_chart4.append(button)

fig4.update_layout(
    updatemenus=[
        dict(
            buttons=buttons_chart4,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.5,
            xanchor="center",
            y=1.20,
            yanchor="top",
            bgcolor="white",
            bordercolor="gray",
            borderwidth=2
        )
    ],
    title=f'Distribució per Nivell d\'Assoliment - {default_territory_chart4}',
    barmode='stack',
    xaxis_title='Any',
    yaxis_title='Percentatge d\'alumnes (%)',
    height=500,
    margin=dict(l=80, r=50, t=120, b=80),
    legend=dict(
        title='Nivell Assoliment',
        orientation="v",
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="gray",
        borderwidth=1
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(gridcolor='rgba(200, 200, 200, 0.3)', range=[0, 100]),
    xaxis=dict(dtick=1)
)

chart4_json = json.dumps(fig4.to_plotly_json(), cls=PlotlyJSONEncoder)

# ==============================================================================
# Generació HTML
# ==============================================================================
print("Generating HTML file...")

html_template = f"""<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Com influeixen el gènere, el territori i l'entorn en els resultats escolars?</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #667eea;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2em;
            margin-bottom: 40px;
        }}
        .chart-container {{
            margin: 40px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .chart-title {{
            font-size: 1.5em;
            color: #34495e;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .chart-description {{
            color: #7f8c8d;
            margin-bottom: 20px;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: #667eea;
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            text-align: center;
            min-width: 180px;
            margin: 10px;
            transition: transform 0.3s ease;
        }}
        .stat-box:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 1em;
            opacity: 0.9;
        }}
        .stat-box.positive {{
            background: #2ecc71;
        }}
        .stat-box.negative {{
            background: #e74c3c;
        }}
        footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .interpretation {{
            background: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .interpretation h3 {{
            color: #2c3e50;
            margin-top: 0;
            font-size: 1.1em;
        }}
        .interpretation p {{
            color: #555;
            line-height: 1.6;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Com influeixen el gènere, el territori i l'entorn <br> en els resultats escolars?</h1>
        <div class="subtitle">Anàlisi de les Competències Bàsiques de Sisè de Primària a Catalunya (2009-2023)<br>
        <small>Font: Portal de dades obertes de la Generalitat de Catalunya (Dades proveïdes pel Departament d'Educació)</small></div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{total_students:,}</div>
                <div class="stat-label">Alumnes Analitzats</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{num_territories}</div>
                <div class="stat-label">Àrees Territorials</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{mitjana_global:.1f}</div>
                <div class="stat-label">Mitjana Global</div>
            </div>
            <div class="stat-box {'positive' if creixement_percentual > 0 else 'negative'}">
                <div class="stat-number">{creixement_percentual:+.2f}%</div>
                <div class="stat-label">Creixement vs Any Anterior</div>
            </div>
        </div>

        <!-- Visualització 1: Evolució LING_MAT -->
        <div class="chart-container">
            <div class="chart-title">1. Equilibri entre Competències Lingüístiques i Matemàtiques</div>
            <div class="chart-description">
                Aquest gràfic mostra l'evolució de la diferència entre el rendiment en llengües i matemàtiques al llarg dels anys.
                <br> Els valors <b>positius</b> indiquen <b>millor rendiment en llengües</b>, mentre que els 
                valors <b>negatius</b> indiquen <b>millor rendiment en matemàtiques</b>.
            </div>
            <div id="chart1"></div>
            <div class="interpretation">
                <h3>Punts clau:</h3>
                <p>S'observa com els <b>nois presenten major desequilibri</b> (habitualment presentant millors resultats en matemàtiques que en llengües).
                Tot i així en els últims anys aquest desequilibri ha anat millorant.<br>
                Les <b>noies</b> partien d'un <b>equilibri més gran</b> entre ambdues competències, encara que en els <b>últims anys</b> han mostrat <b>millors resultats en llengües que en matemàtiques</b>. 
                </p>
            </div>
        </div>

        <!-- Visualització 2: Mitjana Global per territori -->
        <div class="chart-container">
            <div class="chart-title">2. Rendiment per Àrea Territorial segons l'Edat Relativa</div>
            <div class="chart-description">
                Gràfic de línies que mostra com <b>evoluciona la mitjana global</b> de cada àrea territorial en <b>funció de 
                l'edat relativa</b> dels alumnes.<br>
                L'edat relativa indica els mesos de diferència respecte l'edat mínima per cursar sisè.
            </div>
            <div id="chart2"></div>
            <div class="interpretation">
                <h3>Punts clau:</h3>
                <p><b>L'edat relativa</b> té un lleuger <b>impacte en el rendiment acadèmic</b>. Els alumnes més grans dins del 
                mateix curs tendeixen a obtenir millors resultats.<br>
                Les <b>diferències</b> gairebé constants <b>entre territoris</b> poden reflectir factors socioeconòmics, 
                recursos educatius i polítiques locals.</p>
            </div>
        </div>

        <!-- Visualització 3: Heatmaps comparatius -->
        <div class="chart-container">
            <div class="chart-title">3. Comparativa entre Llengües i Matemàtiques en funció del Centre i Gènere</div>
            <div class="chart-description">
                Mapes de calor interactius que permeten <b>comparar el rendiment</b> en llengües i matemàtiques 
                segons la naturalesa del centre (públic/privat) i el gènere. 
                <br>Utilitzeu el selector superior per filtrar per àrea territorial.
            </div>
            <div id="chart3"></div>
            <div class="interpretation">
                <h3>Punts clau:</h3>
                <p>La visualització mostra que, en mitjana, els <b>nois obtenen puntuacions més altes en matemàtiques que en llengües</b>, 
                mentre que les <b>noies</b> presenten valors <b>més equilibrats</b> entre ambdues competències.<br>
                <b>En llengües, les noies superen els nois, i en matemàtiques passa a l'inrevés.</b><br>
                També s'observa que els <b>centres privats</b> tenen <b>mitjanes més altes que els públics</b> en totes les competències 
                (les diferències en funció del centre podríen estar relacionades amb factors socioeconòmics).</p>
            </div>
        </div>

        <!-- Visualització 4: Nivell d'Assoliment -->
        <div class="chart-container">
            <div class="chart-title">4. Evolució dels Nivells d'Assoliment</div>
            <div class="chart-description">
                Gràfic de barres apilades que mostra el percentatge d'alumnes en cada nivell d'assoliment 
                (Alt, Mitja, Baix) al llarg dels anys. Permet avaluar l'evolució global de la qualitat educativa.
            </div>
            <div id="chart4"></div>
            <div class="interpretation">
                <h3>Punts clau:</h3>
                <p>S'observa com es manté una <b>distribució bastant estable</b> al llarg dels anys.<br>
                En els <b>dos últims anys</b> es veu, però, un <b>increment del 3% en el nivell baix</b>, cosa preocupant si es manté
                o segueix creixent</p>
            </div>
        </div>

        <footer>
            <p><strong>Font:</strong> Portal de dades obertes de la Generalitat de Catalunya (Dades proveïdes pel Departament d'Educació).</p>
            <p><strong>Metodologia:</strong> Anàlisi amb {total_students:,} observacions de {num_territories} àrees territorials.</p>
            <p>Visualització creada amb Plotly i Python per a l'assignatura de Visualització de Dades - UOC</p>
            <p><strong>Autora:</strong> Rita Roca Taxonera</p>
        </footer>
    </div>

    <script>
        // Renderitzem totes les visualitzacions per JavaScript
        var chart1Data = {chart1_json};
        var chart2Data = {chart2_json};
        var chart3Data = {chart3_json};
        var chart4Data = {chart4_json};

        console.log('Chart 1 traces:', chart1Data.data ? chart1Data.data.length : 'NO DATA');
        console.log('Chart 2 traces:', chart2Data.data ? chart2Data.data.length : 'NO DATA');

        Plotly.newPlot('chart1', chart1Data.data, chart1Data.layout, {{responsive: true}});
        Plotly.newPlot('chart2', chart2Data.data, chart2Data.layout, {{responsive: true}});
        Plotly.newPlot('chart3', chart3Data.data, chart3Data.layout, {{responsive: true}});
        Plotly.newPlot('chart4', chart4Data.data, chart4Data.layout, {{responsive: true}});
    </script>
</body>
</html>"""

# Write HTML file
with open('RitaRocaTaxonera_PRAC2_Storytelling.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("==========================================================")
print("Fitxer desat com: RitaRocaTaxonera_PRAC2_Storytelling.html")
print("==========================================================")