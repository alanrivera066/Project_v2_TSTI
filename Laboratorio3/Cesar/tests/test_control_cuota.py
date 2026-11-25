import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"guia"))
from control_cuota import ControlCuota
class Respuesta:
    status_code=429
    def __init__(self,datos): self.datos=datos
    def json(self): return self.datos
def test_cuota_diaria_detiene_y_oculta_clave(tmp_path):
    control=ControlCuota(tmp_path,"secreto_sintetico")
    control.registrar(Respuesta({"error":{"message":"secreto_sintetico","details":[{"quotaId":"GenerateRequestsPerDayPerProject"}]}}))
    assert not control.puede_reintentar()
    assert "secreto_sintetico" not in next(tmp_path.glob("*.json")).read_text(encoding="utf8")
def test_cuota_minuto_permite_reintento(tmp_path):
    control=ControlCuota(tmp_path,"")
    control.registrar(Respuesta({"error":{"details":[{"quotaId":"GenerateRequestsPerMinutePerProject"},{"retryDelay":"48s"}]}}))
    assert control.puede_reintentar()
    assert control.ultimo_error["espera_sugerida"]==48
def test_pausa_respeta_intervalo(tmp_path,monkeypatch):
    import control_cuota
    tiempos=iter([100,102,106])
    pausas=[]
    monkeypatch.setattr(control_cuota.time,"monotonic",lambda:next(tiempos))
    monkeypatch.setattr(control_cuota.time,"sleep",pausas.append)
    control=ControlCuota(tmp_path,"",6)
    control.antes()
    control.antes()
    assert pausas==[4]
