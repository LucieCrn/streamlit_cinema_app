#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:54:38 2022

@author: Lucie
"""

# Importer les librairies.
#import pip
#pip.main(["install","matplotlib"])
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from Movie_Database_Build import search_poster
import fonctions as fct

# Chemins
file = os.path.dirname(__file__)
base_films = os.path.join(file, "data.csv")
base_watchlist = os.path.join(file, "WATCHLIST.csv")
folder_affiches = os.path.join(file, "Affiches")
folder_photos_onglet = os.path.join(file, "Photos_onglets")


# Importer les données pour l'onglet "films"
mes_films = pd.read_csv(base_films)

# Importer les données pour l'onglet "watchlist" et suppression des colonnes inutiles
watchlist_brut = pd.read_csv(base_watchlist)
watchlist = watchlist_brut.drop(['Const',
                                 'Created',
                                 'Modified',
                                 "Description",
                                 "Title Type",
                                 "Num Votes",
                                 "Your Rating",
                                 "Date Rated",
                                 "Position"],
                                axis=1)

#############

# Page si onglet "Films" séléctionné : 
def onglet_films() : 
 
    
# PARTIE HAUTE DE L'APP

    
    # Création d'un bandeau avec des affiches de films. 
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col3 : 
        st.image(os.path.join(folder_photos_onglet, "Film1.png"), use_column_width='always')
        
    with col2 : 
        st.image(os.path.join(folder_photos_onglet, "Film2.jpeg"), use_column_width='always')
    
    with col1 : 
        st.image(os.path.join(folder_photos_onglet, "Film3.jpeg"), use_column_width='always')
        
    with col5 : 
        st.image(os.path.join(folder_photos_onglet, "Film5.jpeg"), use_column_width='always')
        
    with col4 : 
        st.image(os.path.join(folder_photos_onglet, "Film4.jpeg"), use_column_width='always')
        
    st.write('<h1 style="text-align:center;color:#FFDD99;font-weight:bolder;font-size:60px;">MES FILMS 🍿</h1>',unsafe_allow_html=True)    
  
    
# OUTILS DE SELECTION - INTERRACTION AVEC L'UTILISATEUR
    
    # Titre de la section
    st.subheader("FILTRES")
    
    # Création des colonnes
    col1, col2, col3 = st.columns(3)
    
    # Création du menu déroulant pour les années
    with col1 : 
        years_list = ['All'] + fct.get_years(mes_films)    
        selected_year = st.selectbox('Choisir une année de visionnage', years_list)
        
    # Création du menu déroulant pour les genres
    with col2 :
        genres_list = ['All'] + fct.get_genres(mes_films)    
        selected_genre = st.selectbox('Choisir un genre', genres_list)
        
    # Choix d'afficher les affiches des films ou non : 
    with col3 : 
        choix_affiche = st.selectbox("Afficher les affiches des films (attention très lent)", ["Non", "Oui"])
        
    # Création de la selection des notes. 
    selected_rates = st.slider('Afficher les notes comprises entre :', 0, 10, (0, 10))

    
    # Afficher le nombre de film
    st.markdown("---")
    # Appliquer les filtres à la dataframe
    nombre_films = fct.filtre_table(mes_films, selected_year, selected_genre, selected_rates).shape[0]
    st.subheader(f"Nombre de films : {nombre_films}")

    
    
# CREATION DES GRAPHIQUES ET DE LA VISUALISATION DE LA TABLE

    col1, col2 = st.columns(2)
    
    # Graphique de la réparttion des notes : 
    with col1 : 
        mes_films_filtre = fct.filtre_table(mes_films, selected_year, selected_genre, selected_rates)
        fig, ax = plt.subplots()
        ax.hist(mes_films_filtre["Your Rating"], color = "pink", edgecolor = "black")
        plt.xlabel('Notes des films')
        plt.ylabel('Nombre de films notés')
        plt.xticks(rotation=45)
        plt.title("Répartition des notes")
        st.pyplot(fig)
        
    # Nombre de films vus par année :
    with col2 : 
        mes_films_filtre = fct.filtre_table(mes_films, selected_year, selected_genre, selected_rates)
        fig, ax = plt.subplots()
        ax.hist(mes_films_filtre["Viewing Year"], color = "pink", edgecolor = "black")
        plt.xlabel('Années')
        plt.ylabel('Nombre de films notés')
        plt.xticks(rotation=45)
        plt.title("Nombre de films visionnés par année")
        st.pyplot(fig)
        

        
    # Afficher la table avec les filtres
    st.markdown("---")
    st.write(fct.filtre_table(mes_films, selected_year, selected_genre, selected_rates))



    # Afficher les films avec leur affiche
    if choix_affiche == "Oui" :
         st.markdown("---")
         col1, col2, col3, col4 = st.columns(4)
        
         mes_films_liste = fct.get_movies(mes_films_filtre)
         x=0
         for film in mes_films_liste :  
             # Chercher l'affiche et la stocker, puis récupérer l'URL IMDb
             search_poster(film)
             affiche = (f"{film}.jpg")
             chemin_none = os.path.join(folder_affiches, "None.jpg")
             chemin = os.path.join(folder_affiches, affiche)
             url = mes_films.loc[(mes_films["Title"] == film), "URL"]
             url_bis = str(url).split()[1]
    
           
             # Organiser les infos en colonnes avec affiche + nom du film dessous avec lien cliquable
             x=x+1
             if x>4 : 
                 x = x-4
                
            
             if x==1 : 
                 with col1 : 
                     if os.path.isfile(chemin) : 
                         st.image(chemin, width=200)
                     else : 
                         st.image(chemin_none, width=200)
                     st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                     continue
                 continue
    
             elif x==2 : 
                  with col2 : 
                     if os.path.isfile(chemin) : 
                         st.image(chemin, width=200)
                     else : 
                         st.image(chemin_none, width=200)
                     st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                     continue
                  continue
                
             elif x==3 : 
                  with col3 : 
                     if os.path.isfile(chemin) : 
                         st.image(chemin, width=200)
                     else : 
                         st.image(chemin_none, width=200)
                     st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                     continue
                  continue
             
             elif x==4 : 
                  with col4 : 
                     if os.path.isfile(chemin) : 
                         st.image(chemin, width=200)
                     else : 
                         st.image(chemin_none, width=200)
                     st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                     continue
                  continue
                        



#############

# Page si l'onglet "watchlist" est sélectionné : 
    
def onglet_watchlist() :      
    
    # Images pour le bandeau
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col2 : 
        st.image(os.path.join(folder_photos_onglet, "Watchlist1.png"), width=80)
    
    with col6 : 
        st.image(os.path.join(folder_photos_onglet, "Watchlist6.png"), width=120)
        
    with col1 : 
        st.image(os.path.join(folder_photos_onglet, "Watchlist2.png"), width=60)
    
    with col4 : 
        st.image(os.path.join(folder_photos_onglet, "Watchlist4.png"), width=80)
    
    with col3 : 
        st.image(os.path.join(folder_photos_onglet, "Watchlist3.png"), width=80)
        
    with col5 : 
        st.image(os.path.join(folder_photos_onglet, "Watchlist5.png"), width=70)
    
    # Titre de la page 
    st.write('<h1 style="text-align:center;color:purple;font-weight:bolder;font-size:60px;">MA WATCHLIST 🎥</h1>',unsafe_allow_html=True)    
    
    # Création de menu déroulant pour les années et les genres
    col1, col2 = st.columns(2)
    
    with col1 :
        genres_watchlist = ['All'] + fct.get_genres(watchlist)    
        selected_genre = st.selectbox('Choisir un genre', genres_watchlist)
        
    with col2 :
        years_watchlist = ['All'] + fct.get_release_year(watchlist)    
        selected_year = st.selectbox('Choisir une année de réalisation', years_watchlist)

       
    
    # Création de la selection des notes. 
    selected_rates = st.slider('Afficher les notes IMBd comprises entre :', 0, 10, (0, 10))
    
    # Création de la DF filtrée. 
    watchlist_filtre = fct.filtre_watchlist(watchlist, selected_genre, selected_year, selected_rates)
    
    # Afficher le nombre de film
    st.markdown("---")
    nombre_films = watchlist_filtre.shape[0]
    st.subheader(f"Nombre de films : {nombre_films}")
        
            
    # Affiche la table avec un séparateur
    st.markdown("---")
    st.write(watchlist_filtre)
    
    # Afficher les films avec leur affiche
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    watchlist_films = fct.get_movies(watchlist_filtre)
    x=0
    for film in watchlist_films :  
        # Chercher l'affiche et la stocker, puis récupérer l'URL IMDb
        search_poster(film)
        affiche = (f"{film}.jpg")
        chemin_none = os.path.join(folder_affiches, "None.jpg")
        chemin = os.path.join(folder_affiches, affiche)
        url = watchlist.loc[(watchlist["Title"] == film), "URL"]
        url_bis = str(url).split()[1]

       
        # Organiser les infos en colonnes avec affiche + nom du film dessous avec lien cliquable
        x=x+1
        if x>3 : 
            x = x-3
            
        
        if x==1 : 
            with col1 : 
                if os.path.isfile(chemin) : 
                    st.image(chemin, width=200)
                else : 
                    st.image(chemin_none, width=200)
                st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                continue
            continue

        elif x==2 : 
             with col2 : 
                if os.path.isfile(chemin) : 
                    st.image(chemin, width=200)
                else : 
                    st.image(chemin_none, width=200)
                st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                continue
             continue
            
        elif x==3 : 
             with col3 : 
                if os.path.isfile(chemin) : 
                    st.image(chemin, width=200)
                else : 
                    st.image(chemin_none, width=200)
                st.markdown(f'<a href="{url_bis}">{film}</a>', unsafe_allow_html=True)
                continue
             continue
                        
                
        
#############
       
def main() : 
    
    st.set_page_config(layout="wide")
    
# COLONNE POUR LA SELECTION DE LA PAGE
    
    st.sidebar.image(os.path.join(folder_photos_onglet, "Image_accueil.png"))
    
    menu = st.sidebar.radio("",("Films", "Watchlist"),)
    if menu == 'Films':
        onglet_films()
    elif menu == 'Watchlist':   
        onglet_watchlist()
    
    
    # Lien vers Allociné et IMDb
    st.sidebar.markdown("---")
    st.sidebar.markdown('<a href="http://allocine.fr">Lien vers le site Allociné</a>', unsafe_allow_html=True)
    st.sidebar.markdown('<a href="http://imdb.com">Lien vers le site IMDb</a>', unsafe_allow_html=True)
    
    
    # Légende des notes : 
    st.sidebar.markdown("---")
    st.sidebar.subheader("Légende pour mes notes :")
    st.sidebar.write("10 : coup de coeur")
    st.sidebar.write("9 : excellent")
    st.sidebar.write("8 : très bien")
    st.sidebar.write("7 : bien")
    st.sidebar.write("6 : pas mal")
    st.sidebar.write("5 : moyen")
    st.sidebar.write("4 : pas terrible")
    st.sidebar.write("3 : mauvais")
    st.sidebar.write("2 : très mauvais")
    st.sidebar.write("1 : ennui total")



    
    
if __name__ == '__main__':
    main()
