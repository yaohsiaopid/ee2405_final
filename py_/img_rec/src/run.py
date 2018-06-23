
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2
from keras.models import load_model
from scipy.misc import imresize

label = {0: 'neg', 1: 'pos'}
# If you train multiple classes, you may change the index to your label.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Load the trained model and run.')
    parser.add_argument("--model_path", required=True,
                        help="The path to the model file.", type=str)
    parser.add_argument("--target_img_size", required=True, nargs='*',
                        help="The target image size to the model.", type=int)
    args = parser.parse_args()

    if len(args.target_img_size) != 2:
        raise Exception('length of traget_img_size should be 2')

    cap = cv2.VideoCapture(0)
    model = load_model(args.model_path)

    for _ in range(10):
        ret, frame = cap.read()
        frame_resize = imresize(frame, tuple(args.target_img_size))
        # [possibility_neg, possibility_pos]
        ans = model.predict(np.expand_dims(frame_resize, axis=0))
        ans = ans.argmax(axis=-1)
        print(label[ans[0]])
        cv2.imwrite('a.jpg', frame)


