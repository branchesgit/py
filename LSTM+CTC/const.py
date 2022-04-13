DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
num_classes = len(DIGITS) + 1

OUTPUT_SHAPE = (32, 256)

INITIAL_LEARNING_RATE = 1e-3
DECAY_STEPS = 5000
REPORT_STEPS = 100
LEARNING_RATE_DECAY_FACTOR = 0.9

num_hidden = 128
num_layers = 2

num_epochs = 10000
BATCHES = 10
BATCH_SIZE = 32
TRAIN_SIZE = BATCHES * BATCH_SIZE

data_dir = 'tmp/lstm_ctc_data/'
model_dir = 'tmp/lstm_ctc_model/'


REPORT_STEPS