import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter

def save_plot(counts, title, filename):
    """Guarda una figura básica."""
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def generate_html_report(analysis, output_dir="."):
    """Crea un reporte HTML simple basado en análisis ya procesado."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    html_file = os.path.join(output_dir, f"logistics_report_{timestamp}.html")
    
    # === Estadísticas ===
    sentiments = [x["sentiment"] for x in analysis if "sentiment" in x]
    sentiment_counts = Counter(sentiments)

    keywords = []
    for x in analysis:
        if "keywords" in x:
            keywords.extend(x["keywords"])
    keyword_counts = Counter(keywords).most_common(20)
    
    # === Guardar gráficos ===
    sentiment_plot = os.path.join(output_dir, f"sentiment_{timestamp}.png")
    save_plot(sentiment_counts, "Distribución de Sentimientos", sentiment_plot)

    keyword_plot = os.path.join(output_dir, f"keyword_freq_{timestamp}.png")
    save_plot(dict(keyword_counts), "Palabras clave más frecuentes", keyword_plot)

    # === Generar HTML ===
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Logistics Opinion Report</title>
    </head>
    <body>
        <h1>📦 Logistics Opinion Report</h1>
        <p>Generado: {timestamp}</p>

        <h2>📊 Distribución de sentimientos</h2>
        <img src="{sentiment_plot}" width="500">

        <h2>🔑 Palabras clave más frecuentes</h2>
        <img src="{keyword_plot}" width="500">

        <h2>📝 Datos Analizados</h2>
        <pre>{json.dumps(analysis[:20], indent=2, ensure_ascii=False)}</pre>
    </body>
    </html>
    """

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    return html_file
