from DLSearch.services.instagram import Instagram


credentials = "credentials/ig_credentials.json"
output_path = 'output'
scrapping = Instagram(credentials=credentials)
scrapping.login()
following = scrapping.get_all_following('jorsemanreloaded')
following = following.get_nodes_after('dualipa')
print([node.username for node in following])
#followers = scrapping.get_all_followers()
#print([node.username for node in followers])
#scrapping.download_from_hashtag("rem", output_path, limit=1000)
for user in following:
    print("Download media from ", user.username)
    media = scrapping.download_all_media(user, output_path)
scrapping.close()