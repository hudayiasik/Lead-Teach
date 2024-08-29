import cv2
import numpy as np

def reorder(point):
    new_points = np.zeros((4, 2), dtype=np.int32)
    point = point.reshape((4, 2))
    add = point.sum(1)
    new_points[0] = point[np.argmin(add)]  # Top-left point
    new_points[2] = point[np.argmax(add)]  # Bottom-right point
    diff = np.diff(point, axis=1)
    new_points[1] = point[np.argmin(diff)]  # Top-right point
    new_points[3] = point[np.argmax(diff)]  # Bottom-left point
    return new_points

def load_templates():
    templates = {}

    # Load card type templates
    #card_types = ['up', 'down', 'left', 'right', 'blue_led', 'red_led', 'green_led','off_led','check','cross','hearth','wait','loop_2','loop_3','loop_4','loop_stop','music_1','music_2','music_3']
    card_types = ['up', 'down', 'left', 'right', 'check','cross','hearth','loop_2','loop_3','loop_4','loop_stop','music_1']
    for card_type in card_types:
        template = cv2.imread(f'templates/correct_blocks/{card_type}.jpg', cv2.IMREAD_GRAYSCALE)
        #_, template_thresh = cv2.threshold(template, 100, 350, cv2.THRESH_BINARY)
        #show images
        
        templates[card_type] = template
        if template is None:
            print('Error loading images.')
            exit(1)

    return templates

def match_template(card_image, templates):

    best_match = None
    for name, template in templates.items():
        gray_warped = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray_warped, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        #print(f'{name}: {max_val}')
        if max_val > 0.6:  # Adjust the threshold as needed
            best_match = name
            print(f'{name}: {max_val}')
            break
    return best_match

def process_image(img_data):
    img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_inverted = cv2.bitwise_not(gray)
    _, binary = cv2.threshold(gray_inverted, 125, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = [c for c in contours if cv2.contourArea(c) > 10000]

    corners = []
    for contour in final_contours:
        epsilon = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # Only consider quadrilateral contours
            corners.append(approx)

    width, height = 150, 150
    dst_points = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype=np.float32)

    warped_images = []
    image_copy = img.copy()
    card_templates = load_templates()
    code_block_list = ""
    card_count = 0

    for corner in corners:
        reordered_corners = reorder(corner)
        M = cv2.getPerspectiveTransform(reordered_corners.astype(np.float32), dst_points)
        warped_image = cv2.warpPerspective(image_copy, M, (width, height))
        warped_images.append(warped_image)

        image_copy = cv2.drawContours(image_copy, [corner], -1, (0, 0, 255), 2)

    for warped_image in warped_images:      
        cv2.imshow('warped', warped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        result = match_template(warped_image, card_templates)
        if result:
            code_block_list += result + ","
            card_count += 1

    print(f'Cards found: {card_count}')
    print(f'Results: {code_block_list}')

    return code_block_list, image_copy






    
    
img_data = open('./temp.jpg', 'rb').read()
list,contour_img = process_image(img_data)