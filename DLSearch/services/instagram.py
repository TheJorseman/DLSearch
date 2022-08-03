from DLSearch.tools.driver_selenium import FirefoxDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep
from requests import get
import os


class Instagram(object):
    def __init__(self, web_driver_path='DLSEARCH/tools/webdriver', credentials=False, username=False, password=False, sleep_time=3):
        super(Instagram,self).__init__()
        self.driver = InstagramSelenium(web_driver_path=web_driver_path)
        self.credentials = credentials
        self.username = username
        self.password = password
        self.sleep_time = sleep_time
        self.verify_credentials()
        self.media_query_id = "17888483320059182"
        self.following_query_id = "17874545323001329"
        self.followers_query_id = "17888483320059182"
        self.hashtag_query_id = "17875800862117404"
        self.cursor = "&after={end_cursor}"
        self.query = "https://www.instagram.com/graphql/query/?query_id={query_id}&id={id}&first={max_count}"
        self.explore_query = "https://www.instagram.com/graphql/query/?query_id={query_id}&tag_name={tag_name}&first={max_count}"
        self.data = None

    
    def verify_credentials(self):
        if self.credentials:
            self.username, self.password = self.get_cred_from_json()

    def login(self):
        self.verify_credentials()
        if not self.username or not self.password:
            raise Warning("No username or password passed.")
        self.driver.set_credentials(self.username, self.password)
        self.wait()
        self.driver.to_home()
        WebDriverWait(self.driver.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@tabindex='0']")))
        self.driver.close_notification_advise()

    def wait(self):
        sleep(self.sleep_time)

    def get_profile_info(self, username):
        return self.driver.profile_info(username)

    def get_cred_from_json(self):
        credentials = open(self.credentials)
        data = json.load(credentials)
        return data.get("username",False), data.get("password",False)

    def get_media_from_user(self, user):
        if isinstance(user, str):
            _id = self.get_profile_info(user)['id']
        elif isinstance(user, QueryNode):
            return self.get_all_media(user.id)
        raise ValueError("No id Found")

    def get_all_media(self, _id):
        return self.execute_query(_id, self.media_query_id)

    def execute_query(self, _id, query_id, max_count=100, max_data=100000):
        has_next_page = True
        end_cursor = ''
        org_query = self.query.format(query_id=query_id, id=_id, max_count=max_count)
        data = None
        while(has_next_page):
            query = org_query
            if end_cursor != '':
                query = org_query + self.cursor.format(end_cursor=end_cursor)
            print(query)
            self.driver.open_url(query, sleep_time_s=1)
            res_data = self.get_json()
            if data is None:
                data = res_data
            else:
                data.append(res_data)
            has_next_page = res_data.has_next_page
            end_cursor = res_data.end_cursor
        return data


    def execute_query_explore(self, hashtag, max_count=100, max_data=100000):
        has_next_page = True
        end_cursor = ''
        org_query = self.explore_query.format(query_id=self.hashtag_query_id, tag_name=hashtag, max_count=max_count)
        data = None
        data_len = 0
        while(has_next_page):
            if data_len >= max_data:
                break
            query = org_query
            if end_cursor != '':
                query = org_query + self.cursor.format(end_cursor=end_cursor)
            self.driver.open_url(query, sleep_time_s=1)
            res_data = self.get_json()
            if data is None:
                data = res_data
            else:
                data.append(res_data)
            has_next_page = res_data.has_next_page
            end_cursor = res_data.end_cursor
            data_len = len(data)
        return data

    def check_path(self, path):
        os.makedirs(path, exist_ok=True)


    def get_media_from_hashtag(self, hashtag, limit=100000):
        return self.execute_query_explore(hashtag, max_data=limit)

    def download_from_hashtag(self, hashtag, output_path, save_metadata=True, limit=100000):
        image_output_path = os.path.join(output_path, hashtag, "images")
        self.check_path(image_output_path)
        if save_metadata:
            metadata_output_path = os.path.join(output_path, hashtag, "metadata")
            self.check_path(metadata_output_path)
        media = self.get_media_from_hashtag(hashtag, limit=limit)
        for med in media:
            if med.is_video:
                pass
            response = get(med.display_url)
            with open(os.path.join(image_output_path, med.id+".jpg"), "wb") as file:
                file.write(response.content)
            file.close()
            if save_metadata:
                with open(os.path.join(metadata_output_path, med.id+".json"), 'w') as f:
                    json.dump(med.__dict__, f)
        return image_output_path   

    def get_all_followers(self, username=False, max_count=100, only_usernames=False):
        _id = False
        if username:
            data = self.get_profile_info(username)
            _id = data['id']
        else:
            _id = self.data['id']
        data = self.execute_query(_id, self.followers_query_id, max_count=max_count)
        if only_usernames:
            return [node.username for node in data]
        return data

    def get_nodes(self, data):
        return data['data']['user']['edge_follow']['page_info']['edges']

    def get_json(self):
        pre = self.driver.driver.find_elements_by_xpath('//pre')
        if len(pre) == 0:
            WebDriverWait(self.driver.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//a[@id='rawdata-tab']")))
            self.driver.driver.find_elements_by_xpath("//a[@id='rawdata-tab']")[0].click()
            pre = self.driver.driver.find_elements_by_xpath('//pre')[0]
        return QueryRes(pre.text)


    def get_all_following(self, username=False, max_count=100, only_usernames=False):
        _id = False
        if username:
            data = self.get_profile_info(username)
            _id = data['id']
        elif self.data is None:
            self.data = self.get_profile_info(self.username)
            _id = self.data['id']
        else:
            _id = self.data['id']
        data = self.execute_query(_id, self.following_query_id, max_count=max_count)
        if only_usernames:
            return [node.username for node in data]
        return data

    def download_all_media(self, user, output_path, save_metadata=True, download_video=False):
        image_output_path = os.path.join(output_path, user.username, "images")
        self.check_path(image_output_path)
        if save_metadata:
            metadata_output_path = os.path.join(output_path, user.username, "metadata")
            self.check_path(metadata_output_path)
        media = self.get_media_from_user(user)
        for med in media:
            if med.is_video:
                pass
            response = get(med.display_url)
            with open(os.path.join(image_output_path, med.id+".jpg"), "wb") as file:
                file.write(response.content)
            file.close()
            if save_metadata:
                with open(os.path.join(metadata_output_path, med.id+".json"), 'w') as f:
                    json.dump(med.__dict__, f)
        return image_output_path

    def close(self):
        self.driver.close()

class InstagramSelenium(FirefoxDriver):
    def __init__(self, web_driver_path='DLSEARCH/tools/webdriver'):
        super(InstagramSelenium,self).__init__(web_driver_path=web_driver_path)
        self.base = "https://www.instagram.com"
        self.open_url(self.base)

    def to_home(self):
        self.open_url(self.base)

    def close_notification_advise(self):
        elements = self.driver.find_elements_by_xpath("//button[@tabindex='0']")
        cancel = elements[-1].click()

    def goto_user(self, user):
        self.open_url(self.base + "/" + user)

    def parse_account_data(self, script):
        idx = script.find('{"ACCOUNT_ID"')
        idx_2 = script[idx::].find('}')
        str_json = script[idx:idx+idx_2+1]
        return json.loads(str_json)

    def parse_json_str(self, data):
        remain = 0
        for i, letter in enumerate(data):
            if letter == '{':
                remain += 1
            elif letter == '}':
                remain -= 1
            if remain == 0:
                return i
        return -1

    def parse_embedded_dict(self, str_json):
        _dict = json.loads(str_json)
        for key, value in _dict.items():
            if isinstance(value, str) and '{' in value:
                _dict[key] = self.parse_embedded_dict(value)
        return _dict

    def parse_user_data(self, script):
        idx = script.find('{"raw"')
        idx_2 = self.parse_json_str(script[idx::])
        str_json = script[idx:idx+idx_2+1]
        return self.parse_embedded_dict(str_json)

    def search_profile_id(self, source):
        search = "profile_id"
        idx = source.find(search)
        return source[idx+13:idx+23]

    def get_json_response(self):
        user_id = self.search_profile_id(self.driver.page_source)
        return {'id': user_id}

    def profile_info(self, username):
        url = "https://www.instagram.com/{}".format(username)
        self.open_url(url)
        return self.get_json_response()

    def parse_json_data(self, data):
        return

    def goto_pub(self, short_code):
        url = "https://www.instagram.com/p/{}/".format(short_code)
        return

    def followers_page(self):
        return 

class QueryData(object):
    def __init__(self, data):
        super(QueryData,self).__init__()
        self.__set_attr__(data)

    def __set_attr__(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)

class QueryNode(QueryData):
    def __init__(self, data):
        super(QueryNode,self).__init__(data)

    def __repr__(self) -> str:
        return str(self.__dict__)

class QueryRes(QueryData):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.data = self.parse_embedded_dict(raw_data)
        super(QueryRes, self).__init__(self.data)
        self.__set_user_data__()
        self.parse_nodes()
        self.parse_page_info()
        self.res = []
        self.type = None

    @property
    def has_next_page(self):
        return self.page_info.has_next_page

    @property
    def end_cursor(self):
        return self.page_info.end_cursor

    def parse_page_info(self):
        self.page_info = QueryData(self.user_data["page_info"])
  
    def parse_embedded_dict(self, str_json):
        _dict = json.loads(str_json)
        for key, value in _dict.items():
            if isinstance(value, str) and '{' in value:
                _dict[key] = self.parse_embedded_dict(value)
        return _dict

    def __set_user_data__(self):
        if 'hashtag' in self.data.keys():
            self.user_data = self.data["hashtag"]['edge_hashtag_to_media']
            self.type = 'hashtag'
        elif 'edge_owner_to_timeline_media' in self.data["user"].keys():
            self.user_data = self.data["user"]['edge_owner_to_timeline_media']
            self.type = 'media'
        elif 'edge_follow' in self.data["user"].keys():
            self.user_data = self.data["user"]['edge_follow']
            self.type = 'following'
        else:
            import pdb;pdb.set_trace()

    def parse_nodes(self):
        nodes = self.user_data['edges']
        self.nodes = [QueryNode(node['node']) for node in nodes]

    def get_nodes(self):
        return self.nodes

    def append(self, data):
        self.res.append(data)
        self.nodes += data.nodes

    def get_nodes_after(self, username):
        output = []
        append = False
        for node in self.nodes:
            if append:
                output.append(node)
            if node.username == username:
                append = True
        return output


    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        return self.nodes[index]


class JsonIGData(object):
    def __init__(self, raw_data):
        super(JsonIGData,self).__init__()
        self.raw_data = raw_data
        key = "graphql" if self.raw_data.get("graphql",False) else "data"
        self.user_data = self.raw_data[key]["user"]

    def get_fid(self):
        return self.user_data["fbid"]

    def get_id(self):
        return self.user_data["id"]

    def get_followers_number(self):
        return self.user_data["edge_followed_by"]["count"]
    
    def get_follow_number(self):
        return self.user_data["edge_follow"]["count"]

    def get_name(self):
        return self.user_data["full_name"]

    def is_private(self):
        return self.user_data["is_private"]

    def is_verified(self):
        return self.user_data["is_verified"]

    def get_biography(self):
        return self.user_data["biography"]

    def get_profile_photo_url(self, hd=True):
        if hd:
            return self.user_data["profile_pic_url_hd"]
        return self.user_data["profile_pic_url"]

    def get_username(self):
        return self.user_data["username"]

    def get_connected_fb_page(self):
        return self.user_data["connected_fb_page"]

    def get_media_post_number(self):
        return self.user_data["edge_owner_to_timeline_media"]["count"]
        
    def get_end_cursor(self):
        return self.user_data["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

    def get_media(self):
        edges = self.user_data["edge_owner_to_timeline_media"]["edges"]
        media = []
        for edge in edges:
            media.append(IgMedia(edge["node"]))
        return media


class IgMedia(object):
    def __init__(self, node):
        super(IgMedia,self).__init__()
        self.node = node
        self.id = node["id"]
        self.is_video = node["is_video"]
        self.url = node["display_url"]
        self.ig_description = node.get("accessibility_caption",False)
        self.description = node["edge_media_to_caption"]["edges"][0]["node"]["text"] if len(node["edge_media_to_caption"]["edges"]) > 0 else ""
        self.comments_number = node["edge_media_to_comment"]["count"]
        self.timestamp = node.get("taken_at_timestamp",False)
        self.location = node.get("location",False)
        self.shortcode = node["shortcode"]
