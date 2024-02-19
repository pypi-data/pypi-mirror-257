import requests
import json
import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def check_activation_on_server(activation_code):
    endpoint_url = 'https://mwip8k8av1.execute-api.us-east-1.amazonaws.com/prod/auth'
    headers = {'Content-Type': 'application/json'}  # Adjust headers if needed
    data = {'activation_code': activation_code}  # Sending activation_code

    try:
        response = requests.post(endpoint_url, headers=headers, json=data)
        if response.status_code == 200:
            server_response = response.json()
            # print("Response from endpoint:", server_response)
            return server_response.get('codeExists')
        else:
            print("Failed to fetch endpoint.")
            # print("Status Code:", response.status_code)
            # print("Response:", response.text)
    except requests.RequestException as e:
        print("An error occurred:", e)




# Python: Add this function to your script
def activate_code_on_server(activation_code):
    endpoint_url = 'https://mwip8k8av1.execute-api.us-east-1.amazonaws.com/prod/auth'  # Assuming a separate endpoint for activation
    headers = {'Content-Type': 'application/json'}
    data = {'activation_code': activation_code, 'action': 'activate'}

    try:
        response = requests.post(endpoint_url, headers=headers, json=data)
        if response.status_code == 200:
            server_response = response.json()
            # print("Activation response from endpoint:", server_response)
            return server_response.get('activationStatus')
        else:
            print("Failed to activate code.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
    except requests.RequestException as e:
        print("An error occurred during activation:", e)

def check_if_code_exists_locally():
    activation_file = 'activation_code.txt'
    try:
        with open(activation_file, 'r') as file:
            stored_code = file.read().strip()
            return stored_code
    except FileNotFoundError:
        return None

def save_activation(code):
    with open('activation_code.txt', 'w') as file:
        file.write(code)

def chat(activation_code):
    # Define the API endpoint
    url = 'https://mwip8k8av1.execute-api.us-east-1.amazonaws.com/prod'

    # Initialize conversation history
    conversation_history = []

    while True:
        user_input = input("You: ")

        # Check if the input is the 'clear' command
        if user_input.lower() == 'quit':
            os.system('clear')
            break
        elif user_input.lower() == 'new':
            os.system('clear')
            conversation_history = []
            # print("Starting new conversation:")
            continue

        conversation_history.append({'role': 'user', 'content': user_input})

        # Define the data to be sent in the POST request
        data = {
            'messages': conversation_history,
            'activation_code': activation_code,
        }

        encryptedData = encrypt_data(data)

        # Make the POST request
        response = requests.post(url, json=encryptedData)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()

            response_data = decrypt_data(response_data['encryptedData'])

            assistant_response = response_data['choices'][0]['message']['content']
            print("PalmFrog:", assistant_response)
            conversation_history.append({'role': 'assistant', 'content': response_data.get('text', '')})

        else:
            print("Failed to make the request.")
            print("Status Code:", response.status_code)
            print(response.text)
            print("Exiting chat.")
            break

# Function to encrypt data
def encrypt_data(data):
    key = b'5d0586495fd90503100c96af0bd4a19d'  # Ensure this is 16 bytes (256 bits) for AES-256
    iv = get_random_bytes(16)  # AES block size is 16 bytes
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data_bytes = json.dumps(data).encode('utf-8')

    # PKCS#7 padding
    pad = 16 - len(data_bytes) % 16
    data_bytes += bytes([pad] * pad)

    encrypted_data = cipher.encrypt(data_bytes)
    # Prepend IV for use in decryption, encode the result as base64
    encrypted_data_with_iv = base64.b64encode(iv + encrypted_data).decode('utf-8')
    return encrypted_data_with_iv

def decrypt_data(encrypted_data_with_iv):
    key = b'5d0586495fd90503100c96af0bd4a19d'  # The same key used for encryption, ensure it's correctly formatted
    try:
        # Base64 decode the IV, which is the first 24 characters
        iv = base64.b64decode(encrypted_data_with_iv[:24])
        # The rest is the encrypted data
        encrypted_data = base64.b64decode(encrypted_data_with_iv[24:])
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(encrypted_data)
        
        # Unpad using PKCS7
        pad = padded_data[-1]
        data = padded_data[:-pad]
        
        return json.loads(data)
    except Exception as e:
        print(f"Error during decryption: {e}")
        return None

def welcome():
    print("Palmfrog is ready to chat.")
    print("Type 'quit' to exit the chat or 'new' to start a new conversation.")

def main():
    print("Welcome to Palmfrog!")

    while True:  # Start a loop to keep checking the code
        activation_code = check_if_code_exists_locally()
        if not activation_code:
            # Prompt for a new activation code if not found or incorrect
            print("It looks like you're using Palmfrog the first time. Please activate your license to start chatting.")
            print("You can find your license-code in the email you received after purchasing Palmfrog on https://palmfrog.net")
            activation_code = input("Enter your license-code here: ")
            save_activation(activation_code)
        
        activation_status = check_activation_on_server(activation_code)
        # print("Activation Status:", activation_status)

        if activation_status == 'valid':
            # print("License is valid.")
            welcome()
            chat(activation_code)
            break  # Exit the loop if the code is valid

        # Python: Modify this part of the main function
        elif activation_status == 'not activated':
            user_confirm = input("License not activated. Would you like to activate the license? Type 'yes' or 'no': ")
            if user_confirm.lower() == 'y' or user_confirm.lower() == 'yes':
                activation_result = activate_code_on_server(activation_code)
                if activation_result == 'activated':
                    print("License activated successfully.")
                    welcome()
                    chat(activation_code)
                else:
                    print("Failed to activate license:", activation_result)
            else:
                print("Activation cancelled.")
                activation_code = input("Enter your activation code: ")
                save_activation(activation_code)

        elif activation_status == 'expired':
            print(f"License is expired. Please buy a new license to continue using Palmfrog on https://palmfrog.net.")
            activation_code = input("Enter new license-code: ")
            save_activation(activation_code)
            # Don't break here because we want to loop back and check the new code

        elif activation_status == 'code not found':
            print(f"License-code does not exist. Please enter a valid license-code.")
            activation_code = input("Enter your license-code: ")
            save_activation(activation_code)
            # Don't break here because we want to loop back and check the new code

# Ensures that main() is only called when the script is executed directly (not imported)
if __name__ == '__main__':
    main()