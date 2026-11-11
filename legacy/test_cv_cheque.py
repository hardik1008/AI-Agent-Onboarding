import cv2
import numpy as np

# Test cheque generation and analysis
w, h = 800, 360
cheque_img = np.ones((h, w, 3), dtype=np.uint8) * 245

# Draw bank header
cv2.putText(cheque_img, "HDFC BANK LTD. - FORT BRANCH", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2)
cv2.putText(cheque_img, "IFSC: HDFC0000060", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (60, 60, 60), 1)

# Draw Payee line
cv2.putText(cheque_img, "PAY: ROHIT RAMESH SHARMA", (40, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (10, 10, 10), 1)

# Draw Account Box
cv2.rectangle(cheque_img, (40, 180), (320, 220), (50, 50, 50), 1)
cv2.putText(cheque_img, "A/C: 50100492817492", (50, 208), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 2)

# Draw MICR Band zone at bottom
cv2.rectangle(cheque_img, (0, h - 60), (w, h), (255, 255, 255), -1)
cv2.line(cheque_img, (0, h - 60), (w, h - 60), (180, 180, 180), 1)
micr_text = "c 000124 c 400240015 d 50100492817492 c 29"
cv2.putText(cheque_img, micr_text, (80, h - 22), cv2.FONT_HERSHEY_DUPLEX, 0.65, (0, 0, 0), 2)

# Encode to bytes and analyze
ret, buf = cv2.imencode('.jpg', cheque_img)
gray = cv2.cvtColor(cheque_img, cv2.COLOR_BGR2GRAY)
lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
print("Generated Cheque Image Bytes:", len(buf))
print("Cheque Sharpness Variance:", lap_var)
print("CTS-2010 Aspect Ratio:", round(w/h, 2))
