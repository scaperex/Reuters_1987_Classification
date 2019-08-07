import pickle
import numpy as np
from sklearn import metrics, preprocessing

import Calculations
import File_reader
import parsing


class Model:
    def __init__(self, path_to_precooked_data):
        print("Parsing train data...")
        raw_data = parsing.parsing_data(path_to_precooked_data, False)
        print("parse train data COMPLETE")
        self.data = File_reader.File_reader(raw_data)
        self.inv_labels = self.data.inv_labels
        print("Creating train_features and train_labels...")
        # self.train_features, self.train_labels = self.data.build_set_tfidf()
        print("Creating train_features and train_labels COMPLETE")
        # print("Number of train articles:", self.train_features.shape[0])
        # TODO remove before submission
        # try:
        #     pickle.dump(self.data, open("data.p", 'wb'), protocol=4)
        #     pickle.dump(self.inv_labels, open("inv_labels.p", 'wb'), protocol=4)
        #     pickle.dump(self.train_features, open("train_features.p", 'wb'), protocol=4)
        #     pickle.dump(self.train_labels, open("train_labels.p", 'wb'), protocol=4)
        # except:
        #     pass

        # print("Restoring train features and labels from pickle..")
        # self.train_features = pickle.load(open("train_features.p", 'rb'))
        # self.train_labels = pickle.load(open("train_labels.p", 'rb'))
        # self.data = pickle.load(open("data.p", 'rb'))
        # self.inv_labels = pickle.load(open("inv_labels.p", 'rb'))
        ### Till here

    def predict(self, path_to_test_set):
        predictions = []
        k = 1
        print("Parsing test data...")
        raw_test = parsing.parsing_data(path_to_test_set, True)
        print("parse test data COMPLETE")
        print("Creating test_features...")
        test_features = self.data.parse_test(raw_test)
        print("Creating test_features COMPLETE")
        print("Running KNN...")
        for index in range(test_features.shape[0]):
            instance = test_features[index]
            binary_predictions = self.knn_predict(instance, k)
            labels = self.labels_from_prediction(binary_predictions)
            predictions.append(labels)
        # TODO Delete
        # print(Calculations.f1_score( ,binary_predictions))
        return tuple(predictions)

    def labels_from_prediction(self, binary_predictions):
        predicted_labels = []
        indexes = np.where(binary_predictions)[0]
        for index in indexes:
            predicted_labels.append(self.inv_labels[index])
        return tuple(predicted_labels)

    def knn_predict(self, instance, k):
        closest_neighbors_labels = self.k_nearest_neighbors(instance, k)
        return self.best_neighbor_match_check(closest_neighbors_labels,k)

    def k_nearest_neighbors(self, test_instance, k):
        """
        kNN algorithm. Returns proposed label of a given test image 'test_instance', by finding the
        'k' similar neighbors (euclidean distance) for 'training_set' set of images.
        """
        closest_neighbors_labels = []
        distances = []

        length = np.ma.size(self.train_features, 0)-1
        for i in range(length):
            dist = Calculations.cosine_distance(self.train_features[i], test_instance)
            distances.append(dist)
        max_dist = max(distances)
        distances = np.array(distances, dtype=float)
        for neighbor in range(k):
            closest_neighbor = np.argmin(distances)
            closest_neighbors_labels.append(self.train_labels[closest_neighbor, :])
            distances[closest_neighbor] = max_dist

        return np.array(closest_neighbors_labels)

    @staticmethod
    def best_neighbor_match_check(k_neighbors_labels,k):
        """	Returns the values with the most repetitions in `k_neighbors`. """
        length = k_neighbors_labels.shape[1]-1
        labels = []
        for index in range(length):
            k_neighbors_label = k_neighbors_labels[:, index]
            if (k_neighbors_label.sum()/k)>0.5:
                labels.append(1)
            else:
                labels.append(0)
        return labels



    def predict_f1(self, path_to_test_set):
        # predictions = []
        # k = 5
        # print("Parsing test data...")
        raw_test = parsing.parsing_data(path_to_test_set, False)
        # print("parse test data COMPLETE")
        # print("Creating test_features...")
        test_features, test_labels = self.data.parse_test(raw_test, True)
        print(test_features.shape, test_labels.shape)
        # print("Creating test_features COMPLETE")
        # print("Running KNN...")
        # for index in range(test_features.shape[0]):
        #     instance = test_features[index]
        #     binary_predictions = self.knn_predict(instance, k)
        #     labels = self.labels_from_prediction(binary_predictions)
        #     predictions.append(labels)
        # # TODO Delete
        predictions = [('usa', 'acq'), ('coffee', 'colombia'), ('usa', 'grain', 'corn'), ('brazil', 'usa'), ('usa',), ('usa',), ('uk', 'usa', 'japan'), ('uk', 'japan'), ('usa', 'livestock', 'ec', 'carcass'), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('usa',), ('usa', 'grain', 'corn', 'mexico'), ('usa', 'earn'), ('usa',), ('usa', 'acq'), ('usa', 'earn'), ('usa',), ('usa',), ('earn',), ('uk',), ('usa',), ('usa',), ('usa',), ('usa', 'earn'), ('uk',), ('usa', 'livestock', 'ec', 'carcass'), ('uk',), ('usa', 'grain', 'corn', 'cbt'), ('usa', 'earn'), ('canada',), ('argentina', 'machinea'), ('crude', 'usa', 'nat-gas', 'gas', 'wpi'), ('usa',), ('usa',), ('usa', 'cotton'), ('usa',), ('earn', 'italy'), ('usa', 'earn'), ('usa', 'acq'), ('usa',), ('earn',), ('usa',), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('brazil', 'ipi'), ('usa', 'earn'), ('usa', 'earn'), ('canada', 'earn'), ('usa', 'grain', 'wheat', 'sudan'), ('usa', 'trade'), ('usa', 'earn'), ('usa', 'money-supply'), ('usa', 'money-supply'), ('crude', 'usa', 'nat-gas', 'gas', 'heat', 'wpi'), ('earn',), ('usa', 'paraguay'), ('usa',), ('usa',), ('usa',), ('usa',), ('earn',), ('usa',), ('usa', 'money-fx'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'earn'), ('canada',), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('spain',), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'earn'), ('usa',), ('usa', 'acq'), ('canada', 'earn'), ('usa',), ('usa', 'acq'), ('brazil',), ('usa', 'ec'), ('canada', 'earn'), ('usa',), ('canada', 'acq'), ('usa', 'nyse'), ('venezuela',), ('usa', 'earn'), ('usa',), ('canada',), ('canada',), ('usa', 'grain', 'corn'), ('canada',), ('usa',), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'earn'), ('canada', 'usa', 'lumber'), ('crude', 'acq', 'venezuela'), ('usa', 'acq'), ('crude', 'ecuador', 'venezuela'), ('crude', 'venezuela'), ('venezuela',), ('usa', 'acq'), ('usa',), ('brazil', 'crude', 'saudi-arabia'), ('usa',), ('brazil', 'crude', 'saudi-arabia'), ('usa', 'earn'), ('usa', 'interest'), ('usa', 'earn'), ('usa',), ('usa',), ('usa', 'mexico'), ('canada', 'usa', 'lumber'), ('ecuador',), ('coffee', 'colombia'), ('usa',), ('brazil', 'canada'), ('ecuador',), ('switzerland', 'rubber'), ('switzerland', 'rubber', 'inro', 'unctad'), ('argentina', 'worldbank'), ('usa', 'acq'), ('veg-oil', 'bangladesh', 'soy-oil'), ('ecuador',), ('spain',), ('cpi', 'ecuador', 'gas'), ('trade', 'sweden'), ('china',), ('iron-steel', 'yugoslavia'), ('france', 'ussr', 'alum'), ('crude', 'france', 'pet-chem', 'yugoslavia'), ('uk', 'japan'), ('indonesia', 'palm-oil', 'veg-oil'), ('uk', 'india', 'iron-steel', 'lead', 'zinc'), ('usa', 'ship', 'iran'), ('yugoslavia',), ('brazil', 'crude', 'ship'), ('usa', 'reagan', 'iran'), ('china',), ('west-germany', 'stoltenberg'), ('usa', 'trade'), ('uk',), ('acq', 'france', 'west-germany', 'ec', 'delors'), ('philippines', 'mnse'), ('iran', 'khomeini'), ('imf', 'kenya', 'camdessus'), ('crude', 'opec'), ('crude', 'opec', 'saudi-arabia', 'hisham-nazer'), ('cocoa', 'icco', 'ivory-coast'), ('usa', 'trade', 'ec', 'veg-oil'), ('saudi-arabia',), ('crude', 'saudi-arabia'), ('france', 'earn'), ('new-zealand',), ('new-zealand',), ('taiwan', 'sugar'), ('usa', 'money-fx'), ('usa', 'acq'), ('ipi', 'ussr'), ('france', 'ecuador'), ('ussr', 'egypt'), ('money-fx', 'reserves', 'peru'), ('saudi-arabia', 'mohammed-ali-abal-khail'), ('usa', 'money-fx', 'taiwan'), ('saudi-arabia',), ('grain', 'corn', 'tanzania'), ('philippines', 'ongpin'), ('taiwan',), ('earn', 'new-zealand'), ('trade', 'australia', 'bop'), ('money-fx', 'worldbank', 'imf', 'zambia'), ('japan', 'ship'), ('cocoa', 'icco', 'ivory-coast'), ('money-fx', 'reserves', 'jordan'), ('cpi', 'new-zealand', 'lange'), ('malaysia', 'rubber'), ('japan', 'ipi', 'inventories'), ('japan',), ('brazil', 'japan'), ('australia',), ('west-germany',), ('uk', 'usa', 'money-fx', 'west-germany'), ('new-zealand', 'douglas'), ('acq', 'australia'), ('money-fx', 'japan', 'yen'), ('west-germany', 'retail'), ('money-fx', 'gnp', 'japan', 'yen'), ('money-supply', 'bangladesh'), ('japan',), ('gold', 'japan'), ('japan', 'earn'), ('uk',), ('uk', 'acq'), ('uk',), ('uk', 'france', 'spain', 'denmark', 'sugar', 'west-germany', 'netherlands', 'ec', 'sweden', 'hungary', 'ireland'), ('switzerland', 'jobs'), ('reserves', 'malaysia'), ('japan',), ('palm-oil', 'veg-oil', 'malaysia'), ('uk', 'earn'), ('trade', 'china'), ('finland',), ('france', 'earn'), ('uk', 'money-fx'), ('hong-kong', 'china'), ('netherlands', 'ase'), ('acq', 'philippines'), ('argentina', 'worldbank'), ('france', 'earn'), ('japan',), ('switzerland',), ('cpi', 'israel'), ('uk', 'money-fx', 'interest'), ('philippines', 'ongpin'), ('acq', 'hong-kong'), ('interest', 'philippines', 'ongpin'), ('trade', 'norway'), ('interest', 'uae'), ('cpi', 'netherlands'), ('luxembourg',), ('ipi', 'sweden'), ('money-fx', 'interest', 'west-germany'), ('usa', 'japan'), ('france', 'ussr', 'alum'), ('crude', 'ecuador', 'opec', 'iraq', 'saudi-arabia', 'cyprus', 'libya', 'turkey'), ('cpi', 'finland'), ('france',), ('usa', 'japan'), ('france',), ('japan',), ('uk', 'earn'), ('money-supply', 'west-germany'), ('hong-kong',), ('money-supply', 'west-germany'), ('uk', 'retail'), ('gold', 'west-germany'), ('uk', 'retail'), ('uk', 'earn'), ('uk', 'ico-coffee', 'ec', 'itc', 'cocoa', 'icco'), ('canada', 'hong-kong'), ('cpi', 'yugoslavia'), ('finland',), ('ussr',), ('philippines',), ('uk', 'earn'), ('philippines',), ('grain', 'rice', 'madagascar'), ('hungary',), ('crude', 'ecuador'), ('uk', 'money-fx'), ('crude', 'usa', 'ecuador'), ('money-fx', 'gnp', 'japan', 'yen'), ('uk', 'acq', 'china'), ('crude', 'opec', 'saudi-arabia', 'hisham-nazer'), ('trade', 'turkey'), ('china',), ('earn', 'switzerland'), ('uk', 'money-fx', 'interest'), ('trade', 'ussr', 'egypt'), ('money-fx', 'reserves', 'peru'), ('usa', 'money-fx', 'taiwan'), ('brazil', 'crude', 'saudi-arabia'), ('uk',), ('earn', 'switzerland'), ('acq',), ('uk', 'trade', 'west-germany', 'belgium', 'ec', 'veg-oil'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'trade'), ('ussr',), ('usa', 'money-fx', 'interest', 'dlr'), ('usa', 'acq'), ('indonesia', 'ship', 'palm-oil', 'veg-oil'), ('usa', 'acq'), ('philippines', 'ongpin'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('uk', 'acq'), ('usa', 'earn'), ('usa',), ('usa',), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'nasdaq'), ('usa',), ('uk',), ('usa', 'earn'), ('usa', 'acq'), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('uk', 'indonesia', 'palm-oil', 'veg-oil'), ('usa', 'earn'), ('usa', 'earn'), ('france', 'cpi'), ('usa',), ('acq',), ('usa', 'earn'), ('usa',), ('gold', 'west-germany'), ('usa',), ('uk',), ('earn',), ('usa', 'earn'), ('earn', 'switzerland'), ('acq',), ('brazil', 'ship'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'hog', 'livestock'), ('coffee', 'usa'), ('usa', 'acq'), ('usa',), ('money-fx', 'grain', 'corn', 'worldbank', 'imf', 'zambia'), ('usa', 'earn'), ('usa', 'acq'), ('uk',), ('canada', 'earn'), ('yugoslavia',), ('money-fx', 'france', 'interest'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa',), ('canada', 'acq'), ('canada', 'acq'), ('usa', 'earn'), ('usa', 'acq'), ('canada',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('canada', 'earn'), ('usa', 'earn'), ('uk', 'money-fx'), ('west-germany',), ('usa', 'grain', 'lyng'), ('usa',), ('canada',), ('usa', 'earn'), ('usa', 'earn'), ('west-germany',), ('usa', 'cme', 'cboe'), ('usa',), ('usa', 'trade', 'west-germany'), ('usa',), ('acq',), ('usa',), ('france', 'cpi'), ('usa', 'trade'), ('usa', 'earn'), ('france', 'cpi'), ('usa', 'acq'), ('uk',), ('usa',), ('uk', 'ec', 'cocoa', 'icco'), ('usa', 'grain', 'wheat'), ('usa',), ('usa', 'earn'), ('switzerland',), ('usa',), ('canada', 'cpu'), ('france', 'cpi'), ('usa', 'earn'), ('usa', 'oilseed', 'netherlands', 'ec', 'veg-oil', 'soybean'), ('jobs', 'sweden'), ('france',), ('money-fx', 'belgium', 'ec'), ('canada',), ('usa', 'acq'), ('usa',), ('acq', 'spain', 'italy'), ('usa', 'amex'), ('usa', 'kuwait', 'livestock'), ('usa',), ('usa', 'earn'), ('usa',), ('usa', 'money-fx', 'interest'), ('usa', 'iran', 'nicaragua'), ('usa',), ('usa', 'earn'), ('usa', 'grain', 'ussr', 'yeutter'), ('usa', 'acq'), ('earn', 'netherlands'), ('usa', 'acq'), ('money-fx', 'spain', 'peseta'), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('denmark',), ('netherlands',), ('usa', 'pet-chem'), ('usa', 'earn'), ('usa', 'earn'), ('france',), ('usa', 'denmark'), ('usa', 'earn'), ('usa',), ('usa',), ('uk', 'earn'), ('usa',), ('usa', 'earn'), ('west-germany',), ('uk',), ('money-fx',), ('acq', 'copper', 'west-germany'), ('canada',), ('usa', 'earn'), ('usa', 'earn'), ('money-fx', 'interest'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'livestock', 'carcass'), ('usa',), ('gnp', 'belgium'), ('usa',), ('usa',), ('uk',), ('usa', 'earn'), ('usa', 'earn'), ('gnp', 'west-germany'), ('usa', 'earn'), ('usa', 'acq'), ('uk', 'usa', 'earn'), ('usa',), ('brazil', 'gnp', 'trade', 'imf'), ('usa',), ('usa', 'cpu'), ('usa', 'earn'), ('france',), ('usa',), ('usa', 'earn'), ('usa', 'acq'), ('usa',), ('usa', 'grain', 'wheat', 'barley', 'corn', 'sorghum', 'cotton'), ('belgium',), ('usa', 'acq'), ('earn', 'sweden'), ('coffee', 'ico-coffee', 'colombia'), ('gnp', 'belgium'), ('canada', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('canada', 'usa', 'trade'), ('usa', 'acq'), ('usa',), ('uk',), ('uk', 'leigh-pemberton'), ('gold', 'south-africa'), ('usa',), ('usa', 'earn'), ('usa',), ('usa', 'cpu'), ('usa',), ('usa', 'livestock', 'carcass'), ('uk', 'canada'), ('usa',), ('cpi', 'balladur'), ('usa', 'cocoa', 'nycsce'), ('canada', 'earn'), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('france', 'trade'), ('uk', 'ship', 'biffex'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa', 'nasdaq'), ('usa', 'acq'), ('usa', 'ec', 'veg-oil', 'yeutter'), ('canada', 'usa', 'trade', 'mulroney'), ('france', 'trade'), ('usa', 'nyse'), ('usa',), ('usa', 'earn'), ('canada',), ('italy',), ('france',), ('uk',), ('usa', 'acq'), ('usa', 'acq'), ('canada', 'usa', 'grain', 'corn', 'gatt'), ('usa',), ('usa', 'acq'), ('usa',), ('usa', 'earn'), ('france', 'cpi', 'balladur'), ('usa',), ('usa', 'earn'), ('canada', 'gold'), ('france',), ('usa', 'earn'), ('uk',), ('usa', 'earn'), ('usa', 'grain', 'wheat', 'oilseed', 'corn', 'soybean'), ('usa', 'earn'), ('usa', 'acq'), ('west-germany',), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('canada', 'earn'), ('usa',), ('usa', 'earn'), ('usa', 'gold'), ('crude', 'trade', 'norway', 'ship', 'south-africa'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa',), ('earn',), ('usa',), ('usa',), ('canada',), ('uk', 'crude', 'ship'), ('denmark', 'bop'), ('usa', 'earn'), ('usa', 'earn'), ('canada',), ('usa', 'gold'), ('canada', 'usa', 'acq'), ('canada',), ('usa', 'trade'), ('usa',), ('usa', 'earn'), ('canada', 'gold'), ('usa', 'earn'), ('usa', 'earn'), ('canada', 'gold'), ('earn',), ('usa',), ('coffee', 'trade', 'ethiopia'), ('earn',), ('earn',), ('usa', 'earn'), ('usa', 'turkey'), ('canada', 'earn'), ('usa', 'earn'), ('usa',), ('usa',), ('usa', 'earn'), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('boesky',), ('usa', 'earn'), ('canada', 'earn'), ('usa',), ('jordan',), ('usa', 'boesky'), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'acq'), ('uk', 'cocoa', 'icco'), ('saudi-arabia',), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('grain', 'wheat', 'corn', 'soybean'), ('usa',), ('usa', 'acq'), ('usa', 'acq', 'italy'), ('usa', 'grain', 'wheat', 'barley', 'oilseed', 'corn', 'sorghum', 'rice', 'cotton', 'soybean'), ('usa', 'grain'), ('usa', 'nyse'), ('usa',), ('usa',), ('usa', 'acq'), ('usa',), ('usa', 'earn'), ('usa', 'nasdaq'), ('usa',), ('usa', 'earn'), ('usa',), ('usa', 'cme', 'cboe'), ('usa',), ('usa', 'earn'), ('usa',), ('brazil', 'usa'), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('crude', 'usa', 'ship', 'fuel'), ('usa',), ('usa', 'earn'), ('usa',), ('acq',), ('usa', 'veg-oil', 'algeria', 'meal-feed'), ('usa', 'grain', 'wheat', 'corn', 'sorghum', 'honduras'), ('usa', 'grain', 'corn'), ('nigeria', 'babangida'), ('usa', 'grain', 'wheat'), ('usa', 'grain', 'barley', 'cyprus'), ('usa', 'acq'), ('usa', 'cme', 'cboe'), ('usa', 'acq'), ('usa', 'earn'), ('usa',), ('usa', 'james-miller'), ('usa', 'earn'), ('usa', 'grain', 'wheat', 'algeria'), ('usa',), ('usa', 'earn'), ('usa',), ('acq',), ('usa',), ('usa', 'earn'), ('usa', 'veg-oil', 'morocco', 'algeria', 'turkey', 'tunisia'), ('usa', 'iraq', 'iran'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'earn'), ('acq',), ('usa', 'acq'), ('usa',), ('usa', 'acq'), ('usa',), ('canada', 'earn'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'acq'), ('usa',), ('usa',), ('usa', 'acq'), ('usa', 'nasdaq'), ('usa', 'earn'), ('canada', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('crude', 'usa', 'fuel'), ('brazil', 'trade'), ('usa',), ('usa', 'acq'), ('usa', 'earn'), ('earn',), ('usa', 'earn'), ('usa', 'acq'), ('usa',), ('brazil', 'trade'), ('uk', 'usa', 'acq', 'nickel', 'strategic-metal'), ('usa', 'earn'), ('usa',), ('usa',), ('west-germany', 'argentina', 'alfonsin', 'von-weizsaecker'), ('icahn',), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'oilseed', 'soybean', 'lyng'), ('costa-rica', 'unctad'), ('usa',), ('usa',), ('usa', 'heat'), ('usa', 'earn'), ('usa', 'acq', 'panama'), ('usa',), ('usa', 'acq', 'icahn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('canada',), ('earn',), ('canada', 'earn'), ('uk', 'usa', 'trade', 'ec'), ('usa',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'earn'), ('usa',), ('brazil', 'canada', 'earn'), ('usa',), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('usa', 'acq'), ('brazil', 'usa'), ('ship', 'new-zealand'), ('usa',), ('usa', 'nasdaq'), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'earn'), ('canada', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa', 'earn'), ('usa',), ('usa',), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'japan', 'trade', 'belgium', 'ec', 'gatt', 'de-clercq'), ('usa',), ('acq',), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'earn'), ('brazil', 'usa', 'argentina', 'james-baker', 'brodersohn'), ('usa',), ('oilseed', 'belgium', 'ec', 'veg-oil'), ('usa', 'acq'), ('usa',), ('australia', 'bop'), ('australia', 'bop'), ('japan', 'miyazawa'), ('australia', 'reserves'), ('japan', 'wpi'), ('japan', 'wpi'), ('japan',), ('west-germany', 'argentina', 'von-weizsaecker'), ('uk', 'west-germany', 'belgium', 'ec', 'morocco', 'algeria', 'egypt', 'syria', 'israel', 'lebanon', 'jordan', 'tunisia'), ('yugoslavia',), ('finland',), ('usa', 'iran', 'nicaragua'), ('india', 'hong-kong', 'italy'), ('japan', 'philippines'), ('usa', 'money-fx', 'japan', 'dlr'), ('money-fx', 'interest', 'trade', 'australia', 'bop', 'austdlr'), ('acq', 'hong-kong'), ('china',), ('money-supply', 'thailand'), ('gnp', 'japan'), ('nicaragua',), ('trade', 'taiwan', 'bop'), ('usa', 'japan', 'trade', 'belgium', 'ec', 'bop', 'de-clercq', 'yeutter'), ('earn', 'hong-kong'), ('copper', 'australia'), ('usa', 'acq', 'new-zealand'), ('india',), ('usa', 'ec', 'veg-oil', 'lyng', 'soy-oil'), ('japan', 'rubber'), ('usa', 'nat-gas'), ('india',), ('japan', 'tse'), ('crude', 'usa'), ('japan', 'money-supply'), ('japan', 'money-supply'), ('malaysia',), ('grain', 'china'), ('south-korea', 'north-korea'), ('syria',), ('gnp', 'japan'), ('gnp', 'japan'), ('gnp', 'japan'), ('australia',), ('gnp', 'japan'), ('usa', 'acq', 'japan'), ('japan',), ('japan', 'south-korea', 'trade', 'gatt'), ('money-fx', 'australia', 'austdlr'), ('japan', 'livestock', 'carcass'), ('switzerland',), ('money-fx', 'interest'), ('japan', 'earn'), ('belgium',), ('taiwan',), ('japan', 'ship'), ('uk', 'money-fx'), ('uk',), ('japan',), ('earn', 'hong-kong'), ('uk',), ('uk',), ('usa', 'japan'), ('grain', 'china'), ('copper', 'south-africa', 'zambia'), ('japan',), ('japan',), ('france', 'cpi', 'oecd'), ('canada',), ('singapore', 'sse'), ('canada', 'oilseed'), ('spain',), ('indonesia', 'sugar'), ('interest', 'money-supply', 'taiwan'), ('luxembourg', 'italy', 'eib'), ('bop',), ('italy', 'wpi'), ('belgium', 'ec'), ('money-fx', 'taiwan', 'reserves'), ('france', 'bop'), ('uk',), ('uk',), ('ipi',), ('uk',), ('grain', 'corn', 'zimbabwe'), ('uk', 'ipi'), ('gnp', 'zimbabwe'), ('usa', 'japan', 'trade'), ('saudi-arabia',), ('crude', 'trade', 'norway', 'ship', 'south-africa'), ('japan',), ('usa', 'acq'), ('uk',), ('canada',), ('yugoslavia',), ('usa', 'money-fx', 'japan', 'dlr'), ('uk',), ('usa', 'worldbank', 'philippines'), ('uk', 'money-fx', 'interest'), ('japan', 'miyazawa'), ('nicaragua',), ('west-germany', 'argentina', 'von-weizsaecker'), ('sweden',), ('crude', 'japan', 'ship', 'iran', 'cyprus'), ('west-germany',), ('netherlands', 'alum', 'suriname'), ('japan', 'housing'), ('netherlands', 'ship'), ('usa', 'iran', 'nicaragua'), ('usa',), ('usa', 'acq'), ('usa', 'amex'), ('usa', 'acq'), ('usa', 'acq'), ('usa',), ('usa',), ('gnp', 'japan'), ('uk', 'cocoa', 'icco'), ('south-africa',), ('usa',), ('usa', 'housing'), ('usa',), ('uk',), ('usa', 'housing'), ('uk', 'japan', 'ecuador', 'norway', 'peru', 'meal-feed', 'chile', 'iceland'), ('usa', 'copper'), ('usa', 'acq'), ('canada',), ('usa',), ('guyana',), ('usa',), ('usa', 'earn'), ('usa', 'japan', 'trade', 'belgium', 'ec', 'de-clercq', 'yeutter'), ('usa', 'livestock', 'l-cattle', 'carcass'), ('usa', 'nyse'), ('usa', 'earn'), ('usa', 'acq'), ('acq', 'france'), ('usa', 'earn'), ('acq', 'france'), ('usa',), ('usa',), ('uk', 'money-fx'), ('usa', 'earn'), ('usa',), ('japan', 'south-korea', 'trade', 'gatt'), ('uk', 'money-fx'), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'earn'), ('canada', 'earn'), ('usa', 'earn'), ('acq',), ('switzerland',), ('west-germany', 'ec'), ('switzerland',), ('usa', 'acq'), ('usa',), ('usa',), ('canada', 'earn'), ('usa',), ('usa',), ('usa', 'earn'), ('canada', 'earn'), ('west-germany',), ('usa', 'hog', 'livestock'), ('denmark', 'schlueter'), ('usa', 'earn'), ('usa', 'earn'), ('canada', 'gold'), ('grain', 'corn', 'taiwan'), ('canada', 'usa', 'acq'), ('usa', 'earn'), ('canada',), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'trade', 'bop'), ('usa',), ('usa', 'trade', 'bop'), ('usa',), ('east-germany',), ('usa', 'james-baker'), ('uk', 'money-fx'), ('usa', 'acq'), ('canada', 'acq'), ('canada',), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'earn'), ('usa',), ('usa', 'saudi-arabia'), ('usa', 'trade', 'netherlands', 'ec'), ('usa', 'acq'), ('usa',), ('switzerland', 'rubber'), ('canada', 'gold'), ('reagan',), ('usa', 'earn'), ('usa', 'nasdaq'), ('uk', 'japan', 'tse'), ('usa', 'reagan', 'iran'), ('usa', 'japan', 'trade', 'oecd'), ('usa', 'earn'), ('james-baker',), ('usa', 'earn'), ('usa', 'earn'), ('usa', 'earn'), ('uk', 'norway'), ('james-baker',), ('usa', 'grain', 'ussr'), ('france', 'trade', 'oecd'), ('usa', 'acq'), ('usa', 'acq'), ('usa', 'earn'), ('usa', 'acq'), ('usa', 'james-baker'), ('usa', 'china'), ('gnp',), ('trade', 'bop', 'lawson'), ('earn',), ('lawson',), ('usa', 'earn'), ('uk', 'gnp', 'lawson'), ('usa', 'acq'), ('usa',), ('usa',)]
        print(len(predictions))
        expected = []
        for row in test_labels:
            label = self.labels_from_prediction(row)
            expected.append(label)
        print(len(expected))
        mlb = preprocessing.MultiLabelBinarizer()
        r = mlb.fit_transform(expected)
        p = mlb.transform(predictions)
        score = 0
        try:
            score = metrics.f1_score(y_true=r, y_pred=p, average='macro')
        except ValueError as ex:
            print("result value is invalid: " + str(ex))
        return score
