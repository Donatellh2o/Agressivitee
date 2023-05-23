import json
import xlsxwriter
from pylab import array
import random
from tqdm import tqdm

global nb_food
global nb_kinds
global nb_means
global kind_chance
global mean_chance
global iteration


nb_food = 100
nb_kinds = 100
nb_means = 30
surviving_kind_mean = [0.5, 1]
reproduct_kind_mean = [0, 0.5]
iteration = 100
sheet_name = 'result'


global nb
nb = nb_kinds + nb_means

global final
global inter
global data
global kinds
global means
final = []
data = []

global workbook
global worksheet
workbook = xlsxwriter.Workbook(sheet_name+'.xlsx')
worksheet = workbook.add_worksheet()

# --------------DEF--------------


def beginning():

    for i in range(nb):

        if (i <= nb_kinds-1):
            result = {
                'type': 'kind',
                'status': 'living',
                'food_partner': 0
            }

        if (i > nb_kinds-1) and (i <= nb-1):
            result = {
                'type': 'mean',
                'status': 'living',
                'food_partner': 0
            }
        data.append(result)

    how_many()

    global cell_format
    global header_format
    global header2_format

    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_font_name('Avenir Next')

    header_format = workbook.add_format()
    header_format.set_align('center')
    header_format.set_align('vcenter')
    header_format.set_font_name('Avenir Next')
    header_format.set_bold()
    header_format.set_bg_color('#BEBEBE')

    header2_format = workbook.add_format()
    header2_format.set_align('center')
    header2_format.set_align('vcenter')
    header2_format.set_font_name('Avenir Next')
    header2_format.set_bold()
    header2_format.set_bg_color('#DCDCDC')

    worksheet.write('A1', 'Time', header_format)
    worksheet.write('B1', 'Kinds', header_format)
    worksheet.write('C1', 'Means', header_format)
    worksheet.write('A2', 0, header2_format)
    worksheet.write('B2', nb_kinds, cell_format)
    worksheet.write('C2', nb_means, cell_format)


def how_many():
    global kinds
    global means
    kinds = 0
    means = 0

    for i in (data):

        if (i['type'] == 'kind') and (i['status'] == 'living'):
            kinds += 1

        if (i['type'] == 'mean') and (i['status'] == 'living'):
            means += 1

        if (i['type'] != 'kind') and (i['type'] != 'mean'):
            print('error')


def choose():

    for i in range(len(data)):

        if data[i]['status'] == 'living':
            rand = random.randint(0, nb_food)
            data[i]['choice'] = rand
            data[i]['food_partner'] = 0


def single(type_user):
    result = {
        'type': type_user,
        'status': 'living'
    }
    data.append(result)


def kind_mean(idkind):

    if (random.random() > surviving_kind_mean[0]):
        data[idkind]['status'] = 'dead'

    if (random.random() < reproduct_kind_mean[1]):
        result = {
            'type': 'mean',
            'choice': nb_food+1,
            'status': 'living'
        }
        data.append(result)


def mean_mean(id1, id2):
    data[id1]['status'] = 'dead'
    data[id2]['status'] = 'dead'


def write(i):
    worksheet.write('A'+str(i+3), i+1, header2_format)
    worksheet.write('B'+str(i+3), kinds, cell_format)
    worksheet.write('C'+str(i+3), means, cell_format)


# --------------BEGINNING--------------

beginning()

# --------------ITERATIONS--------------

for i in tqdm(range(iteration)):

    choose()

    length = len(data)

    for u in range(length):

        if data[u]['status'] == 'living':

            for y in range(u+1, length):

                if data[y]['status'] == 'living':

                    if (data[u]['choice'] == data[y]['choice']):
                        data[u]['food_partner'] += 1

                        if (data[u]['type'] == data[y]['type'] == 'mean'):
                            mean_mean(u, y)

                        elif (data[u]['type'] != data[y]['type']):

                            if (data[u]['type'] == 'kind'):
                                kind_mean(u)
                            elif (data[y]['type'] == 'kind'):
                                kind_mean(y)

            if (data[u]['food_partner'] == 0):
                single(data[u]['type'])

    how_many()
    write(i)

# --------------CHART--------------

chart = workbook.add_chart({'type': 'area', 'subtype': 'stacked'})

chart.add_series(
    {
        'name': 'Kinds',
        'categories': '=Sheet1!$A$2:$A$'+str(iteration+2),
        'values': '=Sheet1!$B$2:$B$'+str(iteration+2)
    }
)

chart.add_series(
    {
        'name': 'Means',
        'categories': '=Sheet1!$A$2:$A$'+str(iteration+2),
        'values': '=Sheet1!$C$2:$C$'+str(iteration+2)
    }
)


worksheet.insert_chart("D1", chart, {"x_offset": 25, "y_offset": 10})

# --------------END--------------

workbook.close()
