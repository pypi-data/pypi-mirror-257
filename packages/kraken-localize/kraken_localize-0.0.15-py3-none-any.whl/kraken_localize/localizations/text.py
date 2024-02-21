
import copy
from os.path import exists
from kraken_localize.helpers import json
from kraken_localize.helpers import things
import os

import uuid
import copy
import functools
import datetime

FILENAME = 'kraken_localize/data/terms.json'
records = json.load(FILENAME)
records = records if records else []


@functools.lru_cache(maxsize=128)
def get_term(code, number='s', language='en_us'):
    """Return localization
    number: ['s', 'p']    singular or plural
    """

    code = code.lower()
    
    singular = {
        "@type": "definedTermSet",
        "@id": 'singular',
        "name": 'singular',
        "hasDefinedTerm": []
    }
    plural = {
        "@type": "definedTermSet",
        "@id": 'plural',
        "name": 'plural',
        "hasDefinedTerm": []
    }



    definedTermSets = [x for x in records if x.get('name', None)==language]
    definedTermSet = definedTermSets[0] if definedTermSets else None

    if not definedTermSet:
        return code

    termCodes = definedTermSet.get('hasDefinedTerm',[])

    # Filter for number
    if number == 's':
        termCodes = [x for x in termCodes if singular in x.get('inDefinedTermSet', None)]
    if number == 'p':
        termCodes = [x for x in termCodes if plural in x.get('inDefinedTermSet', None)]

    # Find and return
    for i in termCodes:
        if i.get('termCode', None) == code:
            result = i.get('name', None)
            if result:
                return result

    #print('Not found')
    return code





def new_entry(id, language, value_singular, value_plural):
    """
    """

    id = id.lower()
    
    template_definedTermSet = {
        "@type": "definedTermSet",
        "@id": language,
        "name": language,
        "hasDefinedTerm": []
    }

    singular = {
        "@type": "definedTermSet",
        "@id": 'singular',
        "name": 'singular',
        "hasDefinedTerm": []
    }
    plural = {
        "@type": "definedTermSet",
        "@id": 'plural',
        "name": 'plural',
        "hasDefinedTerm": []
    }


    definedTermSets = [x for x in records if x.get('name', None)==language]
    definedTermSet = definedTermSets[0] if definedTermSets else None

    if not definedTermSet:
        definedTermSet = copy.deepcopy(template_definedTermSet)
        records.append(definedTermSet)    


    # Remove from record if already exists
    dupes = [x for x in definedTermSet.get('hasDefinedTerm', []) if x.get('termCode', None)==id]
    if dupes:
        for i in dupes:
            definedTermSet.get('hasDefinedTerm', []).remove(i)
        

    record = {
        "@type": "definedTerm",
        "@id": str(uuid.uuid4()),
        "termCode": id,
        "name": value_singular,
        'inDefinedTermSet': [
            copy.deepcopy(template_definedTermSet), copy.deepcopy(singular)
        ]
    }

    definedTermSet['hasDefinedTerm'].append(record)

    record = {
        "@type": "definedTerm",
        "@id": str(uuid.uuid4()),
        "termCode": id,
        "name": value_plural,
        'inDefinedTermSet': [
            copy.deepcopy(template_definedTermSet), copy.deepcopy(plural)
        ]
    }

    definedTermSet['hasDefinedTerm'].append(record)

    json.dump(FILENAME, records)





def _init():
    """Populates with 
    """

    if records:
        return
    
    # French canada common terms

    locale = 'fr_CA'
    new_entry('About us', locale,'À propos de nous',None)
    new_entry('Accessories', locale,'Accessoires',None)
    new_entry('All rights reserved', locale,'Tous droits réservés',None)
    new_entry('Apply for a job here', locale,'Postulez à une offre ici',None)
    new_entry('Back', locale,'Précédent',None)
    new_entry('Back to top of page', locale,'Haut de page',None)
    new_entry('Basket', locale,'Panier',None)
    new_entry('Billing address', locale,'Adresse de facturation',None)
    new_entry('Billing name', locale,'Nom de facturation',None)
    new_entry('Board of Directors', locale,"Conseil d'administration",None)
    new_entry('Calls may be recorded', locale,'Les appels peuvent être enregistrés',None)
    new_entry('Cancel', locale,'Annuler',None)
    new_entry('Card number', locale,'Numéro de carte',None)
    new_entry('Careers', locale,'Recrutement',None)
    new_entry('Case studies', locale,'Études de cas',None)
    new_entry('Checkout', locale,'Commander',None)
    new_entry('Click here', locale,'Cliquez ici',None)
    new_entry('Close', locale,'Fermer',None)
    new_entry('Comments', locale,'Commentaires',None)
    new_entry('Contact', locale,'Contact',None)
    new_entry('Cookie policy', locale,'Politique de cookies',None)
    new_entry('Copyright', locale,"Protégé par droits d'auteur",None)
    new_entry('Create account', locale,'Créer un compte',None)
    new_entry('Customer service', locale,'Service client',None)
    new_entry('Delivery address', locale,'Adresse de livraison',None)
    new_entry('Disclaimer', locale,'Avis de non-responsabilité',None)
    new_entry('Download', locale,'Télécharger',None)
    new_entry('Email', locale,'Courriel',None)
    new_entry('Employees', locale,'Employés',None)
    new_entry('Events', locale,'Événements',None)
    new_entry('Expiry date', locale,"Date d'expiration",None)
    new_entry('FAQs', locale,'FAQ',None)
    new_entry('Financial reports', locale,'Rapports financiers',None)
    new_entry('Find out more', locale,'En savoir plus',None)
    new_entry('First name', locale,'Prénom',None)
    new_entry('Follow us', locale,'Suivez-nous',None)
    new_entry('From date', locale,'À partir du',None)
    new_entry('Full name', locale,'Nom entier',None)
    new_entry('Further information', locale,'Informations supplémentaires',None)
    new_entry('Gift cards', locale,'Cartes cadeaux',None)
    new_entry('Go', locale,'Valider',None)
    new_entry('Help', locale,'Aide',None)
    new_entry('Home', locale,'Accueil',None)
    new_entry('Join', locale,"S'abonner",None)
    new_entry('Last name', locale,'Nom',None)
    new_entry('Learn more', locale,'En savoir plus',None)
    new_entry('Locations', locale,'Localisation',None)
    new_entry('Log in', locale,'Connexion',None)
    new_entry('Log in to my account', locale,'Connexion à mon compte',None)
    new_entry('Management', locale,'Gestion',None)
    new_entry('New arrivals', locale,'Nouveaux arrivages',None)
    new_entry('News', locale,'Actualités',None)
    new_entry('Next', locale,'Suivant',None)
    new_entry('Office locations', locale,'Sites',None)
    new_entry('Order status', locale,'Statut de la commande',None)
    new_entry('Our certification', locale,'Notre certification',None)
    new_entry('Partners', locale,'Partenaires',None)
    new_entry('Password', locale,'Mot de passe',None)
    new_entry('Payment', locale,'Paiement',None)
    new_entry('Phone', locale,'Téléphone',None)
    new_entry('Press', locale,'Presse',None)
    new_entry('Press releases', locale,'Communiqués de presse',None)
    new_entry('Privacy policy', locale,'Politique de confidentialité',None)
    new_entry('Privacy statement', locale,'Déclaration de confidentialité',None)
    new_entry('Products and services', locale,'Produits et services',None)
    new_entry('Promotion', locale,'Promotion',None)
    new_entry('Promotional offers', locale,'Offres promotionnelles',None)
    new_entry('References', locale,'Références',None)
    new_entry('Register', locale,"S'inscrire",None)
    new_entry('Request a call', locale,'Demander à être rappelé',None)
    new_entry('Request a quote', locale,'Demandez un devis',None)
    new_entry('Request a…', locale,'Demandez un(e)…',None)
    new_entry('Reviews', locale,'Commentaires',None)
    new_entry('Sales', locale,'Ventes',None)
    new_entry('Search', locale,'Recherche',None)
    new_entry('Secure payment', locale,'Paiement sécurisé',None)
    new_entry('Security number', locale,'Cryptogramme',None)
    new_entry('Security policy', locale,'Politique de sécurité',None)
    new_entry('Select', locale,'Sélectionner',None)
    new_entry('Select address', locale,"Sélectionner l'adresse",None)
    new_entry('Select country', locale,'Sélectionner un pays',None)
    new_entry('Shipping and returns policy', locale,'Conditions générales de livraison et de retour',None)
    new_entry('Sign in', locale,"S'identifier",None)
    new_entry('Sign up', locale,'Inscription',None)
    new_entry('Site disclaimer', locale,'Avis de non-responsabilité du site',None)
    new_entry('Site map', locale,'Plan du site',None)
    new_entry('Special offers', locale,'Offres spéciales',None)
    new_entry('Store locator', locale,'Trouver un magasin',None)
    new_entry('Stores', locale,'Magasins',None)
    new_entry('Submit', locale,'Envoyer',None)
    new_entry('Subscribe to newsletter', locale,"S'abonner à la lettre d'informations", None)
    new_entry('Support', locale,'Support',None)
    new_entry('Terms and conditions', locale,'Conditions générales',None)
    new_entry('Track order', locale,'Suivi de commande',None)
    new_entry('Unsubscribe', locale,'Se désabonner',None)
    new_entry('Username', locale,"Nom d'utilisateur",None)


    # English canada common terms
    locale = 'en_CA'
    new_entry('About us', locale,'About us',None)
    new_entry('Accessories', locale,'Accessories',None)
    new_entry('All rights reserved', locale,'All rights reserved',None)
    new_entry('Apply for a job here', locale,'Apply for a job here',None)
    new_entry('Back', locale,'Back',None)
    new_entry('Back to top of page', locale,'Back to top of page',None)
    new_entry('Basket', locale,'Basket',None)
    new_entry('Billing address', locale,'Billing address',None)
    new_entry('Billing name', locale,'Billing name',None)
    new_entry('Board of Directors', locale,'Board of Directors',None)
    new_entry('Calls may be recorded', locale,'Calls may be recorded',None)
    new_entry('Cancel', locale,'Cancel',None)
    new_entry('Card number', locale,'Card number',None)
    new_entry('Careers', locale,'Careers',None)
    new_entry('Case studies', locale,'Case studies',None)
    new_entry('Checkout', locale,'Checkout',None)
    new_entry('Click here', locale,'Click here',None)
    new_entry('Close', locale,'Close',None)
    new_entry('Comments', locale,'Comments',None)
    new_entry('Contact', locale,'Contact',None)
    new_entry('Cookie policy', locale,'Cookie policy',None)
    new_entry('Copyright', locale,'Copyright',None)
    new_entry('Create account', locale,'Create account',None)
    new_entry('Customer service', locale,'Customer service',None)
    new_entry('Delivery address', locale,'Delivery address',None)
    new_entry('Disclaimer', locale,'Disclaimer',None)
    new_entry('Download', locale,'Download',None)
    new_entry('Email', locale,'Email',None)
    new_entry('Employees', locale,'Employees',None)
    new_entry('Events', locale,'Events',None)
    new_entry('Expiry date', locale,'Expiry date',None)
    new_entry('FAQs', locale,'FAQs',None)
    new_entry('Financial reports', locale,'Financial reports',None)
    new_entry('Find out more', locale,'Find out more',None)
    new_entry('First name', locale,'First name',None)
    new_entry('Follow us', locale,'Follow us',None)
    new_entry('From date', locale,'From date',None)
    new_entry('Full name', locale,'Full name',None)
    new_entry('Further information', locale,'Further information',None)
    new_entry('Gift cards', locale,'Gift cards',None)
    new_entry('Go', locale,'Go',None)
    new_entry('Help', locale,'Help',None)
    new_entry('Home', locale,'Home',None)
    new_entry('Join', locale,'Join',None)
    new_entry('Last name', locale,'Last name',None)
    new_entry('Learn more', locale,'Learn more',None)
    new_entry('Locations', locale,'Locations',None)
    new_entry('Log in', locale,'Log in',None)
    new_entry('Log in to my account', locale,'Log in to my account',None)
    new_entry('Management', locale,'Management',None)
    new_entry('New arrivals', locale,'New arrivals',None)
    new_entry('News', locale,'News',None)
    new_entry('Next', locale,'Next',None)
    new_entry('Office locations', locale,'Office locations',None)
    new_entry('Order status', locale,'Order status',None)
    new_entry('Our certification', locale,'Our certification',None)
    new_entry('Partners', locale,'Partners',None)
    new_entry('Password', locale,'Password',None)
    new_entry('Payment', locale,'Payment',None)
    new_entry('Phone', locale,'Phone',None)
    new_entry('Press', locale,'Press',None)
    new_entry('Press releases', locale,'Press releases',None)
    new_entry('Privacy policy', locale,'Privacy policy',None)
    new_entry('Privacy statement', locale,'Privacy statement',None)
    new_entry('Products and services', locale,'Products and services',None)
    new_entry('Promotion', locale,'Promotion',None)
    new_entry('Promotional offers', locale,'Promotional offers',None)
    new_entry('References', locale,'References',None)
    new_entry('Register', locale,'Register',None)
    new_entry('Request a call', locale,'Request a call',None)
    new_entry('Request a quote', locale,'Request a quote',None)
    new_entry('Request a…', locale,'Request a…',None)
    new_entry('Reviews', locale,'Reviews',None)
    new_entry('Sales', locale,'Sales',None)
    new_entry('Search', locale,'Search',None)
    new_entry('Secure payment', locale,'Secure payment',None)
    new_entry('Security number', locale,'Security number',None)
    new_entry('Security policy', locale,'Security policy',None)
    new_entry('Select', locale,'Select',None)
    new_entry('Select address', locale,'Select address',None)
    new_entry('Select country', locale,'Select country',None)
    new_entry('Shipping and returns policy', locale,'Shipping and returns policy',None)
    new_entry('Sign in', locale,'Sign in',None)
    new_entry('Sign up', locale,'Sign up',None)
    new_entry('Site disclaimer', locale,'Site disclaimer',None)
    new_entry('Site map', locale,'Site map',None)
    new_entry('Special offers', locale,'Special offers',None)
    new_entry('Store locator', locale,'Store locator',None)
    new_entry('Stores', locale,'Stores',None)
    new_entry('Submit', locale,'Submit',None)
    new_entry('Subscribe to newsletter', locale,'Subscribe to newsletter',None)
    new_entry('Support', locale,'Support',None)
    new_entry('Terms and conditions', locale,'Terms and conditions',None)
    new_entry('Track order', locale,'Track order',None)
    new_entry('Unsubscribe', locale,'Unsubscribe',None)
    new_entry('Username', locale,'Username',None)

    # order
    new_entry('orderItemNumber', locale, '#', None)
    new_entry('orderedItem', locale, 'Product', None)
    new_entry('orderQuantity', locale, 'Quantity', None)
    new_entry('price', locale, 'Price', None)

    new_entry('OrderCancelled', locale, 'Cancelled', None)
    new_entry('OrderDelivered', locale, 'Delivered', None)
    new_entry('OrderInTransit', locale, 'In transit', None)
    new_entry('OrderPaymentDue', locale, 'Payment due', None)
    new_entry('OrderPickupAvailable', locale, 'Pickup available', None)
    new_entry('OrderProblem', locale, 'Problem', None)
    new_entry('OrderProcessing', locale, 'Processing', None)
    new_entry('OrderReturned', locale, 'Returned', None)

    # Schema.org terms en_US
    locale = 'en_US'
    new_entry('givenName', locale,'First name', None)
    new_entry('familyName', locale,'Last name', None)
    new_entry('telephone', locale,'phone', None)
    new_entry('email', locale,'email', None)
    new_entry('organization', locale,'Company', None)
    new_entry('person', locale,'Contact', None)
    new_entry('order', locale,'order', None)
    new_entry('product', locale,'product', None)
    
    new_entry('postalAddress', locale,'Adress', None)
    new_entry('streetAddress', locale,'street', None)
    new_entry('addressLocality', locale,'city', None)
    new_entry('addressRegion', locale,'state', None)
    new_entry('addressCountry', locale,'country', None)
    new_entry('postalCode', locale,'Zip code', None)

    # action
    new_entry('actionStatus', locale, 'Status', None)
    new_entry('startTime', locale, 'Start', None)
    new_entry('endTime', locale, 'Finish', None)
    new_entry('agent', locale, 'Owner', None)
    new_entry('ActiveActionStatus', locale, 'In progress', None)
    new_entry('CompletedActionStatus', locale, 'Completed', None)
    new_entry('FailedActionStatus', locale, 'Failed', None)
    new_entry('PotentialActionStatus', locale, 'New', None)

    # order
    new_entry('orderItemNumber', locale, '#', None)
    new_entry('orderedItem', locale, 'Product', None)
    new_entry('orderQuantity', locale, 'Quantity', None)
    new_entry('price', locale, 'Price', None)

    new_entry('OrderCancelled', locale, 'Cancelled', None)
    new_entry('OrderDelivered', locale, 'Delivered', None)
    new_entry('OrderInTransit', locale, 'In transit', None)
    new_entry('OrderPaymentDue', locale, 'Payment due', None)
    new_entry('OrderPickupAvailable', locale, 'Pickup available', None)
    new_entry('OrderProblem', locale, 'Problem', None)
    new_entry('OrderProcessing', locale, 'Processing', None)
    new_entry('OrderReturned', locale, 'Returned', None)

    # Schema.org terms en_CA
    locale = 'en_CA'
    new_entry('givenName', locale,'First name', None)
    new_entry('familyName', locale,'Last name', None)
    new_entry('telephone', locale,'phone', None)
    new_entry('email', locale,'email', None)
    new_entry('organization', locale,'Company', None)
    new_entry('person', locale,'Contact', None)
    new_entry('order', locale,'order', None)
    new_entry('product', locale,'product', None)
    
    new_entry('postalAddress', locale,'Adress', None)
    new_entry('streetAddress', locale,'street', None)
    new_entry('addressLocality', locale,'city', None)
    new_entry('addressRegion', locale,'province', None)
    new_entry('addressCountry', locale,'country', None)
    new_entry('postalCode', locale,'Postal code', None)

    # action
    new_entry('actionStatus', locale, 'Status', None)
    new_entry('startTime', locale, 'Start', None)
    new_entry('endTime', locale, 'Finish', None)
    new_entry('agent', locale, 'Owner', None)
    new_entry('ActiveActionStatus', locale, 'In progress', None)
    new_entry('CompletedActionStatus', locale, 'Completed', None)
    new_entry('FailedActionStatus', locale, 'Failed', None)
    new_entry('PotentialActionStatus', locale, 'New', None)



    # Schema.org terms fr_CA
    locale='fr_CA'
    new_entry('givenName', locale,'Prénom', None)
    new_entry('familyName', locale,'Nom', None)
    new_entry('telephone', locale,'Téléphone', None)
    new_entry('email', locale,'courriel', None)
    new_entry('organization', locale,'Entreprise', None)
    new_entry('person', locale,'Contact', None)
    new_entry('order', locale,'Commande', None)
    new_entry('product', locale,'Produit', None)
    
    # address
    new_entry('postalAddress', locale,'Adresse', None)
    new_entry('streetAddress', locale,'rue', None)
    new_entry('addressLocality', locale,'Ville', None)
    new_entry('addressRegion', locale,'province', None)
    new_entry('addressCountry', locale,'pays', None)
    new_entry('postalCode', locale,'Code postal', None)

    # action
    new_entry('actionStatus', locale, 'Statut', None)
    new_entry('startTime', locale, 'Début', None)
    new_entry('endTime', locale, 'Fin', None)
    new_entry('agent', locale, 'Responsable', None)
    new_entry('ActiveActionStatus', locale, 'En cours', None)
    new_entry('CompletedActionStatus', locale, 'Complété', None)
    new_entry('FailedActionStatus', locale, 'Échec', None)
    new_entry('PotentialActionStatus', locale, 'Nouveau', None)

    # order
    new_entry('orderItemNumber', locale, '#', None)
    new_entry('orderedItem', locale, 'Produit', None)
    new_entry('orderQuantity', locale, 'Quantity', None)
    new_entry('price', locale, 'Prix', None)

    new_entry('OrderCancelled', locale, 'Annulé', None)
    new_entry('OrderDelivered', locale, 'Livré', None)
    new_entry('OrderInTransit', locale, 'En route', None)
    new_entry('OrderPaymentDue', locale, 'Paiement requis', None)
    new_entry('OrderPickupAvailable', locale, 'Ramassage disponible', None)
    new_entry('OrderProblem', locale, 'Problème', None)
    new_entry('OrderProcessing', locale, 'En traitement', None)
    new_entry('OrderReturned', locale, 'Retourné', None)

_init()




