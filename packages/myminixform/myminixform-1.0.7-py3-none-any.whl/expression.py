import re
from humre import *

def regex(regex_name):
    regex_dict = {
        "EMAIL": (
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "Cette expression valide si une chaîne représente une adresse email valide."
        ),
        "NAME": (
            r"^([a-zA-Z]{1,}(['])?[a-zA-Z]+)([ ][a-zA-Z]{1,}(['])?[a-zA-Z]+)+$",
            "Nom et prenoms"
        ),
        "NAME_MAJ": (
            r"^([A-Z]{1,}(['])?[A-Z]+)([ ][A-Z]{1,}(['])?[A-Z]+)+$",
            "Nom et prenoms en majuscule"
        ),
        "NAME_MIN": (
            r"^([a-z]{1,}(['])?[a-z]+)([ ][a-z]{1,}(['])?[a-z]+)+$",
            "Nom et prenoms en majuscule"
        ),
        "PHONE_NUMBERS": (
            r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "Capture les numéros de téléphone dans divers formats."
        ),
        "PHONE_US": (
            r"^\(\d{3}\)\d{3}-\d{4}$",
            "Valide un numéro de téléphone au format (123) 456-7890."
        ),
        "PHONE_CI": (
            r"^(1|05|07)((?:[-]\d{2}){4}|(?:[ ]\d{2}){4}|\d{8})$",
            "Valide un numéro de téléphone au format 0745678900 ou 07 45 67 89 00 ou 07-45-67-89-00 respectant les 10 chiffres du numéro de téléphone ivoirien."
        ),
        "IPV4": (
            r"^\b(?:\d{1,3}\.){3}\d{1,3}\b$",
            "Valide une adresse IP IPv4."
        ),
        "ZIP_US": (
            r"\b\d{5}(?:-\d{4})?\b",
            "Extrayez les codes postaux américains, optionnellement suivis par un code postal étendu."
        ),
        "ALPHANUMERIC": (
            r"^[a-zA-Z0-9]+$",
            "Valide si une chaîne ne contient que des lettres majuscules et minuscules ainsi que des chiffres."
        ),
        "HTML_TAGS": (
            r"<[^>]+>",
            "Capture toutes les balises HTML dans une chaîne."
        ),
        "DATE_YYYY_MM_DD": (
            r"^\d{4}-\d{2}-\d{2}$",
            "Valide une date au format YYYY-MM-DD."
        ),
        "URL_SIMPLE": (
            r"^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$",
            "Valide une URL simple commençant par 'http', 'https' ou 'ftp'."
        ),
        "HASHTAGS": (
            r"#\w+",
            "Capture tous les hashtags dans une chaîne."
        ),
        "POSTAL_CODE_CA": (
            r"^[ABCEGHJKLMNPRSTVXY]\d[A-Z]\d[A-Z]\d$",
            "Valide un code postal canadien."
        ),
        "EMAIL_ADDRESSES": (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "Capture toutes les adresses email dans une chaîne."
        ),
        "CREDIT_CARD_SIMPLE": (
            r"^\d{4}-\d{4}-\d{4}-\d{4}$",
            "Valide un numéro de carte de crédit au format 0000-0000-0000-0000."
        ),
        "TIME_HH_MM": (
            r"([01]\d|2[0-3]):([0-5]\d)",
            "Capture les heures au format HH:MM."
        ),
        "STRONG_PASSWORD": (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            "Valide un mot de passe fort avec au moins une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial."
        ),
        "TWITTER_MENTIONS": (
            r"@(\w+)",
            "Capture toutes les mentions Twitter dans une chaîne."
        ),
        "MAC_ADDRESS": (
            r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
            "Valide une adresse MAC au format standard."
        ),
        "QUOTED_STRINGS": (
            r'"(.*?)"',
            "Capture le contenu entre guillemets."
        ),
        "SSN_US": (
            r"^\d{3}-\d{2}-\d{4}$",
            "Valide un numéro de sécurité sociale américain au format 123-45-6789."
        ),
        "HTML_LINKS": (
            r'href=["\'](https?:\/\/[^"\']+)["\']',
            "Capture les URL des liens dans du code HTML."
        ),
    }

    return regex_dict.get(regex_name, None)


def eval_contrainte(expression):
    if expression.startswith("py::"):
        val= expression[len("py::"):]
        print(val)
        regx=eval(f'{val}')
        print(regx)
    elif expression.startswith("mxf::"):
        val=expression[len("mxf::"):]
        regx=eval(f'regex("{val}")[0]')
    else:
        regx=expression
    return f'regex(.,"{regx}")'
