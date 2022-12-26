from csv import reader
from sys import exit
from math import sqrt
from operator import itemgetter
import csv


def Book_Appointment(Disease):

    Dict={1:'Fungalinfection',2:'Allergy',3:'GERD',4:'Chronic_cholestasis',5:'Drug_reaction',
    6:'Peptic_ulcer_diseae',7:'AIDS',8:'diabetes',9:'Gastroenteritis',10:'Bronchial_Asthma',11:'Hypertension',
    12:'Migraine',13:'Cervical_spondylosis',
    14:'Paralysis',15:'Jaundice',16:'Malaria',17:'Chicken_pox',18:'Dengue',19:'Typhoid',20:'Hepatitis_A',
    21:'Hepatitis_B',22:'Hepatitis_C',23:'Hepatitis_D',24:'Hepatitis_E',25:'Alcoholic_hepatitis',26:'Tuberculosis',
    27:'Common_Cold',28:'Pneumonia',29:'Dimorphic_hemmorhoids',30:'Heart_attack',31:'Varicose_veins',32:'Hypothyroidism',
    33:'Hyperthyroidism',34:'Hypoglycemia',35:'Osteoarthristis',36:'Arthritis',
    37:'Vertigo',38:'Acne',39:'Urinary_tract_infection',40:'Psoriasis',
    41:'Impetigo'}

    def get_key1(val):
        for key, value in Dict.items():
            if val == value:
                return key
     
        return "key doesn't exist"
    col_1 = get_key1(Disease)
    cad=[]
    cad.append(col_1)
    rows = [cad]
    filename = "Testing_Direct_Doctor_Details.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    def load_data_set(filename):
        try:
            with open(filename, newline='') as iris:
                return list(reader(iris, delimiter=','))
        except FileNotFoundError as e:
            raise e


    def convert_to_float(data_set, mode):
        new_set = []
        try:
            if mode == 'training':
                for data in data_set:
                    new_set.append([float(x) for x in data[:len(data)-1]] + [data[len(data)-1]])

            elif mode == 'test':
                for data in data_set:
                    new_set.append([float(x) for x in data])

            else:
                print('Invalid mode, program will exit.')
                exit()

            return new_set

        except ValueError as v:
            print(v)
            print('Invalid data set format, program will exit.')
            exit()


    def get_classes(training_set):
        return list(set([c[-1] for c in training_set]))


    def find_neighbors(distances, k):
        return distances[0:k]


    def find_response(neighbors, classes):
        votes = [0] * len(classes)

        for instance in neighbors:
            for ctr, c in enumerate(classes):
                if instance[-2] == c:
                    votes[ctr] += 1

        return max(enumerate(votes), key=itemgetter(1))


    def knn(training_set, test_set, k):
        distances = []
        dist = 0
        limit = len(training_set[0]) - 1

        # generate response classes from training data
        classes = get_classes(training_set)
        pq=[]
        try:
            for test_instance in test_set:
                for row in training_set:
                    for x, y in zip(row[:limit], test_instance):
                        dist += (x-y) * (x-y)
                    distances.append(row + [sqrt(dist)])
                    dist = 0
                distances.sort(key=itemgetter(len(distances[0])-1))


                # find k nearest neighbors
                neighbors = find_neighbors(distances, k)

                # get the class with maximum votes
                index, value = find_response(neighbors, classes)

                # Display prediction
                #print(classes[index])
                pq.append(classes[index])
            

                # empty the distance list
                distances.clear()
            print(pq[0])
            return (pq[0])
        

        except Exception as e:
            print(e)

    def main():
        try:
            # get value of k
            k =1
            ans="First predict your disease"

            # load the training and test data set
            training_file = "Training_Direct_Doctor_Details.csv"
            test_file ="Testing_Direct_Doctor_Details.csv"
            training_set = convert_to_float(load_data_set(training_file), 'training')
            test_set = convert_to_float(load_data_set(test_file), 'test')

            if not training_set:
                print('Empty training set')

            elif not test_set:
                print('Empty test set')

            elif k > len(training_set):
                print('Expected number of neighbors is higher than number of training data instances')

            else:
                ans=knn(training_set, test_set, k)

        except ValueError as v:
            print(v)

        except FileNotFoundError:
            print('File not found')


        f = open("Testing_Direct_Doctor_Details.csv", "w+")
        f.truncate()
        f.close()

        print(ans)
        return ans

    return main()


