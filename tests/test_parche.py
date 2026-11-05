import pytest

from finnorte.reglas import validar_explicar






def test_ejemplo_parche_v4_respeta_el_esquema():
    import json
    from finnorte import prompts
    from finnorte.pipeline import validar_esquema

    p = prompts.cargar("rev_parche", 4)
    _, usuario = p.render(explicar='{"hallazgos": []}', codigo_original_json='"valor = 1\\n"')
    ejemplo = json.loads(usuario.split("Formato con un hallazgo:\n", 1)[1])
    assert len(ejemplo["parches"]) == 1
    assert validar_esquema(ejemplo, p.esquema) == []
    compile(ejemplo["codigo_corregido"], "<ejemplo-no-ejecutado>", "exec")
