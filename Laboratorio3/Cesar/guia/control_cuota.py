"""Pausa y diagnóstico de cuota; no altera prompts, modelo ni respuestas guardadas."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,time
class ControlCuota:
    def __init__(self,carpeta,clave,intervalo=6.0):
        self.carpeta=Path(carpeta)
        self.clave=clave
        self.intervalo=intervalo
        self.ultima_peticion=None
        self.ultimo_error=None
    def antes(self):
        if self.ultima_peticion is not None:
            espera=self.intervalo-(time.monotonic()-self.ultima_peticion)
            if espera>0: time.sleep(espera)
        self.ultima_peticion=time.monotonic()
    def registrar(self,respuesta):
        if respuesta.status_code!=429: return
        try: cuerpo=respuesta.json()
        except ValueError: cuerpo={"mensaje":"HTTP 429 sin cuerpo JSON"}
        texto=json.dumps(cuerpo,ensure_ascii=False)
        if self.clave: texto=texto.replace(self.clave,"<CREDENCIAL_OCULTA>")
        diario=bool(re.search(r"(PerDay|per.day|por.d[ií]a)",texto,re.I))
        minuto=bool(re.search(r"(PerMinute|per.minute)",texto,re.I))
        demora=re.findall(r'"retryDelay"\s*:\s*"([0-9.]+)s"',texto)
        segundos=max(30,float(demora[-1])) if demora else 60
        error=dict(fecha_utc=datetime.now(timezone.utc).isoformat(),http_status=429,
            tipo_limite="diario" if diario else "minuto" if minuto else "sin_identificar",
            espera_sugerida=segundos,detalle=json.loads(texto))
        self.ultimo_error=error
        self.carpeta.mkdir(parents=True,exist_ok=True)
        ruta=self.carpeta/("cuota_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".json")
        ruta.write_text(json.dumps(error,ensure_ascii=False,indent=2),encoding="utf8")
    def puede_reintentar(self):
        return bool(self.ultimo_error) and self.ultimo_error["tipo_limite"]!="diario"
    def esperar(self):
        restante=self.ultimo_error["espera_sugerida"] if self.ultimo_error else 60
        print("Límite temporal o no identificado; espera acotada antes de reintentar.",flush=True)
        while restante>0:
            pausa=min(60,restante)
            time.sleep(pausa)
            restante-=pausa
def instalar_control(carpeta,clave,intervalo):
    import requests
    control=ControlCuota(carpeta,clave,intervalo)
    original=requests.post
    def post(url,*args,**kwargs):
        if "generativelanguage.googleapis.com" in url and ":generateContent" in url:
            r=original(url,*args,**kwargs)
            control.registrar(r)
            return r
        return original(url,*args,**kwargs)
    requests.post=post
    return control
