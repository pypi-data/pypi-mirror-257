###Documentación en https://github.com/lucasbaldezzari/sarapy/blob/main/docs/Docs.md
import warnings
import numpy as np
# from sarapy.mlProcessors import PlantinFMCreator
from sarapy.mlProcessors import PlantinClassifier

class OpsProcessor():
    """Clase para procesar las operaciones de los operarios. La información se toma de la base de datos
    hostórica y se procesa para obtener un array con las operaciones clasificadas para cada operario.
    
    La clase recibe una muestra desde la base de datos histórica y la procesa para obtener las
    operaciones clasificadas para cada operario. Se clasifican las operaciones desde el punto de vista
    del plantín y del fertilizante. La clasificación del tipo de operación respecto de plantín se hace
    con el pipeline para plantín, idem para el fertilizante.
    """
    
    def __init__(self, **kwargs):
        """Constructor de la clase OpsProcessor.
        
        Args:
            - distanciaMedia: Distancia media entre operaciones.
        """

        plclass_map = {"classifier_file","imputeDistances", "distanciaMedia",
                       "umbral_precision"," dist_mismo_lugar", "max_dist",
                       "umbral_ratio_dCdP", "deltaO_medio"}

        kwargs_plclass = {}
        ##recorro kwargs y usando plclass_map creo un nuevo diccionario con los valores que se pasaron
        for key, value in kwargs.items():
            if key in plclass_map:
                kwargs_plclass[key] = value
        
        self._plantin_classifier = PlantinClassifier.PlantinClassifier(**kwargs_plclass)
        # self._fertilizerFMCreator = FertilizerFMCreator() ## PARA IMPLEMENTAR
        
        self._operationsDict = {} ##diccionario de operarios con sus operaciones
        self._classifiedOperations = np.array([]) ##array con las operaciones clasificadas
        self._last_row_db = 0 ##indicador de la última fila de los datos extraidos de la base de datos histórica
        
    def processOperations(self, data):
        """Método para procesar las operaciones de los operarios.

        Se toma una nueva muestra y se procesa la información para clasificar las operaciones considerando el
        plantín y por otro lado el fertilizante.
        Se retorna un array con las clasificaciones concatenadas, manteniendo el orden de las operaciones por operario.
        
        Args:
            data: Es una lista de diccionario. Cada diccionario tiene los siguientes keys.
            
            id_db, ID_NPDB, TLM_SPBB, date_oprc, latitud, longitud, precision
            
            Ejemplo:
            
            {"id_db":"1", "ID_NPDB":"XXAA123",
            "TLM_SPBB": "1010001000010010101100010110000111101101001100000000000000000000",
            "date_oprc":"2024-02-17 12:33:20",
            "Latitud":"-32.145564789", "Longitud":"-55.145564789", "Precision": "0.25"}
            
        Returns:
            Lista de diccionarios con las clasificaciones. Cada diccionario tiene la forma
            {"id_db": 10, "tag_seedling": 1, "tag_fertilizer": 1}
        """
        
        ##chqueo que newSample no esté vacío
        if len(data) != 0:
            newSample = self.transformInputData(data)
            #Si tenemos nuevas operaciones, actualizamos el diccionario de operaciones
            self.updateOperationsDict(newSample) #actualizamos diccionario interno de la clase
            plantinClassifications = self.classifyForPlantin() #clasificamos las operaciones para plantín
            # ops_numbers = newSample[:,0]
            ops_numbers = self.getActualOperationsNumbers() #obtenemos los números de operaciones desde el diccionario de operaciones
            return plantinClassifications.round(2), ops_numbers
        
        else:
            self.resetAllNewSamplesValues()
            return None
        
    def updateOperationsDict(self, newSample):
        """Actualiza el diccionario de operaciones.
        
        Args:
            - newSample: lista con los datos (numpy.array de strings) de las operaciones.
            La forma de cada dato dentro de la lista newSample es (n,6). Las columnas de newSample son,
            
                - 0: id_db
                - 1: ID_NPDP
                - 2: TLM_SPBB
                - 3: date_oprc
                - 4: latitud
                - 5: longitud
                - 6: precision
                
        Returns:
            - None
            NOTA: PENSAR SI SE DEVUELVE ALGO COMO UN TRUE O FALSE PARA SABER SI SE ACTUALIZÓ O NO EL DICCIONARIO
            DE MANERA CORRECTA O HUBO ALGÚN PROBLEMA Y ASÍ VER QUÉ HACER EN EL MAIN
        """
        
        ID_NPDPs_w_newOperations = np.unique(newSample[:,1]) ##identificadores de operarios con nuevas operaciones en la muestra
        
        ##chqueo si estos ID_NPDPs ya están en el diccionario, sino los agrego
        for ID_NPDP in ID_NPDPs_w_newOperations:
            if ID_NPDP not in self._operationsDict:
                #El diccionario contiene la siguiente información:
                #sample_ops: np.array con las columnas de TLM_SPBB, date_oprc, lat, lon, precision
                #last_oprc: np.array de la última operación con las columnas de TLM_SPBB, date_oprc, lat, lon, precision
                #first_day_op_classified: booleano para saber si es la primera operación del día fue clasificada
                self._operationsDict[ID_NPDP] = {"sample_ops": None,
                                                 "last_oprc": None, 
                                                 "first_day_op_classified": False,
                                                 "new_sample": False,
                                                 "ops_numbers": None} #inicio del diccionario anidado para el nuevo operario
                
        ##actualizo el diccionario con las operaciones nuevas para aquellos operarios que correspondan
        for ID_NPDP in ID_NPDPs_w_newOperations:
            sample_ops = newSample[newSample[:,1] == ID_NPDP][:,2:] #me quedo con las columnas de TLM_SPBB, date_oprc, lat, lon, precision
            ops_numbers = newSample[newSample[:,1] == ID_NPDP][:,0]
            ##actualizo el diccionario
            self._operationsDict[ID_NPDP]["sample_ops"] = sample_ops
            self._operationsDict[ID_NPDP]["ops_numbers"] = ops_numbers
            ##chequeo si tenemos última operación, si es así, asignamos dicha operación en la primera fila de sample_ops
            last_op = self._operationsDict[ID_NPDP]["last_oprc"]
            ###si last_op es not None y last_op no está vacía, entonces concatenamos last_op con sample_ops
            if last_op is not None and last_op.size != 0:
                self._operationsDict[ID_NPDP]["sample_ops"] = np.vstack((last_op, sample_ops))
                
        self.updateNewSamplesValues(ID_NPDPs_w_newOperations) #actualizo el estado de 'new_sample' en el diccionario de operaciones
        self.updateLastOperations(ID_NPDPs_w_newOperations) #actualizo la última operación de una muestra de operaciones en el diccionario de operaciones

    def classifyForPlantin(self):
        """Método para clasificar las operaciones para plantín.
        Se recorre el diccionario de operaciones y se clasifican las operaciones para plantín.

        Returns:
            - plantinClassifications: np.array con las clasificaciones de las operaciones para plantín.
        """

        ##creamos/reiniciamos el array con las clasificaciones de las operaciones para plantín
        plantinClassifications = None
        
        ##me quedo con los ID_NPDPs que tengan _operationsDict[ID_NPDP]["new_sample"] iguales a True
        ops_with_new_sample = [ID_NPDP for ID_NPDP in self.operationsDict.keys() if self.operationsDict[ID_NPDP]["new_sample"]]

        for ID_NPDP in ops_with_new_sample:#self.operationsDict.keys():
            ##clasificamos las operaciones para plantín
            operations = self.operationsDict[ID_NPDP]["sample_ops"]
            classified_ops = self._plantin_classifier.classify(operations)
            
            ##chequeo si first_day_op_classified es True, si es así, no se considera la primera fila de las classified_ops
            if self.operationsDict[ID_NPDP]["first_day_op_classified"]:
                classified_ops = classified_ops[1:]
                
            # plantinClassifications = np.vstack((plantinClassifications, classified_ops)) if plantinClassifications is not None else classified_ops
            plantinClassifications = np.concatenate((plantinClassifications, classified_ops)) if plantinClassifications is not None else classified_ops
            
            self.operationsDict[ID_NPDP]["first_day_op_classified"] = True

        return plantinClassifications
            
    def updateLastOperations(self, ID_NPDPs_w_newOperations):
        """Método para actualizar la última operación de una muestra de operaciones en el diccionario de operaciones

        Args:
            - newSample: lista con los datos (numpy.array de strings) de las operaciones.
            La forma de cada dato dentro de la lista newSample es (n,6). Las columnas de newSample son,
            
                - 0: id_db
                - 1: ID_NPDP
                - 2: TLM_SPBB
                - 3: date_oprc
                - 4: latitud
                - 5: longitud
                - 6: precision
        """
        
        for ID_NPDP in ID_NPDPs_w_newOperations:
            self._operationsDict[ID_NPDP]["last_oprc"] = self._operationsDict[ID_NPDP]["sample_ops"][-1]

    def updateOperationsNumbers(self, new_ops_numbers):
        """Método para actualizar los números de operaciones en el diccionario de operaciones.

        Args:
            - new_ops_numbers: array de la forma (n,2) con los números de operaciones en la primer columna y los ID_NPDPs en la segunda.
        """
        ID_NPDPs_w_newOperations = np.unique(new_ops_numbers[:,1]) ##identificadores de operarios con nuevas operaciones en la muestra
        opsNumbersList = np.array([]) ##array con los números de operaciones

        for ID_NPDP in ID_NPDPs_w_newOperations:
            opsNumbersList = np.append(opsNumbersList, self.operationsDict[ID_NPDP]["ops_numbers"].flatten())

        return opsNumbersList
    
    def updateNewSamplesValues(self, ID_NPDPs_w_newOperations):
        """Método para actualizar el estado de 'new_sample' del diccionario de operaciones.

        Args:
            - ID_NPDPs_w_newOperations: lista con los ID_NPDPs que tienen nuevas operaciones.
        """

        ##recorro el diccionario de operaciones y actualizo el estado de 'new_sample' a
        ##True para los ID_NPDPs que tienen nuevas operaciones y a False para los que no tienen nuevas operaciones
        for ID_NPDP in self.operationsDict.keys():
            if ID_NPDP in ID_NPDPs_w_newOperations:
                self._operationsDict[ID_NPDP]["new_sample"] = True
            else:
                self._operationsDict[ID_NPDP]["new_sample"] = False
    
    def resetAllNewSamplesValues(self):
        """Método para resetar todos los valores de new_sample en el diccionario de operaciones.
        """
        
        for ID_NPDP in self.operationsDict.keys():
            self._operationsDict[ID_NPDP]["new_sample"] = False

    def getActualOperationsNumbers(self):
        """Método para obtener los números de operaciones desde el diccionario de operaciones para aquellos operarios que
        tienen nuevas operaciones en la muestra."""

        opsNumbersList = np.array([])
        for ID_NPDP in self.operationsDict.keys():
            if self.operationsDict[ID_NPDP]["new_sample"]:
                opsNumbersList = np.append(opsNumbersList, self.operationsDict[ID_NPDP]["ops_numbers"].flatten())

        return opsNumbersList
    
    def updateFirstDayOp(self):
        """Método para actualizar el indicador de si es la primera operación del día para cada operario en el diccionario de operaciones.
        """

        for ID_NPDP in self.operationsDict.keys():
            self._operationsDict[ID_NPDP]["first_day_op_classified"] = False
            
    def transformInputData(self, data):
        """Función para transformar los datos de entrada que llegan del decoder
        
        Args:
            data: Es una lista de diccionario. Cada diccionario tiene los siguientes keys.
            
            id_db, ID_NPDB, TLM_SPBB, date_oprc, latitud, longitud, precision
            
            Ejemplo:
            
            {"id_db":"1", "ID_NPDB":"XXAA123",
            "TLM_SPBB": "1010001000010010101100010110000111101101001100000000000000000000",
            "date_oprc":"2024-02-17 12:33:20",
            "Latitud":"-32.145564789", "Longitud":"-55.145564789", "Precision": "0.25"}
        
        Returns:
            Retorna un array de strings con la siguiente estructura
            - 0: id_db
            - 1: ID_NPDP
            - 2: TLM_SPBB
            - 3: date_oprc
            - 4: latitud
            - 5: longitud
            - 6: precision
        """
    
        ##convierto list_of_dics a un array de strings
        newSample = np.array([[d["id_db"],
                            d["ID_NPDB"],
                            d["TLM_SPBB"],
                            d["date_oprc"],
                            d["Latitud"],
                            d["Longitud"],
                            d["precision"]] for d in data])
        
        return newSample
    
    def cleanSamplesOperations(self):
        """Método para limpiar las operaciones de un operario en el diccionario de operaciones.

        Args:
            - newSample: lista con los datos (numpy.array de strings) de las operaciones.
            La forma de cada dato dentro de la lista newSample es (n,6). Las columnas de newSample son,
            
                - 0: id_db
                - 1: ID_NPDP
                - 2: TLM_SPBB
                - 3: date_oprc
                - 4: latitud
                - 5: longitud
                - 6: precision
        """

        for ID_NPDP in self.operationsDict.keys():
            self._operationsDict[ID_NPDP]["sample_ops"] = None
            
    @property
    def operationsDict(self):
        return self._operationsDict
    
    
if __name__ == "__main__":
    #cargo archivo examples\volcado_17112023_NODE_processed.csv
    import pandas as pd
    import numpy as np
    import os
    path = os.path.join(os.getcwd(), "examples\\volcado_17112023_NODE_processed_modified.csv")
    data_df = pd.read_csv(path, sep=";", )
    raw_data = data_df.to_numpy().astype(str)
    
    ##tomo los valos de data_df y formo una lista de diccionarios por cada fila
    samples = data_df.to_dict(orient="records")
    
    # from sarapy.dataProcessing import OpsProcessor
    op = OpsProcessor(classifier_file="examples\\pip_lda_imp.pkl", imputeDistances = False)
    op.operationsDict

    ##procesamos una muestra
    print(op.processOperations(samples))