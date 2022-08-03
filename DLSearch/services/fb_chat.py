from fbchat import Client
from fbchat.models import *
import json
import os

class FB_chat(object):
    
    def __init__(self, credentials=False, username=False, password=False):
        super(FB_chat,self).__init__()
        self.credentials = credentials
        self.username = username
        self.password = password
        self.set_credentials()
        self.client = Client(self.username , self.password)
        #########################
        self.Colores=[ThreadColor.BILOBA_FLOWER, ThreadColor.BRILLIANT_ROSE, ThreadColor.CAMEO,ThreadColor.DEEP_SKY_BLUE,ThreadColor.FERN,
        ThreadColor.FREE_SPEECH_GREEN,ThreadColor.GOLDEN_POPPY,ThreadColor.LIGHT_CORAL,ThreadColor.MEDIUM_SLATE_BLUE,
        ThreadColor.MESSENGER_BLUE,ThreadColor.PICTON_BLUE,ThreadColor.PUMPKIN,ThreadColor.RADICAL_RED,ThreadColor.SHOCKING,ThreadColor.VIKING]
        
        self.Smiles={'Smile0':u'\U0001F600','Smile1':u'\U0001F601','Smile2':u'\U0001F602','Smile3':u'\U0001F603',
            'Smile4':u'\U0001F604','Smile5':u'\U0001F605','Smile6':u'\U0001F606','Smile7':u'\U0001F607',
            'Smile8':u'\U0001F608','Smile9':u'\U0001F609','SmileA':u'\U0001F60A','SmileB':u'\U0001F60B',
            'SmileC':u'\U0001F60E','SmileD':u'\U0001F60D','SmileE':u'\U0001F618','SmileF':u'\U0001F617',
            'SmileG':u'\U0001F619','SmileH':u'\U0001F61A','SmileI':u'\U0000263A','SmileJ':u'\U0001F642'}


        self.FaceNe={'FaceN0':u'\U0001F610','FaceN1':u'\U0001F611','FaceN2':u'\U0001F636','FaceN3':u'\U0001F60F',
            'FaceN4':u'\U0001F623','FaceN5':u'\U0001F625','FaceN6':u'\U0001F62E','FaceN7':u'\U0001F62F',
            'FaceN8':u'\U0001F62A','FaceN9':u'\U0001F62B','FaceNA':u'\U0001F634','FaceNB':u'\U0001F60C',
            'FaceNC':u'\U0001F61B','FaceND':u'\U0001F61C','FaceNE':u'\U0001F61D','FaceNF':u'\U0001F612',
                'FaceNG':u'\U0001F613','FaceNH':u'\U0001F614','FaceNI':u'\U0001F615','FaceNJ':u'\U0001F632'}

        self.FaceNG={'FaceN0':u'\U0001F616','FaceN1':u'\U0001F61E','FaceN2':u'\U0001F61F','FaceN3':u'\U0001F624',
            'FaceN4':u'\U0001F622','FaceN5':u'\U0001F62D','FaceN6':u'\U0001F626','FaceN7':u'\U0001F627',
            'FaceN8':u'\U0001F628','FaceN9':u'\U0001F629','FaceNA':u'\U0001F62C','FaceNB':u'\U0001F630',
            'FaceNC':u'\U0001F631','FaceND':u'\U0001F633','FaceNE':u'\U0001F635','FaceNF':u'\U0001F621',
                'FaceNG':u'\U0001F620'}

        self.FaceSk={'Sick':u'\U0001F637'}

        self.Emojis={'Angry':u'\U0001F621', 'Puño':u'\U0001F44A','Oso':u'\U0001F43B','Corazon':u'\U00002764',}

    def set_credentials(self):
        if self.credentials:
            self.username, self.password = self.get_cred_from_json()
        if not self.username or not self.password:
            raise Warning("No username or password passed.")

    def get_cred_from_json(self):
        credentials = open(self.credentials)
        data = json.load(credentials)
        return data.get("username",False), data.get("password",False)


    def send_emoji(self, id, emoji):
        self.client.sendEmoji(emoji=emoji,size=EmojiSize.LARGE,thread_id=id,thread_type=ThreadType.USER)

    def send_image(self, id, image):
        self.client.sendLocalImage(image,message='',thread_id=id, thread_type=ThreadType.USER)

    def send_folder_images(self, id, folder):
        for file in os.listdir(folder):
            if os.path.isfile(file):
                self.send_image(id,os.path.join(folder,file))
