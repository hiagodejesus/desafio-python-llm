from typing import Dict, List
import json
from collections import Counter
import plotly.express as px

from core.database import SessionLocal
from core.models import Classifications
from core.logger import get_logger

logger  = get_logger(__name__, "INFO")

session = SessionLocal()


def get_weekly_report():
    """
    Retorna relatório semanal com 5 gráficos obrigatórios
    Cache de 60 segundos para otimizar performance
    """
    try:      
        classificacoes = session.query(Classifications).all()        
        return _grafico_tags_mais_citadas(classificacoes),
    except Exception as e:
        return {"error": str(e)}


def _grafico_tags_mais_citadas(classificacoes: List[Classifications]) -> Dict:
    """Gráfico 3: Tags mais citadas (últimas 48h simuladas)"""
    ultimas_classificacoes = sorted(classificacoes, key=lambda x: x.id, reverse=True)[:100]
    
    todas_tags = []
    for c in ultimas_classificacoes:
        if c.tags:
            todas_tags.extend(c.tags)
    
    tags_count = Counter(todas_tags)
    top_tags = dict(tags_count.most_common(15))
    
    fig = px.pie(
        values=list(top_tags.values()),
        names=list(top_tags.keys()),
        title="Tags Mais Citadas (Últimas Classificações)"
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    statistics = {
        "html": fig.to_html(full_html=False, include_plotlyjs='cdn'),
        "json": json.loads(fig.to_json()),
        "dados": top_tags,
        "titulo": "Tags Mais Citadas",
        "insights": f"Tag mais popular: {max(top_tags, key=top_tags.get) if top_tags else 'N/A'}"
    }
    return statistics
