import pandas as pd
import numpy as np

'''
Definition of the titles of the columns
{[column names in ERP : column names in needed]}
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
  '''
  If col_1 contains val_str new columns are created
  The information is sorted by exchanging the values ​​of certain columns if necessary

     df_p = df
     col_1 = Column containing the word
     val_str = Word to search
     col_new = Temporary column titles, can be a list
     val_new = Temporary column value, can be a list (df_p.fc_nro)
  '''
  # If it finds an inconsistency (FC in RT column or vice versa) in the table, it exchanges the columns
  for i in range(len(col_new)):
    df_p.loc[col_1.str.contains(val_str,na=False), col_new[i]] = val_new[i]
    i += 1
  
  # Replace temporary columns
  for i in range(len(col_new)):
    df_p.loc[col_1.str.contains(val_str,na=False), str(val_new[i].name)] = df_p['{}_2'.format(val_new[i].name)]
    i += 1
    
  return df_p.drop(col_new, axis=1)

def main():
    # Import
    df = pd.read_csv('./RQ.txt', sep='\t', encoding='utf-8', error_bad_lines=False)

    # Transform
    df = df[df['Ítem - Artículo - Cód. Gen.'].notna()]
    df = df.fillna(np.nan).replace([np.nan], [None])

    # Replace column names
    df.rename(dict_cols, axis=1, inplace=True)

    df = interc_cols(
        df_p = df,
        col_1 = df.fc_nro,
        val_str = 'RT',
        col_new = ['rt_fecha_2','rt_nro_2','rt_cantidad_2','fc_fecha_2','fc_nro_2','fc_cantidad_2'],
        val_new = [df.fc_fecha, df.fc_nro, df.fc_cantidad, df.rt_fecha, df.rt_nro, df.rt_cantidad]
    )

    # Table generation
    df_oc = df.set_index(['oc_nro','oc_articulo_generico'])
    df_oc = df_oc.loc[pd.IndexSlice[:],['oc_articulo_desc','oc_cantidad']].drop_duplicates().sort_values(['oc_nro','oc_articulo_generico'])

    df_1er = df.set_index(['oc_nro','oc_articulo_generico'])
    df_1er = df_1er.loc[pd.IndexSlice[:],['fc_nro','fc_cantidad','rt_nro','rt_cantidad']].sort_values(['oc_nro','oc_articulo_generico'])

    df_oc.columns = ['Descripción','Cantidad']
    df_1er.columns = ['Nro. FC', 'Cant. FC','Nro. RT', 'Cant. RT']

    # Export
    df_oc.to_json('./out/df_oc.json',orient="split")
    df_1er.to_json('./out/df_1er.json',orient="split")
    print("JSON Exportado a carpeta 'out'")


main()