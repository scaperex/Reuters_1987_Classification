import pickle


def unpickle(file):
	with open(file, 'rb') as f:
		data = pickle.load(f, encoding='bytes')
	return data