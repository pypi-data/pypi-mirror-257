import requests
from .customresponse import CustomResponse

def Shopify_get_metaobject_gid(shop="", access_token="", api_version="2024-01", metaobject_type="", handle=""):

    # print(f"Access token: {access_token}")

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # print(f"headers: {headers}")

    query = """
    query GetMetaobjectByHandle($type: String!, $handle: String!) {
      metaobjectByHandle(handle: {
            type: $type,
            handle: $handle
        }) {
            id
            type
            handle
        }
    }
    """
    
    variables = {
        "type": metaobject_type,
        "handle": handle
    }
    
    payload = {
        'query': query,
        'variables': variables
    }

    # print(f"payload: {payload}")
    
    response = requests.post(url, json=payload, headers=headers)
    # response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        result_id = response_json['data']['metaobjectByHandle']['id']
        return result_id
    else:
        print(f"Error: {response.status_code}")
        return None

def Shopify_update_metaobject(shop="", access_token="", api_version="2024-01", metaobject_gid="", banner_url="", mobile_banner_url="", product_url="", metaobject_banner_number=1):
    # Push to shopify banner object for vinzo
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/graphql.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Generate field names based on metaobject_banner_number
    field_names = [f"product_link_{metaobject_banner_number}",
                   f"banner_url_{metaobject_banner_number}",
                   f"mobile_banner_url_{metaobject_banner_number}"
    ]

    print(field_names)

    mutation = """
    mutation UpdateMetaobject($id: ID!, $metaobject: MetaobjectUpdateInput!) {
    metaobjectUpdate(id: $id, metaobject: $metaobject) {
        metaobject {
        handle
        """
    
    # Add dynamic field names to the mutation
    for field_name in field_names:
        mutation += f"{field_name}: field(key: \"{field_name}\") {{ value }}\n"

    mutation += """
        }
        userErrors {
        field
        message
        code
        }
    }
    }
    """

    variables = { 
        "id": metaobject_gid,
        "metaobject": {
            "fields": [
                {"key": field_name, "value": value}
                for field_name, value in zip(field_names, [product_url, banner_url, mobile_banner_url])
            ]
        } 
    }

    response = requests.post(url, json={'query': mutation, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error loading to shopify: {response.status_code}")
        return (f"Error loading to shopify: {response.status_code}")

def Shopify_get_products(shop="", access_token="", api_version="2024-01"):

    '''Uses Admin API'''

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/products.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve products: {response.status_code}")
        return None
    
def Shopify_get_collections(shop="", access_token="", api_version="2024-01"):

    url_custom = f"https://{shop}.myshopify.com/admin/api/{api_version}/custom_collections.json"
    url_smart = f"https://{shop}.myshopify.com/admin/api/{api_version}/smart_collections.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url_smart, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve smart collections: {response.status_code}")
        print(f"response {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    smart_collections = response.json()['smart_collections']
    
    response = requests.get(url_custom, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve custom collections: {response.status_code}")
        print(f"response {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    custom_collections = response.json()['custom_collections']
    
    all_collections = smart_collections + custom_collections

    return CustomResponse(data=all_collections, status_code=200)

def Shopify_get_collection_metadata(shop="", access_token="", api_version="2024-01", collection_id=""):
    '''Returns metafields and metadata'''
    metadata_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}.json"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(metadata_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve metadata for collection ID {collection_id}. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return CustomResponse(data=response.text, status_code=400)
    
    collection_metadata = response.json()['collection']
    
    # Retrieve metafields for the collection
    metafields_url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}/metafields.json"
    response = requests.get(metafields_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve metafields for collection ID {collection_id}. Status code: {response.status_code}")
        print(f"Metafields response: {response.text}")
        return CustomResponse(data=response.text, status_code=400)
    metafields_data = response.json()['metafields']

    # Join metadata and metafield 
    collection_metadata['metafields'] = metafields_data

    # print(f"collection_metadata: {collection_metadata}")

    return CustomResponse(data=collection_metadata, status_code=200)

def Shopify_get_products_in_collection(shop="", access_token="", api_version="2024-01", collection_id=""):

    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/collections/{collection_id}/products.json"
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        products=response.json()['products']
        return CustomResponse(data=products, status_code=200)

    else:
        print(f"Failed to retrieve products in collection {collection_id}: {response.status_code}")
        return CustomResponse(data=response.text, status_code=400)
    
def Shopify_get_product_variants(shop="", access_token="", api_version="2024-01", product_id=""):
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/products/{product_id}/variants.json"
    print(url)
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        variants=response.json()['variants']
        return CustomResponse(data=variants, status_code=200)
    else:
        print(f"Failed to retrieve product variants for product {product_id}: {response.status_code}")
        return CustomResponse(data=response.text, status_code=400)

def Shopify_get_customers(shop="", access_token="", api_version="2024-01"):
    # Endpoint URL for fetching customers
    url = f"https://{shop}.myshopify.com/admin/api/{api_version}/customers.json"
    
    # Headers for the request, including the required access token for authentication
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': access_token
    }

    # Making the GET request to the API
    response = requests.get(url, headers=headers)
    
    # Check the response status code
    if response.status_code != 200:
        # If the request was not successful, print an error message and return a custom response
        print(f"Failed to retrieve customers: {response.status_code}")
        print(f"response: {response.text}")
        return CustomResponse(data=response.text, status_code=response.status_code)
    
    # If the request was successful, parse the JSON response to get the customers
    customers = response.json()['customers']
    
    # Return a custom response containing the customers and a successful status code
    return CustomResponse(data=customers, status_code=200)

def Shopify_get_marketing_customer_list(shop="", access_token="", api_version="2024-01"):
    ''' Returns a dictionary with 2 lists, customer who are subscribe to email marketing and cutomers subscribed to SMS marketing'''
    # Assume Shopify_get_customers is defined elsewhere and correctly returns customer data
    response = Shopify_get_customers(shop, access_token, api_version)
    
    # Initialize dictionaries to hold subscribers
    marketing_lists = {
        'newsletter_subscribers': [],
        'sms_marketing_subscribers': []
    }
    
    # Proceed only if the response was successful
    if response.status_code != 200:
        print("Failed to retrieve customers. Status Code:", response.status_code)
        return response

    # Iterate through the customer data
    for customer in response.data:
        email_marketing_consent = customer.get('email_marketing_consent')
        if email_marketing_consent and email_marketing_consent.get('state') == 'subscribed':
            marketing_lists['newsletter_subscribers'].append({
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'email': customer.get('email', '')
            })
        
        sms_marketing_consent = customer.get('sms_marketing_consent')
        # Adjusted to check if sms_marketing_consent is not None and then proceed
        if sms_marketing_consent and sms_marketing_consent.get('state') == 'subscribed':
            marketing_lists['sms_marketing_subscribers'].append({
                'first_name': customer.get('first_name', ''),
                'last_name': customer.get('last_name', ''),
                'email': customer.get('email', '')  # Assuming you want the email for SMS subscribers
            })
    
    return CustomResponse(data=marketing_lists, status_code=200)