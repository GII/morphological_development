import pickle

# ----------------------------------------------------------------------------------------------------------------------
class saveData(object):
    # Class for saving relevant data during the learninf process
    def __init__(self, tamano):

        self.sim = 0
        self.client = 0
        self.locked = 0
        self.contGen = 0
        self.species = []
        self.directory = 0
        self.ang_reduced = 0
        self.finalLenght = 0
        self.inputs_range = 0
        self.output_range = 0
        self.full_generations = 0

        self.falls_value = [0 for n in range(0, tamano)]
        self.median_value = [0 for n in range(0, tamano)]
        self.average_value = [0 for n in range(0, tamano)]
        self.fall_of_the_best = [0 for n in range(0, tamano)]
        self.max_fitness_value = [0 for n in range(0, tamano)]
        self.timeStep_of_the_best = [0 for n in range(0, tamano)]
# ----------------------------------------------------------------------------------------------------------------------

# --------------------------------  Normalizar la salida de la red  ----------------------------------------------------
def normalizeOuputs(dato_out, clase):
    sig_sup = 1.0
    sig_inf = 0.0

    #          0  1  2  3  4  5  6  7  8  9 10 11 12 13
    ang_inf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ang_sup = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    dof_limit = 30.0
    jrom_limit = 150.0
    if clase.contGen < dof_limit:
        rango = clase.locked
        
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
        ang_inf[8] = rango[16]
        ang_sup[8] = rango[17]
        ang_inf[9] = rango[18]
        ang_sup[9] = rango[19]
        ang_inf[10] = rango[20]
        ang_sup[10] = rango[21]
        ang_inf[11] = rango[22]
        ang_sup[11] = rango[23]
        ang_inf[12] = rango[24]
        ang_sup[12] = rango[25]
        ang_inf[13] = rango[26]
        ang_sup[13] = rango[27]
    
    elif clase.contGen < jrom_limit and clase.contGen >= dof_limit:
        rango = clase.locked
        ang_inf[0] = rango[0]
        ang_sup[0] = rango[1]
        ang_inf[1] = rango[2]
        ang_sup[1] = rango[3]
        ang_inf[2] = rango[4]
        ang_sup[2] = rango[5]
        ang_inf[3] = clase.locked[6] + (clase.contGen-dof_limit) * ((clase.output_range[6] - clase.locked[6])/(jrom_limit-dof_limit))
        ang_sup[3] = clase.locked[7] + (clase.contGen-dof_limit) * ((clase.output_range[7] - clase.locked[7])/(jrom_limit-dof_limit))
        ang_inf[4] = clase.locked[8] + (clase.contGen-dof_limit) * ((clase.output_range[8] - clase.locked[8])/(jrom_limit-dof_limit))
        ang_sup[4] = clase.locked[9] + (clase.contGen-dof_limit) * ((clase.output_range[9] - clase.locked[9])/(jrom_limit-dof_limit))
        ang_inf[5] = clase.locked[10] + (clase.contGen-dof_limit) * ((clase.output_range[10] - clase.locked[10])/(jrom_limit-dof_limit))
        ang_sup[5] = clase.locked[11] + (clase.contGen-dof_limit) * ((clase.output_range[11] - clase.locked[11])/(jrom_limit-dof_limit))
        ang_inf[6] = rango[12]
        ang_sup[6] = rango[13]
        ang_inf[7] = rango[14]
        ang_sup[7] = rango[15]
        ang_inf[8] = rango[16]
        ang_sup[8] = rango[17]
        ang_inf[9] = clase.locked[18] + (clase.contGen-dof_limit) * ((clase.output_range[18] - clase.locked[18])/(jrom_limit-dof_limit))
        ang_sup[9] = clase.locked[19] + (clase.contGen-dof_limit) * ((clase.output_range[19] - clase.locked[19])/(jrom_limit-dof_limit))
        ang_inf[10] = clase.locked[20] + (clase.contGen-dof_limit) * ((clase.output_range[20] - clase.locked[20])/(jrom_limit-dof_limit))
        ang_sup[10] = clase.locked[21] + (clase.contGen-dof_limit) * ((clase.output_range[21] - clase.locked[21])/(jrom_limit-dof_limit))
        ang_inf[11] = clase.locked[22] + (clase.contGen-dof_limit) * ((clase.output_range[22] - clase.locked[22])/(jrom_limit-dof_limit))
        ang_sup[11] = clase.locked[23] + (clase.contGen-dof_limit) * ((clase.output_range[23] - clase.locked[23])/(jrom_limit-dof_limit))
        ang_inf[12] = clase.locked[24] + (clase.contGen-dof_limit) * ((clase.output_range[24] - clase.locked[24])/(jrom_limit-dof_limit))
        ang_sup[12] = clase.locked[25] + (clase.contGen-dof_limit) * ((clase.output_range[25] - clase.locked[25])/(jrom_limit-dof_limit))
        ang_inf[13] = clase.locked[26] + (clase.contGen-dof_limit) * ((clase.output_range[26] - clase.locked[26])/(jrom_limit-dof_limit))
        ang_sup[13] = clase.locked[27] + (clase.contGen-dof_limit) * ((clase.output_range[27] - clase.locked[27])/(jrom_limit-dof_limit))
    else:
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
        ang_inf[8] = rango[16]
        ang_sup[8] = rango[17]
        ang_inf[9] = rango[18]
        ang_sup[9] = rango[19]
        ang_inf[10] = rango[20]
        ang_sup[10] = rango[21]
        ang_inf[11] = rango[22]
        ang_sup[11] = rango[23]
        ang_inf[12] = rango[24]
        ang_sup[12] = rango[25]
        ang_inf[13] = rango[26]
        ang_sup[13] = rango[27]

    aux = [round(((((dato_out[n] - sig_inf) * (ang_sup[n] - ang_inf[n])) / (sig_sup - sig_inf)) + ang_inf[n]), 5) for n in range(0, len(dato_out))]

    return aux
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def saveStatistics(clase):
    # Function for saving the data with pickle
    #           0  1  2  3  4  5
    saveData = [0, 0, 0, 0, 0, 0]
    saveData[0] = clase.average_value
    saveData[1] = clase.median_value
    saveData[2] = clase.max_fitness_value
    saveData[3] = clase.falls_value
    saveData[4] = clase.fall_of_the_best
    saveData[5] = clase.timeStep_of_the_best

    text01 = clase.directory + '/' + 'Datos_MediaMediana_array_de_' + str(0) + '.txt'
    file = open(text01, 'wb')
    pickle.dump(saveData, file)
    file.close()
# ----------------------------------------------------------------------------------------------------------------------
