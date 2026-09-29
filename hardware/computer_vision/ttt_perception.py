import cv2 as cv
import numpy as np

MIN_AREA = 100
MAX_AREA = 2000
BOARD_SIZE = 500

pts_dst = np.float32([[0, 0], [BOARD_SIZE, 0], [0, BOARD_SIZE]])

cell_dim = BOARD_SIZE // 3


def create_center_disk_mask(radius_ratio=0.18):
    mask = np.zeros((cell_dim, cell_dim), dtype=np.uint8)
    center = (cell_dim // 2, cell_dim // 2)
    radius = int(cell_dim * radius_ratio)
    cv.circle(mask, center, radius, 255, -1)  # -1 fills the circle
    return mask

center_disk_mask = create_center_disk_mask(radius_ratio=0.4)
cv.imshow("Center Disk Mask", center_disk_mask)

def classify_cell(cell):
    non_zero_count = cv.countNonZero(cell)
    if non_zero_count < 500:
        return 0

    contours, hierarchy = cv.findContours(cv.bitwise_and(cell, center_disk_mask), \
        cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    
    if hierarchy is None or len(contours) == 0:
        return 0

    has_hole = False
    for h in hierarchy[0]:
        if h[2] != -1:
            has_hole = True
            break

    if has_hole:
        return 2  # O
    else:
        return 1  # X


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
            map[i][j] = classify_cell(cells[i][j])

    return map

def create_corner_mask(shape, corner_w=500, corner_h=500):
    h, w = shape[:2]
    corner_mask = np.zeros((h, w), dtype=np.uint8)

    corner_mask[0:corner_h, 0:corner_w] = 255
    corner_mask[0:corner_h, w - corner_w:w] = 255
    corner_mask[h - corner_h:h, 0:corner_w] = 255
    corner_mask[h - corner_h:h, w - corner_w:w] = 255

    return corner_mask

cap = cv.VideoCapture(1)


while True:
    ret, frame = cap.read()

    frame_copy = frame.copy()

    blurred = cv.GaussianBlur(frame, (5, 5), 0)
    hsv_frame = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 60, 70])
    upper_yellow = np.array([40, 255, 255])

    mask = cv.inRange(hsv_frame, lower_yellow, upper_yellow)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv.erode(mask,kernel,iterations = 1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

    # mask = cv.bitwise_and(mask, create_corner_mask(mask.shape))

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


    yellow_objects = []

    for cnt in contours:
        area = cv.contourArea(cnt)
        x, y, w, h = cv.boundingRect(cnt)

        if area < MIN_AREA or area > MAX_AREA:
            # Outline the rejected contour in Red (thickness=1)
            cv.drawContours(frame_copy, [cnt], -1, (0, 0, 255), 1)
            # Print rejection reason & actual area
            cv.putText(frame_copy, f"Drop: {int(area)}", (x, max(12, y - 4)),
                       cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            continue

        center_x = x + w // 2
        center_y = y + h // 2
        
        yellow_objects.append({
            'centroid': (center_x, center_y),
            'bbox': (x, y, w, h),
            'area': area,
            'contour': cnt
        })

    # Draw the accepted markers
    for idx, obj in enumerate(yellow_objects):
        cnt = obj['contour']
        cx, cy = obj['centroid']
        x, y, w, h = obj['bbox']
        area = obj['area']

        # 1. Draw contour boundary (Green, thickness=2)
        cv.drawContours(frame_copy, [cnt], -1, (0, 255, 0), 2)

        # 2. Draw bounding box (Cyan)
        cv.rectangle(frame_copy, (x, y), (x + w, y + h), (255, 255, 0), 1)

        # 3. Draw center point (Blue dot)
        cv.circle(frame_copy, (cx, cy), 4, (255, 0, 0), -1)

        # 4. Display Marker ID and Area
        cv.putText(frame_copy, f"#{idx + 1} A:{int(area)}", (x, max(15, y - 6)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
    
    if(len(yellow_objects) >= 3):
        frame = frame[10:frame.shape[0]-10, 0:frame.shape[1]-0]
        rows, cols, ch = frame.shape

        pts = np.float32(sort_points(np.array([obj['centroid'] for obj in yellow_objects[:3]])))
        M = cv.getAffineTransform(pts, pts_dst)
        dst = cv.warpAffine(frame, M, (BOARD_SIZE, BOARD_SIZE))

        gray_image = cv.adaptiveThreshold(cv.cvtColor(dst, cv.COLOR_BGR2GRAY), \
        255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv.THRESH_BINARY_INV,11,2)

        kernel = np.ones((2,2),np.uint8)
        gray_image = cv.erode(gray_image,kernel,iterations = 2)

        cv.imshow('Gray', gray_image)

        cells = crop_cells(gray_image)
        map = process_cells(cells)
        print("Parsed Tic-Tac-Toe board:")
        for row in map:
            print(row)
    


    # Debug Feed
    cv.imshow('Contour Debug View', frame_copy)
    cv.imshow('Mask', mask)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()
cv.destroyAllWindows()

# Print parsed object locations
print(f"Total yellow objects found: {len(yellow_objects)}")
for obj in yellow_objects:
    print(f"Object {obj['id']}:Centroid={obj['centroid']}, BBox (x,y,w,h)={obj['bbox']}, Area={obj['area']}")