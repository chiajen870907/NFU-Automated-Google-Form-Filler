import requests
from bs4 import BeautifulSoup


def merge(x,y):
    z = x.copy()
    z.update(y)
    return z


def Get_FormsURL_List(url_target='http://cdaas.nfu.edu.tw/files/11-1017-6809.php'):
    title_list = []
    url_forms = []
    res = requests.post(url_target)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    for entry in soup.select('.h3'):
        try:
            link = entry.find('a')['href']
            if link:
                title = entry.find('a').text
                title_list.append(title)
                url_forms.append(link)
        except:
            pass
    return title_list, url_forms


def ParsingHTML(url):
    # Create a session
    session = requests.Session()

    # Page 1 & 2

    html = session.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    # Burte force convert to Python list
    node = soup.find_all('script', type='text/javascript')
    data = node[1].text.replace('var FB_PUBLIC_LOAD_DATA_ = ', '')
    data = data.replace('null', '"null"')
    list = eval(data[0:-1])
    result = []
    value = []
    for entry_id in range(100):
        try:
            if list[1][1][entry_id][4][0][0] and str(list[1][1][entry_id][4][0][0]).isdigit():
                result.append('entry.' + str(list[1][1][entry_id][4][0][0]))
                value.append('5')
        except IndexError:
            pass


    page1_data = result[0:4]
    draftResponse_data = []
    for i in range(len(page1_data)):
        draftResponse_data.append(page1_data[i].replace('entry.', ''))


    pageHistory_ = soup.find('input', {'name': 'pageHistory'}).get('value')
    fbzx_ = soup.find('input', {'name': 'fbzx'}).get('value')
    fvv_ = soup.find('input', {'name': 'fvv'}).get('value')
    url_ = soup.find('meta', {'property': 'og:url'}).get('content')
    url_ = url_.replace('viewform?usp=send_form&usp=embed_facebook', 'formResponse')
    draftResponse_ = '[[[null,{},["學生"],0],[null,{},["男"],0],[null,{},["1次至5次"],0],[null,{},["mail"],0]],null,"{}"]'.format(draftResponse_data[0], draftResponse_data[1], draftResponse_data[2], draftResponse_data[3], fbzx_)

    payload1 = {'fvv': fvv_, 'draftResponse': draftResponse_, 'pageHistory': '0,1', 'fbzx': fbzx_}
    payload2 = dict(zip(result, value))

    for i in range(len(page1_data)):
        payload2.pop(page1_data[i])

    payload = merge(payload2, payload1)
    Response = session.post('https://docs.google.com/forms/d/e/1FAIpQLSfDB-2aS7vjsCGZxOzyHLwFnk0kqO2tFwc1PojVDFLOectT5g/formResponse',payload)
    return Response

if __name__ == '__main__':
    office,url = Get_FormsURL_List()
    for i in range(len(url)):
        if ParsingHTML(url[i]):
            print(office[i] + str(i+1) + '/' + str(len(office)) + '-----Finish')
