from DLSearch.services.fb_chat import FB_chat

Cblue = '100002144413235'

client = FB_chat(credentials="credentials/fb_credentials.json")
client.send_folder_images(Cblue,"dataset/any_cemar")