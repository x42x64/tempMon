import matplotlib.pyplot as plt
import time
from loadLogIntoPandas import loadLogsAsDF

df = loadLogsAsDF('/mnt/quh/', start=time.time()-24*60*60.0)
df_plot = df[['data.Heat_Resorvoir0.value', 'data.Heat_Resorvoir1.value', 'data.Heat_Resorvoir2.value', 'data.Heat_Resorvoir3.value', 'data.SolarHeatExchangeLead.value', 'data.SolarHeatExchangeReturn.value']]
ax = df_plot.plot()
ax.grid(True)
plt.ylabel("°C")
plt.xlabel("UTC time (m-d h)")
fig = plt.gcf()
fig.set_size_inches(10, 5)
ax.legend_.remove()
plt.savefig("/mnt/ramdsk/graphHeatResorvoir.png")

fig_legend = plt.figure(figsize=(3.5, 1.5))
fig_legend.legend(ax.get_lines(), list(df_plot), loc='center', frameon=False)
plt.savefig("/mnt/ramdsk/graphHeatResorvoirLegend.png")
