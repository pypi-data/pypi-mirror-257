import requests
import json
import os
import base64
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from colorama import Fore, Back, Style

# Initialize Colorama (needed for Windows)
from colorama import init
init()

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
    url = 'https://mwip8k8av1.execute-api.us-east-1.amazonaws.com/prod'

    # Initialize conversation history
    conversation_history = []

    while True:
        buffer = []  # Accumulate input lines here
        try:
            print("You: ", end="", flush=True)  # Optional: Print a prompt for each new line of input

            # Read multiline input from user
            text = sys.stdin.read()

            # Check if the text is a command
            if text.strip().lower() == '/quit':
                print("Exiting chat.")
                # Clear the terminal before exiting
                if os.name == 'nt':  # For Windows
                    os.system('cls')
                else:  # For macOS and Linux
                    os.system('clear')
                break
            elif text.strip().lower() == '/new':
                # Clear the terminal before exiting
                if os.name == 'nt':  # For Windows
                    os.system('cls')
                else:  # For macOS and Linux
                    os.system('clear')
                
                print("Starting new conversation:")
                conversation_history = []
                continue

            # Process the standard chat operation
            conversation_history.append({'role': 'user', 'content': text})

            # Define the data to be sent in the POST request
            data = {
                'messages': conversation_history,
                'activation_code': activation_code,
            }

            encryptedData = encrypt_data(data)
            print("Palmfrog is thinking...")

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

        except EOFError:
            # This exception will be raised after the EOF character is detected, so the loop can end.
            print("\nDetected EOF: Ending the text input. If this is an error, start the session again.")
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
    print("")
    print("Type '/quit' to exit the chat or '/new' to start a new conversation.")
    print(Fore.RED)
    print("Multiline-Mode is active: Pressing ENTER does not submit your message but creates a new line for your input. ")
    print("Press ENTER and then CTRL+D (Mac/Linux) or CTRL+Z (Windows) on an empty new line to submit your message!")
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def main():
    print(Fore.GREEN)
    print("Welcome to Palmfrog!")
    print(Fore.RESET)

    while True:  # Start a loop to keep checking the code
        activation_code = check_if_code_exists_locally()
        if not activation_code:
            # Prompt for a new activation code if not found or incorrect
            print("It looks like you're using Palmfrog the first time. Please activate your license to start chatting.")
            print("You can find your license-code in the email you received after purchasing Palmfrog on https://palmfrog.net")
            print("")
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
            print(Fore.YELLOW)
            user_confirm = input("License not activated. Would you like to activate the license for 24 hours starting now?" + Fore.RESET + " Type 'yes' or 'no': ")
            if user_confirm.lower() == 'y' or user_confirm.lower() == 'yes':
                activation_result = activate_code_on_server(activation_code)
                if activation_result == 'activated':
                    print(Fore.GREEN)
                    print("License activated successfully.")
                    print(Fore.RESET)
                    welcome()
                    chat(activation_code)
                else:
                    print(Fore.RED)
                    print("Failed to activate license:", activation_result)
                    print(Fore.RESET)
            else:
                print(Fore.RED)
                print("Activation cancelled.")
                print(Fore.RESET)
                activation_code = input("Enter your activation code: ")
                save_activation(activation_code)

        elif activation_status == 'expired':
            print(Fore.RED)
            print(f"License is expired. Please buy a new license to continue using Palmfrog on https://palmfrog.net.")
            print(Fore.RESET)
            activation_code = input("Enter new license-code: ")
            save_activation(activation_code)
            # Don't break here because we want to loop back and check the new code

        elif activation_status == 'code not found':
            print(Fore.RED)
            print(f"License-code does not exist. Please enter a valid license-code.")
            print(Fore.RESET)
            print("")
            activation_code = input("Enter your license-code: ")
            save_activation(activation_code)
            # Don't break here because we want to loop back and check the new code

# Ensures that main() is only called when the script is executed directly (not imported)
if __name__ == '__main__':
    main()