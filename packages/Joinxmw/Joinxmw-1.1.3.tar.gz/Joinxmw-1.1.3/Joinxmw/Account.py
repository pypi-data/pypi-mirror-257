import requests
from bs4 import BeautifulSoup

def reviewid(id):
    # 发送GET请求
    response = requests.get(f'https://world.xiaomawang.com/w/person/project/all/{id}')

    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找并获取特定元素的值
    Name = soup.find(class_='topheader__NickName-sc-13u5cd2-0 gjUfHk').text
    items = soup.find_all(class_='staticNumbItem__e-xf4')
    fans = items[0].find(class_='topNumber__AqPye').text
    following = items[1].find(class_='topNumber__AqPye').text
    likes = items[2].find(class_='topNumber__AqPye').text
    fanslikes = int(likes)/int(fans)
    jg = (f'名称:{Name},粉丝: {fans}, 关注: {following}, 被赞: {likes},粉丝点赞比:{str(fanslikes)}\n')
    return jg
def getworks(id):
    # 发送GET请求
    response = requests.get(f'https://world.xiaomawang.com/w/person/project/all/{id}')

    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有具有特定类名的元素
    works_elements = soup.find_all(class_='work-item__3YUOG work-item noBgWorkItem')

    # 计算元素的数量，即已发布作品的数量
    published_works = "作品数量为：" + str(len(works_elements))

    return published_works
def getworksdata(id):
    # 发送GET请求
    response = requests.get(f'https://world.xiaomawang.com/w/person/project/all/{id}')

    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有具有特定类名的元素
    works_elements = soup.find_all(class_='work-item__3YUOG work-item noBgWorkItem')

    total_views = 0
    total_comments = 0
    total_likes = 0
    for work in works_elements:
        # 在每个作品元素中查找data-item__aqeaK元素
        data_items = work.find_all(class_='data-item__aqeaK')

        # 如果找到了data-item__aqeaK元素，将其值加到对应的总数中
        if data_items is not None and len(data_items) == 3:
            total_views += int(data_items[0].text)
            total_comments += int(data_items[1].text)
            total_likes += int(data_items[2].text)

    return f'用户ID：{id},作品总浏览量: {total_views}, 作品总评论数: {total_comments}, 作品总点赞数: {total_likes}'






