import cv2
import joblib as joblib
from extract_features import extract_features
import pickle
import numpy as np


def nothing(x):
    pass



svm = pickle.load(open('svm_model_7.sav', 'rb'))
scaler = joblib.load('scaler_7.gz')
encoder = joblib.load('encoder_7.gz')
if __name__ == '__main__':
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('video_test.avi')

    out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (256, 256))

    while True:
        # Capture frame-by-frame

        #hmin = cv2.getTrackbarPos('HMin', 'tunning')
        #smin = cv2.getTrackbarPos('SMin', 'tunning')
        #vmin = cv2.getTrackbarPos('VMin', 'tunning')
        #hmax = cv2.getTrackbarPos('HMax', 'tunning')
        #smax = cv2.getTrackbarPos('SMax', 'tunning')
        #vmax = cv2.getTrackbarPos('VMax', 'tunning')
        hmin = 0
        smin =0
        vmin = 0
        hmax = 50
        smax = 70
        vmax = 255

        ret, frame = cap.read()
        ## TEST
        if ret == True:

            img,cnt, p, s,d,a = extract_features(frame, 0, 0, 0, 50, 70, 255)

            X = scaler.transform(np.array([cnt, p, s,d,a]).reshape(1,-1))

            res = svm.predict(X)
            res_decoded = encoder.inverse_transform(res)[0]
            cv2.putText(img, str(res_decoded), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('result', img)

            out.write(img)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        else:
            break


    # When everything done, release the capture
    cap.release()

    out.release()
    cv2.destroyAllWindows()
