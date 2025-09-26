from app.agent.seo_agent.agent import create_seo_agent
from app.agent.seo_agent.tools.analyze_url import analyze_url_for_seo

def test_seo_agent_contract():
    seo_agent_instance = create_seo_agent()
    assert analyze_url_for_seo in seo_agent_instance.tools