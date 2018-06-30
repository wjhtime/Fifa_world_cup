"""FIFA World Cup
Usage:
    fifa -l | --list
    fifa -h | --help
    fifa -v | --version


Options:
    -h --help        Show this help message and exit.
    -v --version     Show version.
    -l --list        Show game list.
"""

from docopt import docopt
import requests
from lxml import etree


class Fifa():

    url = "http://2018.sohu.com/2018schedules/"

    __headers__ = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://2018.sohu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }

    def __init__(self, **kwargs):
        self._args = kwargs

    def execute(self):
        if self._args.get('-l') or self._args.get('--list'):
            self.getList()
            try:
                self.getList()
            except Exception:
                print("无法获取比赛内容")

    def getList(self):
        try:
            response = requests.get(self.url, headers=self.__headers__)
            response.encoding = 'GBK'

            for sel in etree.HTML(response.text).xpath("//div[@id='turnIDA']/div[@class='turn'][1]/div[@class='TableC']"):
                # 组
                print(sel.xpath("h2/span/text()")[0] + ":")
                for sel2 in sel.xpath("table/tbody/tr/td/table/tbody/tr[@bgcolor='#ffffff']"):
                    id = sel2.xpath("td[1]/div/span/text()")[0]
                    date = sel2.xpath("td[2]/div/span/text()")[0]
                    country1 = sel2.xpath("td[3]/div/span/text()")[0]
                    country2 = sel2.xpath("td[5]/div/span/text()")[0]
                    print("{} \t {}vs {} \t {}". format(id, country1, country2, date))
                print('-'*100)
            exit()
        except requests.exceptions.ConnectTimeout:
            print("获取比赛内容失败，请检查网络连接状况")

def cli():
    args = docopt(__doc__)
    Fifa(**args).execute()

if __name__=="__main__":
    cli()