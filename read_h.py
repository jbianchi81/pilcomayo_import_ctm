import pandas
from a5client import client

# importCSV("villamontes.csv", 42291)

# filename = "misionlapaz_3.csv"
# series_id = 42292
# value_column="Altura Horaria (m)"

def importCSV(filename : str, series_id : int, round_hour_only=True, value_column="Altura Horaria (m)"):
    data = pandas.read_csv(filename)
    data["Fecha"].fillna(method="ffill", inplace=True)
    data["timestart"] = pandas.to_datetime(data["Fecha"], format="%d-%m-%Y")
    data["timestart"] = data["timestart"] + pandas.to_timedelta(data["Hora"])
    data["timestart"] = data["timestart"].dt.tz_localize("America/Argentina/Buenos_Aires")
    data["series_id"] = series_id
    data["tipo"] = "puntual"
    data = data.set_index("timestart")
    if round_hour_only:
        data = data[(data.index.minute == 0) & (data.index.second == 0)]
    data = data.rename(columns={value_column: "valor"})
    client.createObservaciones(data, series_id=series_id)

# importCSV("misionlapaz_3.csv", 42292)