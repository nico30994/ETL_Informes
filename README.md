## ETL_Informes
## Resumen
Se necesita solucionar las limitaciones del ERP a la hora de analizar los datos de forma rápida y consistente, por lo que se busca aplicar herramientas de ETL para transformar la información que antes se hacía manualmente, generar una API y recibir la información en formato JSON (un solo endpoint) para ser utilizado en dos tablas en un servidor HTML para garantizar la toma de decisiones basadas en datos de forma automática.

## Persistencia
El dataset se encuentra alojado en el ERP y se exporta en formato `.TXT` una vez al día. (Una mejora posible es usar directamente la BBDD del ERP pero no se usa para este caso)

## Lógica
El cliente de la API debe poder filtrar por número de orden de compra (OC).

## Prerequisitos
* FastAPI
* Pandas
* Python

## Desarrollo local
Luego de exportar el `.TXT` se ejecuta el script `ETL_RQ.py` localmente generando 2 archivos `JSON` en la carpeta out.
Enviando un `num_loc:int` al servidor ejecutado con `app.py`, la API procesa los JSON, los filtra y devuelve la información necesaria para cargar los datos.

## Test
Con FastAPI pasamos el parámetro para que filtre y devuelva la información para completar ambas tablas.
```
{
  "num_oc": 2,
  "order_desc": "string"
}
```
```
curl -X 'POST' \
  'http://127.0.0.1:8000/data' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "num_oc": 2,
  "order_desc": "string"
}'
```

Resultado:
```
{
  "index": [[
      "OC   00000002", "FER-073        " ],[
      "OC   00000002", "FER-074        " ],[
      "OC   00000002", "FER-073        " ],[
      "OC   00000002", "FER-074        "
      ]],

  "data": [[
      "PUNTA PHILLIPS Nº 1 (FELO)", 50 ], [
      "PUNTA PHILLIPS Nº 2 (FELO)", 100 ], [
      "FC A 00006-00047680", 50, "RT X 00003-00044125", 50 ], [
      "FC A 00006-00047680", 100, "RT X 00003-00044125", 100
    ]]
}
```

Estos datos ya pueden ser cargados ACA para ser consumidos por el cliente:
![tabla](https://github.com/nico30994/ETL_Informes/blob/main/imgs/out_html_tables.PNG)