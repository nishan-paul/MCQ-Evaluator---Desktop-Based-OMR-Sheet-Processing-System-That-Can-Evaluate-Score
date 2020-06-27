import cv2
import imutils
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform
from developer_functions_1 import *


def mcq_evaluate(m, path, level, roll, subject):
    records = select('result', level, subject, roll)
    n = len(records)
    if n == 0: insert(level, subject, roll)

    ANSWER_KEY = get_solution(level, subject, roll)

    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                docCnt = approx
                break

    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    # cv2.imshow("binary_image", thresh)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 20 and h >= 20 and 0.9 <= ar <= 1.1:
            questionCnts.append(c)

    questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
    correct = 0
    index = 0

    for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
        cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
        bubbled = None

        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if bubbled is None or total > bubbled[0]: bubbled = (total, j)

        color = (0, 0, 255)

        key = m[index]
        value = bubbled[1]
        ans = ANSWER_KEY[q]

        update(key, value, level, subject, roll)

        if ans == value:
            color = (0, 255, 0)
            correct += 1

        cv2.drawContours(paper, [cnts[ans]], -1, color, 3)
        index = index + 1

    update('number', correct, level, subject, roll)

    cv2.putText(paper, "{:d}".format(correct), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    paper_name = level + '_' + roll + '_' + subject + '.jpg'
    cv2.imshow(paper_name, paper)

    location = level + '/RESULT/' + paper_name
    cv2.imwrite(location, paper)
    cv2.waitKey(0)


