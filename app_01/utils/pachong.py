#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Create Time: 2019/10/22 下午6:29
Author: ybx
"""

import requests
import urllib.request
import json
from lxml import etree
import re
import os
from bs4 import BeautifulSoup
import  random


proxy = '111.29.3.184:8080|111.29.3.224:8080|111.29.3.220:8080'
proxies = {
    'http': 'http://' + proxy.split('|')[random.randint(0, 2)],
    'https': 'https://' + proxy.split('|')[random.randint(0, 2)],

}
headers={

"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

def get_one_page(url):
    response = urllib.request.urlopen(url)
    text = response.read().decode('utf-8')
    return text


def get_url(offset, i):
    proxy = '111.29.3.184:8080|111.29.3.224:8080|111.29.3.220:8080'
    proxies = {
        'http': 'http://' + proxy.split('|')[random.randint(0, 2)],
        'https': 'https://' + proxy.split('|')[random.randint(0, 2)],

    }
    url = 'https://data.tbportals.niaid.nih.gov/cases?_take=21&_skip='+str(21 * i)
    r = requests.get(url, proxies=proxies)
    demo = r.text  # 服务器返回响应
    soup = BeautifulSoup(demo, "html.parser")
    # fout = open('D:/PycharmProjects/template_lesson/app_01/html/%s.txt' % str(offset)+'_'+str(i), 'a')
    # fout.write(demo)
    # fout.close()
    # p_all = soup.find_all(name='p', attrs={'class': "text-uppercase"})
    # list_a = [] # 记录每一个病人的ID
    # for p in p_all:
    #     patient_id = str(p.text)
    #     if patient_id.isdigit():
    #         list_a.append(patient_id)
    # print(len(list_a))
    a_all = soup.find_all('a')
    # print(a_all)
    pid_case = set()
    for a in a_all:
        try:
            href = a.attrs['href']
        except:
            pass
        if str(href).startswith('/patient/'):
            # print(href)
            pid_case.add('https://data.tbportals.niaid.nih.gov/'+href)
    fout = open('D:/PycharmProjects/template_lesson/app_01/html/%s.txt' % str(i), 'a')
    for url_a in pid_case:
        fout.write(url_a + '\n')

    fout.close()



def get_url_3():
    list_a = []
    with open('D:\PycharmProjects\\template_lesson\\app_01\html\\0.txt', 'r') as fin:
        for file in fin.readline():
            file = file.strip()
            list_a.append(file)

    for file in list_a:

        r = requests.get(file, proxies=proxies)
        demo = r.text  # 服务器返回响应
        soup = BeautifulSoup(demo, "html.parser")
        soup.find_all(name='h5', attrs={'class': 'text-uppercase'})
        print()





def get_url_2():
    url = 'https://data.tbportals.niaid.nih.gov/patient/1ff29035-0e5c-43d3-ab1d-63598f5053a3/case/details/c7edaeb1-6b28-449c-ab3d-1805bb75b4e0'
    r = requests.get(url)
    demo = r.text  # 服务器返回响应
    soup = BeautifulSoup(demo, "html.parser")
    list_pid = []
    pid = soup.find_all('h5', attrs={'class': 'text-uppercase'})[0]
    patient = str(pid.text)[-4:]
    list_pid.append(patient)
    # p_country = soup.find_all('p', attrs={'class': 'text-uppercase'})
    p_country = soup.find_all('p', attrs={'class': 'text-uppercase'})[2].text


    tables = soup.find_all('table', attrs={'class': "table table-hover"})[5]
    trs = tables.find_all('tr')
    list_view_url = []
    fout = open('D:/PycharmProjects/template_lesson/app_01/review_url/%s.txt' % (patient + '_' + p_country), 'a')
    for tr in trs:

        tds = tr.find_all('td')
        for index, value in enumerate(tds):
            if index == 5:
                urls = re.findall(r"<a.*?href=.*?>", str(value), re.S | re.M)
                for uurl in urls:
                    # list_view_url.append('https://data.tbportals.niaid.nih.gov'+str(uurl).split(' ')[7][6:-1])
                    fout.write('https://data.tbportals.niaid.nih.gov'+str(uurl).split(' ')[7][6:-1] + '\n')

    fout.close()





def main():
    save_path = "D:/PycharmProjects/template_lesson/app_01/dcm"
    path = 'D:/PycharmProjects/template_lesson/app_01/review_url/3693_BY.txt'
    a = path.split('/')[-1]
    patient_id = a.split('_')[0]
    country = a.split('_')[1][:-4]
    with open(path, 'r') as fin:
    # url = 'https://data.tbportals.niaid.nih.gov/patient/1ff29035-0e5c-43d3-ab1d-63598f5053a3/case/c7edaeb1-6b28-449c-ab3d-1805bb75b4e0/imaging/view/4d30803d-f6f7-4c01-a5e1-54b999016f57'
        for url in fin.readlines():
            url = url.strip()
            text = get_one_page(url)

            htmlinfo = etree.HTML(text)
            for person in htmlinfo.xpath('//script/text()'):
                if 'studyContainer' in str(person):
                    result = re.compile("\{.*\}")
                    dict_str = result.search(str(person))[0]
                    res = json.loads(dict_str)
                    list_a = res['series'][0]['instance']
                    for pid in list_a:
                        pid = pid[8:]
                        a_path = '/'.join(pid.split('/')[-3:-1])
                        insatnce_name = os.path.split(path)[-1]
                        # # print(a_path)
                        out_path = os.path.join(save_path, patient_id,country,a_path)
                        # print(out_path)
                        if not os.path.exists(out_path):
                            os.makedirs(out_path)
                        urllib.request.urlretrieve(pid, os.path.join(out_path, insatnce_name))
                        print('download')



if __name__ == '__main__':
    main()
    # get_url()
    #
    # for i in range(59,70):
    #     get_url(21, i)


    # get_url_2()