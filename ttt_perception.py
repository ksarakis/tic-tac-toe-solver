import cv2 as cv
import numpy as np

MIN_AREA = 50
MAX_AREA = 200
BOARD_SIZE = 500

pts_dst = np.float32([[0, 0], [BOARD_SIZE, 0], [0, BOARD_SIZE]])

def sort_points(pts):
    # Sort points in Top-Left, Top-Right, Bottom-Left order 
    # like QR code corners to ensure correct affine transformation

    d1 = np.linalg.norm(pts[0] - pts[1])**2
    d2 = np.linalg.norm(pts[0] - pts[2])**2
    d3 = np.linalg.norm(pts[1] - pts[2])**2

    if d1 > d2 and d1 > d3:
        c, a, b =  [pts[2], pts[1], pts[0]]
    elif d2 > d1 and d2 > d3:
        c, a, b =  [pts[1], pts[2], pts[0]]
    else:   
        c, a, b =  [pts[0], pts[2], pts[1]]

    v1 = a - c
    v2 = b - c

    if v1[0] * v2[1] - v1[1] * v2[0] > 0:
        return [c, a, b]
    else:
        return [c, b, a]

def crop_cells(gray_image):
    cells = [[None for _ in range(3)] for _ in range(3)]
    cell_size = BOARD_SIZE // 3
    for i in range(3):
        for j in range(3):
            x = j * cell_size
            y = i * cell_size
            cell = gray_image[y:y + cell_size, x:x + cell_size]
            cells[i][j] = cell
            cv.imshow(f'Cell ({i}, {j})', cell)
    return cells

def process_cells(cells):
    map = np.zeros((3, 3), dtype=int) # 0 for empty, 1 for X, 2 for O
    for i in range(3):
        for j in range(3):
            cell = cells[i][j]
            non_zero_count = cv.countNonZero(cell)
            print(f"Cell ({i}, {j}) non-zero pixel count: {non_zero_count}")
            if non_zero_count < 500:  # Threshold for detecting a mark
                map[i][j] = 0  # Empty
            else:
                circle = cv.HoughCircles(
                    cell,
                    cv.HOUGH_GRADIENT,
                    dp=1.2,
                    minDist=35,
                    param1=50,
                    param2=20,
                    minRadius=40,
                    maxRadius=100
                )
                if circle is not None:
                    map[i][j] = 2  # O
                else:
                    map[i][j] = 1  # X

    return map

cap = cv.VideoCapture(1)


while True:
    ret, frame = cap.read()

    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 60, 70])
    upper_yellow = np.array([40, 255, 255])

    mask = cv.inRange(hsv_frame, lower_yellow, upper_yellow)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask,kernel,iterations = 1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    frame_copy = frame.copy()

    yellow_objects = []

    for idx, cnt in enumerate(contours):
        area = cv.contourArea(cnt)
        if area < MIN_AREA or area > MAX_AREA:
            continue

        x, y, w, h = cv.boundingRect(cnt)
        center_x = x + w // 2
        center_y = y + h // 2

        yellow_objects.append({
            'id': len(yellow_objects) + 1,
            'centroid': (center_x, center_y),
            'bbox': (x, y, w, h),
            'area': area
        })

        print(f"Object {idx + 1}: Centroid=({center_x}, {center_y}), BBox (x,y,w,h)=({x},{y},{w},{h}), Area={area}")


        cv.circle(frame_copy, (center_x, center_y), 4, (0, 0, 255), -1)
        label = f"#{len(yellow_objects) + 1} ({center_x},{center_y})"

        frame_copy = cv.putText(frame_copy, label, (x, max(15, y - 8)),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if(len(yellow_objects) >= 3):
        frame = frame[10:frame.shape[0]-10, 0:frame.shape[1]-0]
        rows, cols, ch = frame.shape

        pts = np.float32(sort_points(np.array([obj['centroid'] for obj in yellow_objects[:3]])))
        M = cv.getAffineTransform(pts, pts_dst)
        dst = cv.warpAffine(frame, M, (BOARD_SIZE, BOARD_SIZE))

        gray_image = cv.adaptiveThreshold(cv.cvtColor(dst, cv.COLOR_BGR2GRAY), \
        255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv.THRESH_BINARY_INV,11,2)

        cv.imshow('Frame', frame)
        cv.imshow('Frame Copy', frame_copy)
        cv.imshow('Mask', mask)
        cv.imshow('Transformed', dst)
        cv.imshow('Gray', gray_image)

        cells = crop_cells(gray_image)
        map = process_cells(cells)
        print("Parsed Tic-Tac-Toe board:")
        for row in map:
            print(row)
    else:
        cv.imshow('Frame', frame)
        cv.imshow('Mask', mask)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()
cv.destroyAllWindows()

# Print parsed object locations
print(f"Total yellow objects found: {len(yellow_objects)}")
for obj in yellow_objects:
    print(f"Object {obj['id']}:Centroid={obj['centroid']}, BBox (x,y,w,h)={obj['bbox']}, Area={obj['area']}")