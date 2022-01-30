import json
json_path = ['./out/df_oc.json', './out/df_1er.json']

class num_to_json:

    def validar_nro(self, nro_oc):
        # len_nro --> Tamaño de dígitos de nro_oc_texto
        len_nro = len(str(nro_oc))

        # Agrego texto para indexear en JSON
        nro_oc_texto = 'OC   000000000'[0:13-len_nro] + str(nro_oc)
        return nro_oc_texto

    def filtrar(self, nro_oc:int, json_path):
        # Creo las variables con los JSON a filtrar
        JSONs = []
        for path in json_path:
            with open(path) as f:

                JSONs.append(json.load(f))

        # Cambio el formato del input para que coincida con el archivo JSON (EJ: 30 --> OC   00000030)
        nro_oc_texto = self.validar_nro(nro_oc)

        # Creo la variable que van a contener la información fitrada
        json_filtrado = []
        json_data_filtrado = []

        # Filtro según nro_oc_texto
        for json_file in JSONs:
            j = 0
            for elemento in json_file['index']:
                if str(elemento[0]) == str(nro_oc_texto):
                    json_filtrado.append(elemento)
                    json_data_filtrado.append(json_file['data'][j])
                j += 1

        out = {
            'index':json_filtrado,
            'data':json_data_filtrado
        }
        return out