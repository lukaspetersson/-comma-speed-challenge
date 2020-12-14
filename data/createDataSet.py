import tensorflow as tf

inFile = open("train-grouped.txt", "r")
filenames = []
lables = []
for i, v in enumerate(inFile):
	filenames.append(str(i)+".jpg")
	lables.append(v)

filenames = tf.constant(filenames)
labels = tf.constant(lables)

dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))

def _parse_function(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string, channels=3)
    image = tf.cast(image_decoded, tf.float32)
    return image, label

dataset = dataset.map(_parse_function)
dataset = dataset.batch(3)

iterator = dataset.make_one_shot_iterator()
images, labels = iterator.get_next()
