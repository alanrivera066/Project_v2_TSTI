"""Verifica el cierre guardado sin ejecutar Gemini ni modificar sus respuestas."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
import xml.etree.ElementTree as ET

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / 'bitacora/proceso_gemini/20261125T002950Z'

def leer(p):
    return p.read_text(encoding='utf8')

def objeto(p):
    return json.loads(leer(p))

def guardar(p, dato):
    p.write_text(json.dumps(dato, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    assert objeto(BASE/'estado.json')['estado'] == 'completo'
    firma = objeto(BASE/'evaluacion/firma.json')
    firmados = {}
    for original, esperado in firma['sha256'].items():
        ruta = Path(original)
        if not ruta.exists():
            relativo = original.replace('\\', '/').split('/finnorte-ia-alumno/', 1)[1]
            ruta = RAIZ/relativo
        assert sha(ruta) == esperado, f'Insumo cambiado: {ruta.name}'
        firmados[ruta.relative_to(RAIZ).as_posix()] = esperado
    resumen = objeto(BASE/'evaluacion/resumen.json')
    docente = objeto(BASE/'evaluacion/analisis_docente/resumen_docente.json')
    assert resumen['ejecuciones'] == 192 and docente['respuestas_modificadas'] == 0
    casos = [json.loads(l)['id'] for l in leer(RAIZ/'evals/comun.jsonl').splitlines() if l.strip()]
    respuestas = {}
    for config in 'ABCD':
        archivos = list((BASE/'evaluacion'/config).glob('*.json'))
        assert len(archivos) == 48
        for c in casos:
            for n in range(1, 4):
                p = BASE/'evaluacion'/config/f'{c}_{n}.json'
                d = objeto(p)
                assert (d['config'],d['caso'],d['repeticion']) == (config,c,n)
                respuestas[p.relative_to(RAIZ).as_posix()] = sha(p)
    actual = RAIZ/'bitacora/gemini_estado_actual.json'
    historico = RAIZ/'bitacora/gemini_estado_antes_cierre.json'
    if not historico.exists() and objeto(actual)['estado'] != 'completo':
        historico.write_bytes(actual.read_bytes())
    previas = objeto(historico)['sha256_respuestas_previas']
    for nombre, esperado in previas.items():
        p = RAIZ/Path(nombre)
        assert sha(p) == esperado, f'Respuesta anterior modificada: {nombre}'
    ultima = objeto(RAIZ/'bitacora/validacion_oficial/ultima_ejecucion.json')
    pruebas = []
    # La fecha se conserva en el paquete; permite verificar el mismo registro en otro equipo.
    carpeta = RAIZ/'bitacora/validacion_oficial'/Path(ultima['directorio']).name
    for nombre in ('controles_lab3','suite_local','equipo_a1_a2_av1'):
        arbol = ET.parse(carpeta/(nombre+'.xml'))
        suites = list(arbol.getroot().iter('testsuite'))
        totales = {k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
        assert totales['errors'] == totales['failures'] == 0
        pruebas.append(dict(grupo=nombre,aprobadas=totales['tests']-totales['skipped'],omitidas=totales['skipped'],
                            junit=(carpeta/(nombre+'.xml')).relative_to(RAIZ).as_posix()))
    assert [(x['aprobadas'],x['omitidas']) for x in pruebas] == [(3,0),(51,6),(11,0)]
    guardar(RAIZ/'bitacora/validacion_oficial/resumen_resultados.json',dict(ejecucion=carpeta.name,grupos=pruebas,
        alcance_equipo='Instantanea parcial de A1/A2/AV1, no suite completa del repositorio',
        commit_equipo='6c1835b1a556240382c3d678ecec6bf0af6f5948'))
    integridad = dict(fecha_verificacion_utc=datetime.now(timezone.utc).isoformat(),estado='completo',
        respuestas=192,casos=16,repeticiones=3,configuraciones=list('ABCD'),insumos_firmados=firmados,
        respuestas_sha256=respuestas,respuestas_previas_preservadas=len(previas),
        modelo=resumen['modelo'],embeddings=resumen['embeddings'],umbral=resumen['umbral'],
        analisis_docente_sin_nuevas_llamadas=docente['llamadas_nuevas_modelo']==0,
        evaluador_docente_sha256=sha(RAIZ/'referencias/evaluacion_docente_original.py'),
        informe_sha256=sha(RAIZ/'entrega/Laboratorio3_Revisor_Codigo.pdf'))
    guardar(BASE/'integridad_final.json',integridad)
    guardar(actual,dict(estado='completo',umbral=resumen['umbral'],respuestas_guardadas=192,respuestas_previstas=192,
        modelo=resumen['modelo'],embeddings=resumen['embeddings'],
        evidencia=BASE.relative_to(RAIZ).as_posix(),integridad=(BASE/'integridad_final.json').relative_to(RAIZ).as_posix(),
        consistencia_docente='Estabilidad del acierto booleano',consistencia_literal='Conservada como metrica adicional',
        nota='Se conserva el fallo c10; no se ajusto el umbral con el conjunto final.'))
    print(json.dumps(dict(estado='completo',respuestas=len(respuestas),firmados=len(firmados),previas_preservadas=len(previas),pruebas=pruebas)))

if __name__ == '__main__':
    main()
