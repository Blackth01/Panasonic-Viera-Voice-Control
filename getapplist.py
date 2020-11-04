import panasonic_viera

rc = panasonic_viera.RemoteControl("192.168.1.5", app_id="AVjZdqRjoRxCXg==", encryption_key="23Lw9k7hjaIhx9xsgRLkSg==")


print(rc.get_apps())