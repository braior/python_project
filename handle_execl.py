import openpyxl
from openpyxl import Workbook
import json
from urllib import request


def read_all_data():
    # 第一步：打开工作簿
    wb = openpyxl.load_workbook('hwhb1&bjyz cmdb_product.xlsx')

    # 第二步：选取表单
    sh = wb['Sheet1']
    # 第三步：读取数据
    # print(list(sh.rows)[1:])     # 按行读取数据，去掉第一行的表头信息数据
    for instance in list(sh.rows)[1:]:
        instance_detail = []
        hostname = instance[0].value
        instance_attach = instance[1].value
        instance_type = instance[2].value
        generator_room = instance[3].value
        environment = instance[4].value
        base_components = instance[5].value
        cpu_core = instance[6].value
        memory = instance[7].value
        dist = instance[8].value
        ip = instance[9].value
        components = instance[10].value
        create_time = str(instance[11].value)
        status = instance[12].value
        business_inspection_status = instance[13].value

        instance_detail = [hostname, instance_attach, instance_type,
                           generator_room, environment, base_components, cpu_core,
                           memory, dist, ip, components, create_time, status,
                           business_inspection_status]
        instances_detail.append(instance_detail)

    # 关闭工作薄
    wb.close()


def get_project_name():
    for instance in instances_detail:
        project_name = instance[0].split(".")[0]
        if project_name not in projects.keys():
            projects[project_name] = []
            projects[project_name].append(instance)
        else:
            projects[project_name].append(instance)

def get_project_area():
    for key, value in projects.items():
        for instance in value:
            if key not in project_area.keys():
                project_area[key] = {}
                project_area[key]["area"] = []
                project_area[key]["instance_type"] = ""
                project_area[key]["area"].append(instance[3])
                project_area[key]["instance_type"] = instance[2]

            else:
                if instance[3] not in project_area[key]["area"]:
                    project_area[key]["area"].append(instance[3])
                if instance[2] != project_area[key]["instance_type"]:
                    project_area[key]["instance_type"] = instance[2]

# 将area只有一个区域的project写入excel
def write_area_le_2_to_excel():
    count = 0
    # url = 'https://example.domain.com/api/projects/xxx-yyy-zzz'
    header = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'X-XSRF-TOKEN': 'eyJpdiI6IlhNSWIraFRcL25KUzdOaTh6Mmkxa09BPT0iLCJ2YWx1ZSI6IkdiYTg5UGFrRnkrcTh5b3ROWTF6Q3BKV0VnYkZzaTBiclprOHduZ1wva1NVN1VJYUQ0a3BkOVNQeHNXcDFycjdWUkUzeVpMSUdGZFFnYUU2VldNYVwvVUE9PSIsIm1hYyI6ImQ4NjllZThkZmViODJkYjI0Mzg5MDA3NzRkNWNjNTI4MzZjOGUwOWUwMDE0ODliZGQ4MmUxZGY0NWE2MDE5ODEifQ==',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://example.domain.com/projects/xxx-yyy-zzz/instances',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_ga=GA1.2.1698452664.1602837251; _uq=f8f1bf241b7b2e3694e2f853bb930894; AGENT20170621jssdkcross=%7B%22props%22%3A%7B%7D%2C%22subject%22%3A%7B%7D%2C%22object%22%3A%7B%7D%2C%22uniqueId%22%3A%22175402d7b6d524-0f6962e06b14b1-584b2f11-13c680-175402d7b6e826%22%2C%22domain%22%3A%22devops.zhubajie.la%22%7D; route=bd23b5fcfd6821a6db21629dcfd33d27; SEARCH-OPTION=name; bossuid=26231; source=op; XSRF-TOKEN=eyJpdiI6IlhNSWIraFRcL25KUzdOaTh6Mmkxa09BPT0iLCJ2YWx1ZSI6IkdiYTg5UGFrRnkrcTh5b3ROWTF6Q3BKV0VnYkZzaTBiclprOHduZ1wva1NVN1VJYUQ0a3BkOVNQeHNXcDFycjdWUkUzeVpMSUdGZFFnYUU2VldNYVwvVUE9PSIsIm1hYyI6ImQ4NjllZThkZmViODJkYjI0Mzg5MDA3NzRkNWNjNTI4MzZjOGUwOWUwMDE0ODliZGQ4MmUxZGY0NWE2MDE5ODEifQ%3D%3D; laravel_session=eyJpdiI6ImJlUnZlME9jWjZZVDRPc0c0WUZXc2c9PSIsInZhbHVlIjoieDlJVElrcjJsNzBVeGFQZjhkSXB6Vzh5cEYwaFVuVnJuV1A2N2FlZkR1ZTA1azJLemNCQVwvNWJMeTVWbUlJTjIxb255ODFldEtla0d5QnBaNlhxNUx3PT0iLCJtYWMiOiI1NDkyODEwM2IzMDUwOTI3YjM3YzQwNjJhNDBmNjRlZmU5MzQyYjA1ZmExOGQ4ZjQ1OTYwMDkzMzAzNTJmNmFjIn0%3D',
        'If-None-Match': 'W/"c67223fd7aa0ac450966c6c3ecb9bf44768890ff"',
    }
    wb_new = Workbook()
    ws1 = wb_new.active
    ws1.title = "生产环境-单机房部署项目"  # 修改表名称
    tableTitle = ['项目名', '机房', '实例类型', '域名', '项目类型', '维护团队', '开发负责人']
    ws1.append(tableTitle)

    for key, value in project_area.items():
        if len(value["area"]) < 2:
            count += 1
            url = 'https://example.domain.com/api/projects/' + key
            print(url)

            # 该urllib.request模块定义了有助于在复杂环境中打开URL（主要是HTTP）的函数和类-基本身份验证和摘要身份验证，重定向，Cookie等。
            rq = request.Request(url, headers=header)

            # 打开一个url的方法，返回一个文件对象，然后可以进行类似文件对象的操作
            res = request.urlopen(rq)

            respoen = res.read()
            result = str(respoen, encoding="utf-8")
            cl = json.loads(result)

            domain = cl['data']['domain']
            type_ = cl['data']['type']
            group_name = cl['data']['group_name']
            development_masters = cl['data']['development_masters'][0]['name']

            tmp = [key, value["area"][0], value["instance_type"],
                   domain, type_, group_name, development_masters]
            ws1.append(tmp)

    wb_new.save(filename="./生产环境-单机房部署项目.xlsx")


if __name__ == "__main__":
    instances_detail = []
    projects = {}
    project_area = {}

    read_all_data()
    get_project_name()
    get_project_area()
    write_area_le_2_to_excel()
