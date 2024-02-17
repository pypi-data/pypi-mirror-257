const allTranslations = {
    'fr': {
        ":": " :",
        "Connection to web server closed": "Connexion au serveur interrompue",
        "Unauthorized": "Non autorisé",
        "Celery is not working": "Celery ne fonctionne pas",
        "Try to reconnect": "Essayer de se reconnecter",
    },
    'ru': {
        ":": ":",
        "Connection to web server closed": "Соединение с веб-сервером закрыто",
        "Unauthorized": "Несанкционированный",
        "Celery is not working": "Celery не работает",
        "Try to reconnect": "Попробуйте переподключиться",
    },
}

const lang = document.documentElement.lang
const translations = allTranslations[lang]

export function gettext(msg, ...args) {
    msg = translations[msg] ?? msg
    if (args.length > 0) {
        msg = msg.format(...args)
    }
    return msg
}
