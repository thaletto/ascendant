from ascendant.chart import Chart
from tests.horoscope import my_horoscope
import json


chart = Chart(my_horoscope)
d9 = chart.get_varga_chakra_chart(9)

print(json.dumps(d9, indent=4))