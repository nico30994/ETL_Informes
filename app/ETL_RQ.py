import pandas as pd
import numpy as np

'''
Definir los nombres de las columnas a cambiar
{[nombre de columna en ERP : nombre de columna necesario]}
'''

dict_cols = {
        'Comp. - F. Emisión' : 'rq_fecha_emision',
        'Ítem - F. Recepción' : 'rq_fecha_recepcion',
        'Comp. Ppal. - Tipo Comp. - Cód.' : 'rq_tipo',
        'Comp. Ppal. - Nro.' : 'rq_nro',
        'Ítem - U. M. 1' : 'rq_um',
        'Ítem - Cant. UM 1' : 'rq_cantidad',
        'Comp. - F. Emisión.1' : 'oc_fecha_emision',
        'Ítem - F. Recepción.1' : 'oc_fecha_recepcion',
        'Comp. Ppal. OC' : 'oc_nro',
        'Comp. - Prov. - Cód.' : 'oc_prov_cod',
        'OC Razón Social' : 'oc_prov_nombre',
        'Ítem - Artículo - Cód. Gen.' : 'oc_articulo_generico',
        'Ítem - Artículo - Elem. 1 - Cód.' : 'oc_articulo_generico_1atrib',
        'Ítem - Desc.' : 'oc_articulo_desc',
        'Ítem - Leyenda Astos.' : 'oc_articulo_leyenda',
        'Ítem - U. M. 1.1' : 'oc_um',
        'Ítems OC' : 'oc_cantidad',
        'Mon. Emisión - Símbolo' : 'oc_moneda',
        'Comp. - Cotiz. mon. Emisión' : 'oc_cotizacion',
        'Ítem - Pr. Unitario' : 'oc_precio_unitario',
        'Ítem - Impte.Total mon. Emisión' : 'oc_precio_total',
        'Pend. Entrega Real' : 'pendiente_entrega',
        'Pend. de Fact' : 'pendiente_facturacion',
        'NP N°' : 'NP_nro',
        'OP Web' : 'OPW_nro',
        'Lugar de Entrega' : 'entrega',
        'Responsable de Recepcion' : 'Recepcion',
        'Ítem - F. Recepción.2' : 'fc_fecha',
        'Comp. Ppal. P1' : 'fc_nro',
        'Ítem - U. M. 1.2' : 'fc_um',
        'Ítems Posterior 1' : 'fc_cantidad',
        'Ítem - F. Recepción.3' : 'rt_fecha',
        'Comp. Ppal. P2' : 'rt_nro',
        'Ítem - U. M. 1.3' : 'rt_um',
        'Ítems Posterior 2' : 'rt_cantidad'
}

def interc_cols(df_p,col_1,val_str,col_new,val_new):
  ''' Crea columnas nuevas si col_1 contiene val_str
   Sirve para intercambiar los valores de la columna porque se encuentran desordenados desde el ERP

     df_p = df
     col_1 = Columna que contiene la palabra
     val_str = Palabra a buscar
     col_new = Título de la columna temporal, puede ser lista
     val_new = Valor de la columna temporal, puede ser lista de columnas a reemplazar (df_p.fc_nro)
  '''
  # Si encuentra una inconsistencia (FC en columna RT o al revez) en la tabla realiza el intercambio de las columnas
  for i in range(len(col_new)):
    df_p.loc[col_1.str.contains(val_str,na=False), col_new[i]] = val_new[i]
    i += 1
  
  # Reemplazar columnas temporales
  for i in range(len(col_new)):
    df_p.loc[col_1.str.contains(val_str,na=False), str(val_new[i].name)] = df_p['{}_2'.format(val_new[i].name)]
    i += 1
    
  return df_p.drop(col_new, axis=1)

def main():
        # Leer TXT --> Querie RQ-OC-RTO-FC del ERP
    df = pd.read_csv('./RQ.txt', sep='\t', encoding='utf-8', error_bad_lines=False)

    # Borrar leyendas que no sirven para el análisis (NaN en "oc_articulo_generico" // 'Ítem - Artículo - Cód. Gen.')
    df = df[df['Ítem - Artículo - Cód. Gen.'].notna()]

    # Reemplazar NaN => None (Para que lo acepte postgresql)
    df = df.fillna(np.nan).replace([np.nan], [None])

    # Reemplazar títulos de cols
    df.rename(dict_cols, axis=1, inplace=True)

    df = interc_cols(
        df_p = df,
        col_1 = df.fc_nro,
        val_str = 'RT',
        col_new = ['rt_fecha_2','rt_nro_2','rt_cantidad_2','fc_fecha_2','fc_nro_2','fc_cantidad_2'],
        val_new = [df.fc_fecha, df.fc_nro, df.fc_cantidad, df.rt_fecha, df.rt_nro, df.rt_cantidad]
    )

    ### Genero tabla de [OC, item] --> Cantidades
    df_oc = df.set_index(['oc_nro','oc_articulo_generico'])
    df_oc = df_oc.loc[pd.IndexSlice[:],['oc_articulo_desc','oc_cantidad']].drop_duplicates().sort_values(['oc_nro','oc_articulo_generico'])

    ### Genero tabla de [OC, 1er posterior, 2do posterior] --> Cantidades
    df_1er = df.set_index(['oc_nro','oc_articulo_generico'])
    df_1er = df_1er.loc[pd.IndexSlice[:],['fc_nro','fc_cantidad','rt_nro','rt_cantidad']].sort_values(['oc_nro','oc_articulo_generico'])

    # Cambiar nombre de columnas
    df_oc.columns = ['Descripción','Cantidad']
    df_1er.columns = ['Nro. FC', 'Cant. FC','Nro. RT', 'Cant. RT']

    # Exportar JSON
    df_oc.to_json('./out/df_oc.json',orient="split")
    df_1er.to_json('./out/df_1er.json',orient="split")
    print("JSON Exportado a carpeta 'out'")


main()