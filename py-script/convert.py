import tensorflow as tf

model = tf.keras.models.load_model("model.h5")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

# 🔥 REMOVE this line (important)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]

# compatibility fix
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS
]

converter._experimental_lower_tensor_list_ops = False

tflite_model = converter.convert()

with open("model_fixed.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Compatible model created!")