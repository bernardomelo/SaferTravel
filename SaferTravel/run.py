import flask
from collections import defaultdict
from flask import Flask, render_template, request

class Graph():
    def __init__(self):
        self.nos = defaultdict(list)
        self.dist = {}

    def add_no(self, inicio, destino, distancia):
        self.nos[inicio].append(destino)
        self.nos[destino].append(inicio)
        self.dist[(inicio, destino)] = distancia
        self.dist[(destino, inicio)] = distancia

    #def print_graph(self):
        #print('ADJACENCIA ENTRE NOS: ')
        #print(self.nos)
        #print('LISTA DE DISTANCIAS: ')
        #print(self.dist)
    #def get_distancia(self):
        #return self.dist

def dijsktra(graph, inicio, destino):
    curr_no = inicio
    menores_caminhos = {inicio: (None, 0)}
    visitados = set()

    while curr_no != destino:
        visitados.add(curr_no)
        destinations = graph.nos[curr_no]
        distancia_to_curr_no = menores_caminhos[curr_no][1]

        for prox_no in destinations:
            distancia = int(graph.dist[(curr_no, prox_no)]) + int(distancia_to_curr_no)
            if prox_no not in menores_caminhos:
                menores_caminhos[prox_no] = (curr_no, distancia)
            else:
                curr_menor_distancia = menores_caminhos[prox_no][1]
                if curr_menor_distancia > distancia:
                    menores_caminhos[prox_no] = (curr_no, distancia)

        prox_destinations = {node: menores_caminhos[node] for node in menores_caminhos if node not in visitados}
        if not prox_destinations:
            return []
        curr_no = min(prox_destinations, key=lambda k: prox_destinations[k][1])

    caminho = []
    while curr_no is not None:
        caminho.append(curr_no)
        prox_no = menores_caminhos[curr_no][0]
        curr_no = prox_no
    caminho = caminho[::-1]
    custo = menores_caminhos[caminho[-1]]
    custo = str(custo[1])
    caminho.append(custo)
    return caminho


f = open('USAir2010.txt', "r")
list_of_lists = []
graph = Graph()
for line in f:
    stripped_line = line.strip()
    line_list = stripped_line.split()
    list_of_lists.append(line_list)
f.close()
b = []
for x in list_of_lists:
    if int(x[2]) < 5:
        continue
    else:
        b.append(x)
for x in b:
    de = x[0]
    para = x[1]
    dist = x[2]
    graph.add_no(de, para, int(dist))

app = Flask(__name__)
#app.config['']
@app.route('/', methods=['POST','GET'])
def index():
    if flask.request.method == 'POST':
        from_content = request.form['contentFrom']
        to_content = request.form['contentTo']
        volta = dijsktra(graph, str(from_content), str(to_content))
        if len(volta) < 1:
            return "YOUR DESTINATION IS NOT REACHABLE BY PLANE THRU YOUR LOCATION"
        else:
            c = volta[-1]
            c = str(c)
            volta.pop(-1)
            return 'Your route:  \n' + '--> '.join([str(x) for x in volta]) + ' | ' + 'Only ' + c + ' people passed thru this route.'

    else:
        return render_template('home_screen.html')

if __name__ == "__main__":
    app.run(debug=True)