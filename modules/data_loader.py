import json
import os
import streamlit as st

def cargar_datos():
    if not os.path.exists("foods.json"):
        st.error("Archivo foods.json no encontrado.")
        return [], []

    with open("foods.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        desayunos = data.get("desayunos", [])
        comidas = data.get("comidas", [])
    return desayunos, comidas

def filtrar_platos(lista, tags_usuario):
    if not tags_usuario:
        return lista
    aptos = [p for p in lista if all(t in p.get("tags", []) for t in tags_usuario)]
    return aptos if aptos else lista
