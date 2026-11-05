"""Consulta la configuración sin mostrar llaves."""
import argparse
from .config import config

def main():
    p = argparse.ArgumentParser(prog='finnorte')
    p.add_argument('comando', choices=['info'])
    p.parse_args()
    c = config()
    print(f'LLM: {c.llm_proveedor} / {c.llm_modelo}\nEmbeddings: {c.emb_proveedor} / {c.emb_modelo}')

if __name__ == '__main__':
    main()
