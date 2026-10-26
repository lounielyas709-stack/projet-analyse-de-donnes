import pandas as pd

MOTS_CLES_IA = (
    r"\b(?:AI|A\.I\.|AGI|LLMs?|ChatGPT|GPT-?\d|OpenAI|Anthropic|Llama|LLaMA|Mistral|DeepSeek|Grok|Copilot"
    r"|Midjourney|DALL-?E|Stable Diffusion)\b"
    r"|\bClaude\b(?! Shannon)"
    r"|(?i:machine learning|deep learning|neural net)"
)
LANCEMENT_GOOGLE_GEMINI = pd.Timestamp("2023-12-01", tz="UTC")

PARAMETRES_DE_SUIVI = {"ref", "ref_src", "fbclid", "gclid", "_fb_noscript", "usp", "source", "hn", "s"}

NOMS_DES_LABOS = {
    "Google": "Google",
    "Google AI": "Google",
    "Google Brain": "Google",
    "Google Cloud": "Google",
    "Google DeepMind": "Google",
    "Google Research": "Google",
    "DeepMind": "Google",
    "Meta AI": "Meta",
    "Facebook": "Meta",
    "Facebook AI": "Meta",
    "Facebook AI Research": "Meta",
    "Microsoft": "Microsoft",
    "Microsoft Research": "Microsoft",
    "Microsoft Research Asia": "Microsoft",
    "Microsoft Research AI for Science": "Microsoft",
    "Alibaba": "Alibaba",
    "Alibaba DAMO Academy": "Alibaba",
}


def parle_d_ia(titres, dates):
    mentionne_ia = titres.str.contains(MOTS_CLES_IA, regex=True)
    mentionne_google_gemini = titres.str.contains(r"\bGemini\b", regex=True) & (dates >= LANCEMENT_GOOGLE_GEMINI)
    return mentionne_ia | mentionne_google_gemini


def est_un_parametre_de_suivi(cle):
    return cle.startswith(("utm_", "X-Amz-")) or cle in PARAMETRES_DE_SUIVI


def retirer_parametres_de_suivi(url):
    if pd.isna(url) or "?" not in url:
        return url
    debut, parametres = url.split("?", 1)
    parametres, _, ancre = parametres.partition("#")
    parametres_gardes = [p for p in parametres.split("&") if p and not est_un_parametre_de_suivi(p.split("=")[0])]
    url_nettoyee = debut + ("?" + "&".join(parametres_gardes) if parametres_gardes else "")
    return url_nettoyee + ("#" + ancre if ancre else "")


def normaliser_liste(valeur, separateur):
    if pd.isna(valeur):
        return valeur
    elements = {element.strip() for element in valeur.split(separateur) if element.strip()}
    return separateur.join(sorted(elements))


def harmoniser_organisations(valeur):
    if pd.isna(valeur):
        return valeur
    organisations = [NOMS_DES_LABOS.get(nom.strip(), nom.strip()) for nom in valeur.split(",")]
    return normaliser_liste(",".join(organisations), ",")
