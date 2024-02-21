import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import importlib.resources as resources

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from collections import Counter
from packagenlp.nlp import NLP

class ClassAnalyse:
    
    def __init__(self):
        self.nlp = NLP()
        self.data = None
        self.selected_column = None
        self.langue = None
        self.step_counter = 0
        self.completed_steps = []
        
            
    def main(self):
        resource_logo = "data/logo.png"
        chemin_image = resources.files('packagenlp').joinpath(resource_logo)
        image = Image.open(chemin_image)
        st.sidebar.image(image)
        menu = ["Accueil", "Data Processing"]
        choice = st.sidebar.selectbox("", menu)

        if choice == "Accueil":
            self.menu_acceuil()
        elif choice == "Data Processing":
            st.markdown("### Importation des données")
            self.menu_data_processing()
            st.markdown("---")            
            for i in range(3):
                self.step_counter += 1 
                st.markdown(f"### Étape {self.step_counter + 1}: Choisissez une fonction de prétraitement")
                self.process_data()
                st.markdown("---")
            self.token()
            st.markdown("---")
            self.histogramme()
            st.markdown("---")
            self.nuage_de_mots()
            st.markdown("---")
            self.bigrammes()
            st.markdown("---")
                 
    
    def menu_acceuil(self):
        st.title("Package NLP")
        st.write("\n")  # Ligne vide

        st.header("Informations")
        st.markdown("Initié le : 02/03/2023")
        st.markdown("Interlocuteurs : Marine CERCLIER, Grégory GAUTHIER, Tangi LE TALLEC, Alan BIGNON, Islem EZZINE, Killian FARRELL")
        st.markdown("Dans le cadre du projet interne DataScience Package NLP")
        st.write("\n")  # Ligne vide

        st.header("Présentation de la classe NLP")
        st.write("La classe NLP fournit un ensemble de méthodes pour le prétraitement du texte dans les langues française et anglaise. Voici une brève présentation de ses fonctionnalités principales:")
        st.write("- **cleanStopWord**: Nettoie un texte en retirant les StopWord spécifiés pour une langue donnée (français ou anglais). Prmet l'ajout ou la suppresion des StopWord")
        st.write("- **cleanText**: Nettoie le texte en retirant les accents, en convertissant le texte en minuscules, et en filtrant les caractères non désirés à l'aide d'une expression régulière. Permet de spécifier des exceptions dans les caractères à supprimer et offre la possibilité de conserver les chiffres.")
        st.write("- **lemmatisation**: Effectue la lemmatisation du texte en utilisant TreeTagger pour les langues française ou anglaise. Permet de conserver les nombres et d'exclure certains types de mots dans le processus de lemmatisation.")
        st.write("\nEnsemble, ces méthodes facilitent grandement le prétraitement du texte, ce qui est une étape cruciale dans de nombreux projets de traitement du langage naturel (NLP). La classe est conçue pour être facilement personnalisable et adaptable aux différents besoins et exigences des projets NLP.")
   
    def menu_data_processing(self):
        
        uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv",label_visibility='visible')
        separators = [",", ";", "/", "Autre"]
        selected_separator = st.selectbox("Sélectionnez un séparateur", separators)
    
        if selected_separator == "Autre":
            delimiter = st.text_input("Entrez le séparateur")
        else:
            delimiter = selected_separator

        if uploaded_file is not None and delimiter:
            try:
                self.data = pd.read_csv(uploaded_file, delimiter=delimiter)
                st.write(self.data)
            except Exception as e:
                st.error(f"Une erreur s'est produite lors de l'importation du fichier : {e}")

        if self.data is not None:
            self.selected_column = st.selectbox("Sélectionnez une colonne", self.data.columns)
            self.langue = st.selectbox("Sélectionnez la langue", ['','Français', 'English'])

    def process_data(self): 
        if self.data is None or self.data.empty:
            st.warning("Veuillez charger des données avant de procéder au prétraitement.")
            return

        st.markdown("#### Options de prétraitement")

        options = ["Pas de traitement", "Supprimer les mots vides", "Nettoyer le texte", "Lemmatisation"]
        options = [option for option in options if option not in self.completed_steps]

        for func in self.completed_steps:
            if func in options:
                options.remove(func)
            
        if not options:
            st.warning("Toutes les étapes de prétraitement ont été complétées.")
            return

        selected_function = st.selectbox(f"Étape {self.step_counter + 1}: Choisissez une fonction de prétraitement", options)
    
        if selected_function == "Supprimer les mots vides":
            st.markdown("##### Paramètres")
            add_stopwords = st.text_input("Ajouter des mots vides", "")
            remove_stopwords = st.text_input("Retirer des mots vides", "")
            if st.button("Appliquer Suppression des mots vides"):
                with st.spinner("Traitement en cours..."):
                    self.data[self.selected_column] = self.data[self.selected_column].apply(lambda text: self.nlp.cleanStopWord(text, self.langue, add_stopwords.split(","), remove_stopwords.split(",")))
                self.completed_steps.append(selected_function)
                self.completed_steps.append("Supprimer les mots vides")
                st.success("Traitement terminé!")

        elif selected_function == "Nettoyer le texte":
            st.markdown("##### Paramètres")
            keep_numbers = st.checkbox("Garder les chiffres", value=True)
            exception = st.text_input("Exceptions", "")
            remove_accent = st.checkbox("Supprimer les accents", value=True)
            lowercase = st.checkbox("Texte en minuscule", value=True)
            if st.button("Appliquer Nettoyage du texte"):
                with st.spinner("Traitement en cours..."):
                    self.data[self.selected_column] = self.data[self.selected_column].apply(lambda text: self.nlp.cleanText(text, keep_numbers, exception, remove_accent, lowercase))
                self.completed_steps.append(selected_function)
                st.success("Traitement terminé!")

        elif selected_function == "Lemmatisation":
            st.markdown("##### Paramètres")
            lemma_exclu = st.text_input("Lemmes à exclure", "")
            lemma_exclu_dict = {i.split(":")[0].strip(): (i.split(":")[1].strip() if len(i.split(":")) > 1 else None) for i in lemma_exclu.split(",") if i}
            keep_numbers = st.checkbox("Conserver les nombres", value=True)
            keep_type_word_input = st.text_input("Types de mots à conserver", "")
            keep_type_word = [i.strip() for i in keep_type_word_input.split(",") if i]
            if st.button("Appliquer Lemmatisation"):
                with st.spinner("Traitement en cours..."):
                    self.data[self.selected_column] = self.data[self.selected_column].apply(lambda x: self.nlp.lemmatisation(x, lemma_exclu_dict, self.langue, keep_numbers, keep_type_word))
                self.completed_steps.append(selected_function)
                st.success("Traitement terminé!")


                

                
    def find_common_bigrams(self, text):
        words = text.split()
        bigrams = [(words[i], words[i + 1]) for i in range(len(words) - 1)]
        bigram_counts = Counter(bigrams)
        common_bigrams = bigram_counts.most_common()
        
        return common_bigrams

    def token(self):
        st.markdown("### Étape 5: Téléchargement des tokens")

        # Vérifier si self.data et self.selected_column ne sont pas None
        if self.data is not None and self.selected_column is not None:
            # Fonction pour sauvegarder les tokens dans un fichier CSV
            def save_tokens_to_csv(column_data):
                # Création d'une nouvelle dataframe avec chaque token sur une nouvelle ligne
                all_tokens = []
                for row in column_data:
                    if isinstance(row, str):  # Vérification que la ligne est une chaîne de caractères
                        tokens = row.split()  # Tokenisation du texte
                        all_tokens.extend(tokens)

                # Création d'une DataFrame à partir de la liste des tokens
                df = pd.DataFrame(all_tokens, columns=['Token'])
                # Sauvegarde de la DataFrame en tant que fichier CSV
                csv_file_path = 'tokens.csv'
                df.to_csv(csv_file_path, index=False)

                return csv_file_path

            # Bouton de téléchargement du CSV
            download_button = st.download_button(
            label="Télécharger les tokens en tant que CSV",
            data=self.data[self.selected_column].to_csv(index=False),
            file_name='tokens.csv',
            mime='text/csv'
            )

            if download_button:
                st.success(f"Les tokens ont été téléchargés avec succès en tant que tokens.csv")
        else:
            st.warning("Veuillez charger des données et sélectionner une colonne avant de télécharger les tokens.")

            
            
    def histogramme(self):
        st.markdown("### Étape 6: Affichage de l'histogramme des mots les plus fréquents")

        # Vérifier si self.data et self.selected_column ne sont pas None
        if self.data is not None and self.selected_column is not None:
            
            if self.selected_column not in self.data.columns or not self.data[self.selected_column].apply(lambda x: isinstance(x, str)).all():
                st.warning("La colonne sélectionnée ne contient pas de texte (chaînes de caractères). Veuillez sélectionner une colonne valide.")
                return
            # Récupérez tous les tokens
            all_tokens = []
            for row in self.data[self.selected_column]:
                if isinstance(row, str):  # Vérification que la ligne est une chaîne de caractères
                    tokens = row.split()  # Tokenisation du texte
                    all_tokens.extend(tokens)

            # Utilisez Counter pour obtenir les fréquences
            token_counts = Counter(all_tokens)

            # Créez une série pour l'histogramme
            token_series = pd.Series(token_counts).sort_values(ascending=False)  # Trier dans l'ordre décroissant

            # Demandez à l'utilisateur combien de mots les plus fréquents ils veulent afficher
            top_n = st.selectbox("Sélectionnez le nombre de mots les plus fréquents à afficher", [10, 20, 50], index=0)

            # Créez un histogramme avec les top_n mots les plus fréquents
            fig = px.bar(token_series.head(top_n).reset_index(), x='index', y=0, labels={'index': 'Mots', 0: 'Fréquence'}, title=f'Top {top_n} des mots les plus fréquents')
            st.plotly_chart(fig)
        else:
            st.warning("Veuillez charger des données et sélectionner une colonne avant de générer un histogramme.")
        
    def nuage_de_mots(self):
        
        st.markdown("### Étape 7: Afficher le nuage de mots")
        # Vérifier si self.data et self.selected_column ne sont pas None
        if self.data is not None and self.selected_column is not None:
            # Vérification que la colonne sélectionnée contient des chaînes de caractères
            if self.selected_column not in self.data.columns or not self.data[self.selected_column].apply(lambda x: isinstance(x, str)).all():
                st.warning("La colonne sélectionnée ne contient pas de texte (chaînes de caractères). Veuillez sélectionner une colonne valide.")
                return
            # Récupération de tous les tokens
            all_tokens = []
            for row in self.data[self.selected_column]:
                if isinstance(row, str):
                    tokens = row.split()
                    all_tokens.extend(tokens)

            
            
            unique_words_count = len(set(all_tokens))
            
            resource_nuage = "data/Image.jpg"
            image_path = resources.files('packagenlp').joinpath(resource_nuage)
            mask = np.array(Image.open(image_path))
            image_colors = ImageColorGenerator(mask)
            
            # Définition de token_counts ici
            token_counts = Counter(all_tokens)
            
            # Générez le nuage de mots en utilisant les fréquences obtenues avec Counter
            wordcloud = WordCloud(width=800, height=400, background_color='white', min_font_size=5, max_words=unique_words_count, mask=mask, contour_color='black').generate_from_frequencies(token_counts)
            
            fig, ax = plt.subplots(figsize=(8, 4), facecolor=None)
            ax.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
        else:
            st.warning("Veuillez charger des données et sélectionner une colonne avant de générer un nuage de mots.")

        
    def bigrammes(self):
        st.markdown("### Étape 8: Afficher les bigrammes les plus courants")
        # Vérifier si self.data et self.selected_column ne sont pas None
        if self.data is not None and self.selected_column is not None:
        
            if self.selected_column not in self.data.columns or not self.data[self.selected_column].apply(lambda x: isinstance(x, str)).all():
                st.warning("La colonne sélectionnée ne contient pas de texte (chaînes de caractères). Veuillez sélectionner une colonne valide.")
                return
            # Concaténation de toutes les lignes de texte en une seule chaîne
            text = ' '.join(self.data[self.selected_column].dropna())
            
            # Trouver les bigrammes les plus courants
            common_bigrams = self.find_common_bigrams(text)
            
            # Option pour exclure des bigrammes spécifiques
            if st.checkbox('Exclure des bigrammes spécifiques'):
                exclude_bigram = st.text_input('Entrez le bigramme à exclure (séparez les mots par une virgule) :', value='').strip()
            else:
                exclude_bigram = ''

            # Filtrer les bigrammes pour exclure ceux spécifiés
            if exclude_bigram:
                exclude_bigram = tuple(map(str.strip, exclude_bigram.split(',')))
                
                common_bigrams = [
                    (bigram, count) for bigram, count in common_bigrams
                    if bigram != exclude_bigram
                    ]

            # Slider pour sélectionner le nombre de bigrammes à afficher
            num_bigrams = st.slider('Sélectionnez le nombre de bigrammes à afficher:', min_value=1, max_value=len(common_bigrams), value=10)
            
            # Préparer les données pour le tableau
            table_data = [
                {"Bigramme": f"{bigram[0]} {bigram[1]}", "Nombre d'occurrences": count}
                for bigram, count in common_bigrams[:num_bigrams]
                ]

            # Afficher les données sous forme de tableau
            st.table(pd.DataFrame(table_data))
        else:
                st.warning("Veuillez charger des données et sélectionner une colonne avant de générer les bigrammes.")
