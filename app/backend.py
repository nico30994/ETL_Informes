import json
json_path = ['./out/df_oc.json', './out/df_1er.json']

class num_to_json:

    def validar_nro(self, nro_oc):
        # len_nro --> Size of nro_oc_texto
        len_nro = len(str(nro_oc))

        # Format needed to index JSON --> OC   00000000N
        nro_oc_texto = 'OC   000000000'[0:13-len_nro] + str(nro_oc)
        return nro_oc_texto

    def filtrar(self, nro_oc:int, json_path):
        """
        The JSON is filtered, returning the requested data
        nro_oc : int = number provided by the client
        json_path = json paths

        return data in JSON format

        """

        JSONs = []
        for path in json_path:
            with open(path) as f:

                JSONs.append(json.load(f))

        nro_oc_texto = self.validar_nro(nro_oc)

        # Filter
        json_filtrado = []
        json_data_filtrado = []

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