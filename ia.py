import erppeek
import requests
import openai
import base64

# Configuration des paramètres Odoo
odoo_url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

# Connexion à Odoo en utilisant erppeek
odoo_client = erppeek.Client(odoo_url, db, username, password)

# Configurez votre clé API OpenAI. Remplacez 'VOTRE_CLE_API' par votre clé réelle.
openai.api_key = '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'

# Recherche de l'enregistrement 'product.template' avec le nom 'Table'
product_tmpl_ids = odoo_client.model('product.template').search([('name', '=', 'Table')])

if product_tmpl_ids:
    # Sélection du premier enregistrement trouvé (supposons qu'il y ait au moins un enregistrement)
    record_product = odoo_client.model('product.template').browse(product_tmpl_ids[0])

    # Accès au champ 'image_1920' de l'enregistrement
    image_data = record_product.image_1920

    # Conversion des données de l'image en base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # Utilisation de l'API OpenAI avec les données de l'image
    response = openai.Image.create(
        content=image_base64,
        model="clip-image-v1",
        n=1,
        size="256x256"
    )

    # Récupération de la description générée par l'API
    description_ai = response['data'][0]['text']

    # Mise à jour du champ 'description' de l'enregistrement dans Odoo
    record_product.write({'description': description_ai})

    print(f"Description mise à jour pour l'enregistrement 'product.template' avec ID {product_tmpl_ids[0]}")
else:
    print("Aucun enregistrement 'product.template' trouvé avec le nom 'Table'")

#product_tmpl = client.model('product.template').search([('name', '=', 'Table')])
#record_product = client.model('product.template').browse(product_tmpl)
#record_product.image_1920

#record_product.write({'description': description_ai})