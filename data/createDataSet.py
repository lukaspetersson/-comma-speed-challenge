import tensorflow as tf

# Create arrays with filenames and lables
inFile = open("train-grouped.txt", "r")
filenames = []
lables = []
for i, v in enumerate(inFile):
	filenames.append(str(i)+".jpg")
	lables.append(v)

filenames = tf.constant(filenames)
labels = tf.constant(lables)

#create Dataset
dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))

# load images
def im_file_to_tensor(file, label):
    def _im_file_to_tensor(file, label):
        path = f"./frames/{file.numpy().decode()}"
        im = tf.image.decode_jpeg(tf.io.read_file(path), channels=3)
        im = tf.cast(image_decoded, tf.float32) / 255.0
        return im, label
    return tf.py_function(_im_file_to_tensor,
                          inp=(file, label),
                          Tout=(tf.float32, tf.uint8))

dataset = dataset.map(im_file_to_tensor)

# include?
#dataset.shuffle()

#split dataset
train_ds_size = int(0.7 * len(lables))
valid_ds_size = int(0.15 * len(lables))

train_dataset = dataset.take(train_ds_size)
remaining = dataset.skip(train_ds_size)
valid_dataset = remaining.take(valid_ds_size)
test_dataset = remaining.skip(valid_ds_size)
