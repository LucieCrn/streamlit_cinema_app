#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 23:56:46 2022

@author: Lucie
"""

###########
# Fonctions utiles à mon app cinéma Streamlit 
###########

import pandas as pd 

# Fonctions pour créer les listes de films, années de visionnage et notes. 
def get_movies(data):
    return sorted(data["Title"].unique().tolist())
    
def get_years(data) :
    return sorted(data["Viewing Year"].unique().tolist())

def get_release_year(data) :
    return sorted(data["Year"].unique().tolist())

def get_rates(data): 
    return sorted(data["Your Rating"].unique().tolist())

def get_imdb_rates(data): 
    return sorted(data["IMDb Rating"].unique().tolist())
    
def get_genres(data): 
    liste_des_genres = set(str(data["Genres"].tolist()).replace("[","").replace("]", "").replace("'", "").replace(",","").split())
    return sorted(liste_des_genres)



# Fonction pour appliquer les filtres de l'onglet "Watchlist". 

def filtre_watchlist(data, selected_genre, selected_year, selected_rates) :  
    # Application du filtre "année de réalisation"
    if selected_year == "All" :
        mes_films_year = data
    else : 
        mes_films_year = data[data["Year"] == selected_year]
        
    # Application du filtre "notes"
    mes_films_notes = mes_films_year.loc[(mes_films_year["IMDb Rating"] >= min(selected_rates)) & (mes_films_year["IMDb Rating"] <= max(selected_rates))]
    
    # Application du filtre "genre"
    mes_films_genre = pd.DataFrame()
    if selected_genre == "All" :
        mes_films_genre = mes_films_notes
    else : 
        for ligne in range(0, len(mes_films_notes)) : 
            if str(selected_genre) in mes_films_notes.iloc[ligne]["Genres"] :
                mes_films_genre = mes_films_genre.append(mes_films_notes.iloc[ligne])
            else :
                mes_films_genre = mes_films_genre
    mes_films_genre = mes_films_genre.reindex(columns = mes_films_notes.columns)
    
    watchlist_filtres = mes_films_genre.drop(["URL"], axis=1)
    watchlist_filtres["IMDb Rating"] = watchlist_filtres["IMDb Rating"].astype(int)
    watchlist_filtres["Year"] = watchlist_filtres["Year"].astype(int)
    watchlist_filtres["Runtime (mins)"] = watchlist_filtres["Runtime (mins)"].astype(int)
    watchlist_filtres.reset_index(drop=True, inplace=True)
    
    return watchlist_filtres



# Fonction pour appliquer les filtres de l'onglet "Films".  
    
def filtre_table(data, selected_year, selected_genre, selected_rates) : 
    # Application du filtre "année de visionnage"
    if selected_year == "All" :
        mes_films_year = data
    else : 
        mes_films_year = data[data["Viewing Year"] == str(selected_year)]
        
    # Application du filtre "notes"
    mes_films_notes = mes_films_year.loc[(mes_films_year["Your Rating"] >= min(selected_rates)) & (mes_films_year["Your Rating"] <= max(selected_rates))]
    
    # Application du filtre "genre"
    mes_films_genre = pd.DataFrame()
    if selected_genre == "All" :
        mes_films_genre = mes_films_notes
    else : 
        for ligne in range(0, len(mes_films_notes)) : 
            if str(selected_genre) in mes_films_notes.iloc[ligne]["Genres"] :
                mes_films_genre = mes_films_genre.append(mes_films_notes.iloc[ligne])
            else :
                mes_films_genre = mes_films_genre
    mes_films_genre = mes_films_genre.reindex(columns = mes_films_notes.columns)
    
    mes_films_filtres = mes_films_genre.drop(["Unnamed: 0", "URL", "Date Rated", "IMDb Rating"], axis=1)
    mes_films_filtres["Your Rating"] = mes_films_filtres["Your Rating"].astype(int)
    mes_films_filtres["Year"] = mes_films_filtres["Year"].astype(int)
    mes_films_filtres["Runtime (mins)"] = mes_films_filtres["Runtime (mins)"].astype(int)
    mes_films_filtres.reset_index(drop=True, inplace=True)
    
    return mes_films_filtres