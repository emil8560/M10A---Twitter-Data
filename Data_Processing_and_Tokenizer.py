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

def convert_to_list(type, list, data): # Funktion der tilføjer elementer fra dataframe til en liste
    for x in range(len(data)):
        list.append(data.loc[x, type])

convert_to_list('retweet_count',Retweets, tweetdata)
convert_to_list('favorite_count',Likes, tweetdata)

d = {'word':[], 'likes':[],'retweets':[],'comments':[],'n':[],
     'avg_likes':[],'avg_retweets':[],'avg_comments':[],'trafic':[]}
df = pd.DataFrame(data=d)
df
stop_count = 0
stop_value = 6000

for posts in range(len(tweetdata)):
    opdelt_tekst = tokenizer_spacy(tweetdata.loc[posts, 'full_text'])
    antal_likes = Likes[posts]
    antal_retweets = Retweets[posts]
    #antal_comments = Comments[posts]
    print(posts, "ud af ", len(tweetdata), "DataProcessing")
    stop_count = stop_count + 1
    if stop_count > stop_value:
        break
    for index_words in range(len(opdelt_tekst)):
        ord = opdelt_tekst[index_words]
        if df.loc[df['word'] == ord].empty == True:
            lenght = len(df) + 1
            df.loc[lenght, 'word'] = ord
            df.loc[lenght, 'likes'] = antal_likes
            df.loc[lenght, 'retweets'] = antal_retweets
            #df.loc[lenght, 'comments'] = antal_comments
            df.loc[lenght, 'n'] = 1
        else:
            row = df.index[df['word'] == ord]
            add_likes = df.loc[row, 'likes'] + antal_likes
            df.loc[row, 'likes'] = add_likes
            add_retweets = df.loc[row, 'retweets'] + antal_retweets
            df.loc[row, 'retweets'] = add_retweets
            #add_comments = df.loc[row, 'comments'] + antal_comments
            #df.loc[row, 'comments'] = add_comments
            add_n = df.loc[row, 'n'] + 1
            df.loc[row, 'n'] = add_n

for n in range(len(df)):
    print(n, "ud af", len(df), "Calc Avg")
    row = df.index[n]
    avg_likes = df.loc[row, 'likes'] / df.loc[row, 'n']
    df.loc[row, 'avg_likes'] = avg_likes
    avg_retweets = df.loc[row, 'retweets'] / df.loc[row, 'n']
    df.loc[row, 'avg_retweets'] = avg_retweets
    #avg_comments = df.loc[row, 'comments'] / df.loc[row, 'n']
    #df.loc[row, 'avg_comments'] = avg_comments
    trafic = df.loc[row, 'likes'] + df.loc[row, 'retweets'] # + df.loc[row, 'comments']
    df.loc[row, 'trafic'] = trafic



df.to_csv('midlertidigt_data.csv', float_format='%.0f')


# print(Retweets)
# print(Likes)
# print("antal posts med en retweets værdi:", len(Retweets))
# print("antal posts med en likes værdi:", len(Likes))
#
# print(tokenizer_spacy(tweetdata.loc[0, 'full_text']))


