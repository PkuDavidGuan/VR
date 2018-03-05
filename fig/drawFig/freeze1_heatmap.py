import plotly.plotly as py
import plotly.graph_objs as go
import pickle
with open("/home/gys/VR/total.pkl", 'rb') as infile:
    total = pickle.load(infile)

a1 = [0 for i in range(100)]
for k in total:
    tmp = int(k / 20)
    if tmp > 99:
        tmp = 99
    a1[tmp] += total[k]
trace = go.Heatmap(z=[a1],
                   x=[i*4 for i in range(90)])
data=[trace]
py.plot(data, filename='heatmap')