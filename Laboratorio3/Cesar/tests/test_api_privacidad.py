import pytest
from finnorte import llm, trazas

def test_error_del_proveedor_no_expone_llave(monkeypatch):
    llave = "llave_sintetica_para_regresion"
    monkeypatch.setenv("GEMINI_API_KEY", llave)
    def proveedor(*args):
        raise llm.LLMError("Error de prueba " + llave)
    monkeypatch.setitem(llm._PROVEEDORES, "gemini", proveedor)
    with pytest.raises(llm.LLMError) as exc:
        llm.generar("prueba", proveedor="gemini")
    assert llave not in str(exc.value)
    assert llave not in str(trazas.leer())
    assert "CREDENCIAL_OCULTA" in str(exc.value)
