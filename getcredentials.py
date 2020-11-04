import panasonic_viera
rc = panasonic_viera.RemoteControl("TV_IP")
# Make the TV display a pairing pin code
rc.request_pin_code()
# Interactively ask the user for the pin code
pin = input("Enter the displayed pin code: ")
# Authorize the pin code with the TV
rc.authorize_pin_code(pincode=pin)
# Display credentials (application ID and encryption key)
print (rc.app_id)
print (rc.enc_key)