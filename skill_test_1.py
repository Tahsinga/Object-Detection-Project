import cv2

cap = cv2.VideoCapture(0)
return_status = True

while True:
    ret,frame = cap.read()
    cv2.imshow("DETECT OBJECTS", frame)

    if not ret:
        break

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


    



