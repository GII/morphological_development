import pickle

# Class for saving relevant data during the learninf process .
class saveData(object):
    def __init__(self, tamano):

        self.contGen = 0
        self.directory = 0
        self.finalLenght = 0
        self.inputs_range = 0
        self.output_range = 0
        self.full_generations = 0

        self.median_value = [0 for n in range(0, tamano)]
        self.average_value = [0 for n in range(0, tamano)]
        self.max_fitness_value = [0 for n in range(0, tamano)]

# Denormalize the output values of the NeuralNetwork.
def deNormalizeOuputs(dato_out, clase):
    sig_sup = 1.0
    sig_inf = 0.0

    #          0  1  2  3  4  5  6  7
    ang_inf = [0, 0, 0, 0, 0, 0, 0, 0]
    ang_sup = [0, 0, 0, 0, 0, 0, 0, 0]

    rango = clase.output_range

    ang_inf[0] = rango[0]
    ang_sup[0] = rango[1]
    ang_inf[1] = rango[2]
    ang_sup[1] = rango[3]
    ang_inf[2] = rango[4]
    ang_sup[2] = rango[5]
    ang_inf[3] = rango[6]
    ang_sup[3] = rango[7]
    ang_inf[4] = rango[8]
    ang_sup[4] = rango[9]
    ang_inf[5] = rango[10]
    ang_sup[5] = rango[11]
    ang_inf[6] = rango[12]
    ang_sup[6] = rango[13]
    ang_inf[7] = rango[14]
    ang_sup[7] = rango[15]

    aux = [((((dato_out[n] - sig_inf) * (ang_sup[n] - ang_inf[n])) / (sig_sup -sig_inf)) + ang_inf[n]) for n in range(0, len(dato_out))]

    return aux

# Save relevant data in a fie.
def saveStatistics(clase):
    # Function for saving the data with pickle
    #           0  1  2
    saveData = [0, 0, 0]
    saveData[0] = clase.average_value
    saveData[1] = clase.median_value
    saveData[2] = clase.max_fitness_value

    text01 = clase.directory + '/' + 'Datos_MediaMediana_array_de_' + str(0) + '.txt'
    file = open(text01, 'wb')
    pickle.dump(saveData, file)
    file.close()
