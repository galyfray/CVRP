import numpy as np

def choose_data(nb):
    dataset_choice = ""
    match nb:
        case 0:
            dataset_choice = "E-n29-k4-s7-c200-ecap100.csv"
        case 1:
            dataset_choice = "E-n29-k4-s7-c6000-ecap99.csv"
        case 2:
            dataset_choice = "E-n30-k3-s7-c4500-ecap162.csv"
        case 3:
            dataset_choice = "E-n35-k3-s5-c4500-ecap138.csv"
        case 4:
            dataset_choice = "E-n37-k4-s4-c8000-ecap238.csv"
        case 5:
            dataset_choice = "E-n60-k5-s9-c160-ecap88.csv"
        case 6:
            dataset_choice = "E-n89-k7-s13-c220-ecap87.csv"
        case 7:
            dataset_choice = "F-n140-k7-s5-c2210-ecap307.csv"
        case 8:
            dataset_choice = "F-n49-k4-s4-c2010-ecap260.csv"
        case 9:
            dataset_choice = "F-n80-k4-s8-c30000-ecap53.csv"
        case 10:
            dataset_choice = "M-n110-k10-s9-c200-ecap118.csv"
        case 11:
            dataset_choice = "M-n126-k7-s5-c200-ecap199.csv"
        case 12:
            dataset_choice = "M-n163-k12-s12-c200-ecap100.csv"
        case 13:
            dataset_choice = "M-n212-k16-s12-c200-ecap100.csv"
        case 14:
            dataset_choice = "X-n1006-k43-s5-c131-ecap2536.csv"
        case 15:
            dataset_choice = "X-n147-k7-s4-c1190-ecap2762.csv"
        case 16:
            dataset_choice = "X-n221-k11-s9-c944-ecap1204.csv"
        case 17:
            dataset_choice = "X-n360-k40-s9-c436-ecap1236.csv"
        case 18:
            dataset_choice = "X-n469-k26-s10-c1106-ecap1230.csv"
        case 19:
            dataset_choice = "X-n577-k30-s4-c210-ecap2191.csv"
        case 20:
            dataset_choice = "X-n698-k75-s13-c408-ecap1336.csv"
        case 21:
            dataset_choice = "X-n759-k98-s10-c396-ecap1367.csv"
        case 22:
            dataset_choice = "X-n830-k171-s11-c358-ecap1385.csv"
        case 23:
            dataset_choice = "X-n920-k207-s4-c33-ecap2773.csv"
        case _:
            dataset_choice = "E-n29-k4-s7-c200-ecap100.csv"

    return dataset_choice

def read_data(filename):
    # using loadtxt()
    path = "./Utils/Datasets/" + filename
    data = np.loadtxt(path,
                    delimiter=";", dtype=str)
    return data

def sending_to_solver(data, algoParams):
    return ""
