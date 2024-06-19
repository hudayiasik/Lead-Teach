import cv2
import numpy as np

def load_templates():
    templates = {}

    # Load card type templates
    card_types = ['up', 'down', 'left', 'right', 'start_loop', 'end_loop', 'dfn_fn', 'call_fn', 'dance', 'music', 'run']
    for card_type in card_types:
        template = cv2.imread(f'templates/color/{card_type}.png', cv2.IMREAD_GRAYSCALE)
        _, template_thresh = cv2.threshold(template, 230, 255, cv2.THRESH_BINARY)
        templates[card_type] = template_thresh
        if template is None :
            print('Error loading images.')
            exit(1)
        

    return templates

def match_template(card_image, templates):
    best_match = None
    max_val = -1

    for name, template in templates.items():
        res = cv2.matchTemplate(card_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val_temp, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val_temp > max_val:
            max_val = max_val_temp
            best_match = name

    return best_match
def process_image(img_data):
    img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    blurred = cv2.GaussianBlur(img, (9, 1), 0)
    edges = cv2.Canny(blurred, 50, 150)
    #cv2.imshow('edges', edges)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Create a copy of the original image to draw contours
    contour_image = img.copy()
    # Load card type templates
    card_templates = load_templates()
    # Iterate over all contours and approximate each one
    card_count = 0  # Counter to keep track of the number of cards
    code_block_list = ""

    for contour in contours:
        # Only consider contours that are large enough to be a card
        if cv2.contourArea(contour) > 500:  # Adjusted threshold
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the contour has four points
            if len(approx) == 4:
                # Get the points in a consistent order
                pts = np.float32([approx[0][0], approx[1][0], approx[2][0], approx[3][0]])

                # Define the destination points for the top-down view
                width, height = 200, 200  # Adjust these values based on card size
                dst_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
                matrix = cv2.getPerspectiveTransform(pts, dst_pts)
                warped = cv2.warpPerspective(img, matrix, (width, height))
                warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                _, warped_thresh = cv2.threshold(warped_gray, 230, 255, cv2.THRESH_BINARY)
                card_type = match_template(warped_thresh, card_templates)
                print(f'Card {card_count + 1}: {card_type}')
                code_block_list += card_type + ","
                card_count += 1
                #cv2.imshow(f'Card {card_count}', warped_thresh)
                cv2.drawContours(contour_image, [approx], -1, (0, 255, 0), 2)
    print(code_block_list)
    return code_block_list,edges


