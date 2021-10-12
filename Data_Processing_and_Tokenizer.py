import pandas as pd
import spacy
import datetime

tweetdata_path = "Data/parti_data.csv"
tweetdata = pd.read_csv(tweetdata_path)
nlp = spacy.load("da_core_news_sm") # Definerer model
proces_start = datetime.datetime.now()

def tokenizer_spacy(text):  # Definerer funktion ud fra koden fra tidligere
    custom_stops = ["dkpol","ad", "af", "aldrig", "alene", "alle", "allerede", "alligevel", "alt", "altid", "anden", "andet",
                    "andre", "at", "bag", "bare", "begge", "bl.a.", "blandt", "blev", "blive", "bliver", "burde",
                    "bør", "ca.", "da", "de", "dem", "den", "denne", "dens", "der", "derefter", "deres", "derfor",
                    "derfra", "deri", "dermed", "derpå", "derved", "det", "dette", "dig", "din", "dine", "disse",
                    "dit", "dog", "du", "efter", "egen", "ej", "eller", "ellers", "en", "end", "endnu", "ene",
                    "eneste", "enhver", "ens", "enten", "er", "et", "f.eks.", "far", "fem", "fik", "fire", "flere",
                    "flest", "fleste", "for", "foran", "fordi", "forrige", "fra", "fx", "få", "får", "før", "først",
                    "gennem", "gjorde", "gjort", "god", "godt", "gør", "gøre", "gørende", "ham", "han", "hans", "har",
                    "havde", "have", "hej", "hel", "heller", "helt", "hen", "hende", "hendes", "henover", "her",
                    "herefter", "heri", "hermed", "herpå", "hos", "hun", "hvad", "hvem", "hver", "hvilke", "hvilken",
                    "hvilkes", "hvis", "hvor", "hvordan", "hvorefter", "hvorfor", "hvorfra", "hvorhen", "hvori",
                    "hvorimod", "hvornår", "hvorved", "i", "igen", "igennem", "ikke", "imellem", "imens", "imod",
                    "ind", "indtil", "ingen", "intet", "ja", "jeg", "jer", "jeres", "jo", "kan", "kom", "komme",
                    "kommer", "kun", "kunne", "lad", "langs", "lav", "lave", "lavet", "lidt", "lige", "ligesom",
                    "lille", "længere", "man", "mand", "mange", "med", "meget", "mellem", "men", "mens", "mere",
                    "mest", "mig", "min", "mindre", "mindst", "mine", "mit", "mod", "må", "måske", "ned", "nej",
                    "nemlig", "ni", "nogen", "nogensinde", "noget", "nogle", "nok", "nu", "ny", "nyt", "når", "nær",
                    "næste", "næsten", "og", "også", "okay", "om", "omkring", "op", "os", "otte", "over", "overalt",
                    "pga.", "på", "samme", "sammen", "se", "seks", "selv", "selvom", "senere", "ser", "ses", "siden",
                    "sig", "sige", "sin", "sine", "sit", "skal", "skulle", "som", "stadig", "stor", "store", "synes",
                    "syntes", "syv", "så", "sådan", "således", "tag", "tage", "temmelig", "thi", "ti", "tidligere",
                    "til", "tilbage", "tit", "to", "tre", "ud", "uden", "udover", "under", "undtagen", "var", "ved",
                    "vi", "via", "vil", "ville", "vor", "vore", "vores", "vær", "være", "været", "øvrigt"]  
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
                word.lemma_ not in stop_words):
            tokens.append(word.lemma_)

    return (tokens)

def convert_to_list(type, list, data): # Funktion der tilføjer elementer fra dataframe til en liste
    for x in range(len(data)):
        list.append(data.loc[x, type])

def post_to_df(data, df):
    stop_count = 0
    stop_value = 100000

    Likes = []
    Retweets = []
    Comments = []

    convert_to_list('retweet_count', Retweets, data)
    convert_to_list('like_count', Likes, data)
    convert_to_list('reply_count', Comments, data)


    for posts in range(len(data)):
        opdelt_tekst = tokenizer_spacy(data.loc[posts, 'text'])
        antal_likes = Likes[posts]
        antal_retweets = Retweets[posts]
        antal_comments = Comments[posts]
        if posts % 10 == 0:
            print(posts, "ud af ", len(data), "DataProcessing")
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
                df.loc[lenght, 'comments'] = antal_comments
                df.loc[lenght, 'n'] = 1
            else:
                row = df.index[df['word'] == ord]
                add_likes = df.loc[row, 'likes'] + antal_likes
                df.loc[row, 'likes'] = add_likes
                add_retweets = df.loc[row, 'retweets'] + antal_retweets
                df.loc[row, 'retweets'] = add_retweets
                add_comments = df.loc[row, 'comments'] + antal_comments
                df.loc[row, 'comments'] = add_comments
                add_n = df.loc[row, 'n'] + 1
                df.loc[row, 'n'] = add_n

def create_dataframe(name):
    d = {'word': [], 'likes': [], 'retweets': [], 'comments': [], 'n': [],
         'avg_likes': [], 'avg_retweets': [], 'avg_comments': [], 'trafic': [], 'party': []}
    name = pd.DataFrame(data=d)


def calc_average(df, parti):
    for n in range(len(df)):
        if n % 10 == 0:
            print(n, "ud af", len(df), "Calc Avg")
        row = df.index[n]
        avg_likes = df.loc[row, 'likes'] / df.loc[row, 'n']
        df.loc[row, 'avg_likes'] = avg_likes
        avg_retweets = df.loc[row, 'retweets'] / df.loc[row, 'n']
        df.loc[row, 'avg_retweets'] = avg_retweets
        avg_comments = df.loc[row, 'comments'] / df.loc[row, 'n']
        df.loc[row, 'avg_comments'] = avg_comments
        trafic = df.loc[row, 'likes'] + df.loc[row, 'retweets']  # + df.loc[row, 'comments']
        df.loc[row, 'trafic'] = trafic
        df.loc[row, 'party'] = parti

def df_to_csv(df, name):
    df.to_csv(name, float_format='%.0f')
    print(name, "saved")

# ------- Parti Variable ---------
DanskDf1995 = []
LiberalAlliance = []
KonservativeDK = []
venstredk = []
radikale = []
Spolitik = []
Enhedslisten = []
All = []

d = {'word': [], 'likes': [], 'retweets': [], 'comments': [], 'n': [],
     'avg_likes': [], 'avg_retweets': [], 'avg_comments': [], 'trafic': [], 'party': []}

DanskDf1995 = pd.DataFrame(data=d)
LiberalAlliance = pd.DataFrame(data=d)
KonservativeDK = pd.DataFrame(data=d)
venstredk = pd.DataFrame(data=d)
radikale = pd.DataFrame(data=d)
Spolitik = pd.DataFrame(data=d)
Enhedslisten = pd.DataFrame(data=d)
All = pd.DataFrame(data=d)

DanskDf1995_sorted = tweetdata[tweetdata['username'] == "DanskDf1995"]
LiberalAlliance_sorted = tweetdata[tweetdata['username'] == "LiberalAlliance"]
KonservativeDK_sorted = tweetdata[tweetdata['username'] == "KonservativeDK"]
venstredk_sorted = tweetdata[tweetdata['username'] == "venstredk"]
radikale_sorted = tweetdata[tweetdata['username'] == "radikale"]
Spolitik_sorted = tweetdata[tweetdata['username'] == "Spolitik"]
Enhedslisten_sorted = tweetdata[tweetdata['username'] == "Enhedslisten"]

DanskDf1995_sorted.reset_index(inplace=True)
LiberalAlliance_sorted.reset_index(inplace=True)
KonservativeDK_sorted.reset_index(inplace=True)
venstredk_sorted.reset_index(inplace=True)
radikale_sorted.reset_index(inplace=True)
Spolitik_sorted.reset_index(inplace=True)
Enhedslisten_sorted.reset_index(inplace=True)

# ---------- RUN TIME Main ------------


# post_to_df(DanskDf1995_sorted, DanskDf1995)
# post_to_df(LiberalAlliance_sorted, LiberalAlliance)
# post_to_df(KonservativeDK_sorted, KonservativeDK)
# post_to_df(venstredk_sorted, venstredk)
# post_to_df(radikale_sorted, radikale)
# post_to_df(Spolitik_sorted, Spolitik)
# post_to_df(Enhedslisten_sorted, Enhedslisten)
post_to_df(tweetdata, All)

# calc_average(DanskDf1995, "Danske Folkeparti")
# calc_average(LiberalAlliance, "Liberal Alliance")
# calc_average(KonservativeDK, "Konservative Folkeparti")
# calc_average(venstredk, "Venstre")
# calc_average(radikale, "Radikale")
# calc_average(Spolitik, "Socialistisk Folkeparti")
# calc_average(Enhedslisten, "Enhedslisten")
calc_average(All, "All")

# df_to_csv(DanskDf1995, "DF.csv")
# df_to_csv(LiberalAlliance, "LA.csv")
# df_to_csv(KonservativeDK, "konservative.csv")
# df_to_csv(venstredk, "venstre.csv")
# df_to_csv(radikale, "radikale.csv")
# df_to_csv(Spolitik, "spolitik.csv")
# df_to_csv(Enhedslisten, "enhedslisten.csv")
df_to_csv(All, "All.csv")

proces_end = datetime.datetime.now()
difference = proces_end - proces_start
print("RunTime: ", difference)