import pandas as pd
import spacy

tweetdata_path = "TestData/poltweets_sample.csv"
tweetdata = pd.read_csv(tweetdata_path)
nlp = spacy.load("da_core_news_sm") # Definerer model

Posts = []
Likes = []
Retweets = []
Comments = []

def tokenizer_spacy(text):  # Definerer funktion ud fra koden fra tidligere
    custom_stops = ["god", "al", "stor", "ny", "tak", "dag"]  # Definerer kontekstspecifikke stopord
    default_stopwords = list(nlp.Defaults.stop_words)  # Indlæser prædefineret stopordsliste
    stop_words = default_stopwords + custom_stops  # Danner samlet stopordsliste
    pos_tags = ['PROPN', 'ADJ', 'NOUN']  # Definerer POS-tags som skal bevares: egenavne, adjektiver og navneord

    doc = nlp(text)

    tokens = []

    for word in doc:  # Looper igennem hvert ord i tweet
        if word.lemma_.startswith("@"):  # Ord må ikke starte med @ - går videre til næste ord, hvis det gør
            continue
        if word.lemma_.startswith("#"):  # Ord må ikke starte med # - går videre til næste ord, hvis det gør
            continue
        if (len(word.lemma_) < 3):  # Ord må ikke være mindre end 3 karakterer - går videre til næste ord, hvis det er
            continue
        if (word.pos_ in pos_tags) and (
                word.lemma_ not in stop_words):  # Tjek at ordets POS-tag indgår i listen af accepterede tags og at ordet ikke er stopord
            # Bemærk at denne betingelse nås kun for dem, som ikke opfylder betingelserne fra de andre if-linjer
            tokens.append(word.lemma_)  # Tilføj ordets lemma til tokens, hvis if-betingelse er opfyldt

    return (tokens)