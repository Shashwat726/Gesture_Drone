import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    if not ret:
        break


    #Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.putText(gray, "Hello Drone",(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    cv2.imshow("Gray Feed", gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release() 
cv2.destroyAllWindows()