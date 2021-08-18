import openpyxl

instances_detail = []

# projects= {"project_name":{area:[,]},""}
projects = {}
project_area = {}

area_list = ["华为华北一", "北京亦庄"]

# 第一步：打开工作簿
wb = openpyxl.load_workbook('hwhb&bjyz_project.xlsx')

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
                       memory, ip, components, create_time, status,
                       business_inspection_status]
    instances_detail.append(instance_detail)

for instance in instances_detail:
    project_name = instance[0].split(".")[0]
    if project_name not in projects.keys():
        projects[project_name] = []
        projects[project_name].append(instance)
    else:
        projects[project_name].append(instance)
# print(projects)
for key, value in projects.items():
    for instance in value:
        if key not in project_area.keys():
            # project_area[key] = []
            # project_area[key].append(instance[3])

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

for key, value in project_area.items():
    print(key, value)

print("\n\n")
for key, value in project_area.items():
    if len(value["area"]) < 2:
        print(key, value)

# print(instances_detail)

# 关闭工作薄
wb.close()
