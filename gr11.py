import numpy as np
import plotly.graph_objs as go
import plotly.plotly


dictActual = {}
dictCalc = {}
dictCalcX = {}

for idx,item in enumerate(allDataIRITest):
    dictActual[str(idx)] = item
    dictCalc[str(idx)] = calculatedIRI12[idx]
    dictCalcX[str(idx)] = calculatedIRI12X[idx]
import operator
sorted_x = sorted(dictActual.items(), key=operator.itemgetter(1))
newIRIAc = []
newIRICAlc = []
newIRICAlcX = []
newIRICAlcXY = []
print(sorted_x)
for key in sorted_x:
    newIRIAc.append(dictActual[key[0]])
    newIRICAlc.append(dictCalc[key[0]])
    newIRICAlcX.append(dictCalcX[key[0]])
    newIRICAlcXY.append((dictCalcX[key[0]] + dictCalc[key[0]])/2.0)

mean_absolute_error123Xy=mean_absolute_error(np.array(newIRIAc), np.array(newIRICAlcXY))

print("mean_absolute_error :",mean_absolute_error123)

count123 = []
for idx,i in enumerate(allDataIRITest):
    count123.append(idx+1)
spikesGraphs = []
traceActual = go.Scatter(
        x=count123,
        y=newIRIAc,
        mode='lines',
        name="Actual"
    )
spikesGraphs.append(traceActual)
plotly.offline.plot({
        "data": spikesGraphs,
        "layout": go.Layout(yaxis=dict(range=[2,10]),title="Ac vs CAL All 500:"+str(round(mean_absolute_error123,5)))
}, auto_open=True, filename='actualVSPredictedIRI300.html')