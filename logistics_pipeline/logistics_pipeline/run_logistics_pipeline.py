import yaml
import os
from datetime import datetime

# === Importar motores principales de BettaFish ===
from QueryEngine.query import QueryEngine
from InsightEngine.insight import InsightEngine

# === Ruta al archivo de palabras clave ===
KEYWORDS_FILE = os.path.join(
    os.path.dirname(__file__), 
    "keywords_logistics.yaml"
)

def load_keywords():
    """Carga lista de palabras clave para logística."""
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["keywords"]

def run_pipeline():
    print("\n🚚 Logistics Opinion Pipeline — BettaFish Adaptation")
    print("=====================================================\n")

    # 1. Cargar palabras clave
    keywords = load_keywords()
    print(f"🔍 Palabras clave cargadas ({len(keywords)}): {keywords}\n")

    # 2. Crear motores de BettaFish
    query_engine = QueryEngine()
    insight_engine = InsightEngine()

    # 3. Realizar búsquedas web
    print("🌐 Buscando menciones globales...")
    all_results = []

    for kw in keywords:
        print(f"   → Buscando: {kw}")
        results = query_engine.search(kw)
        all_results.extend(results)

    print(f"\n📦 Total de entradas recolectadas: {len(all_results)}")

    # 4. Análisis profundo (sentimiento + temas)
    print("\n🧠 Analizando contenido con InsightEngine...")
    analysis = insight_engine.analyze(all_results)

    # 5. Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_file = f"logistics_report_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        import json
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"\n📁 Reporte guardado en: {output_file}")
    print("\n✨ Pipeline completado.\n")

if __name__ == "__main__":
    run_pipeline()
