import PIL.Image
from pdf2image import convert_from_path

# input your file name(with extension)
input_file_name = "UBT-04.pdf"

output_file_name = f"{input_file_name[:-4]}-Paper-Clean.pdf"

# generally left side of the paper is on `Hindi` and right side is on `English`
english_on_right = True  # True = right section of the page contains the English Questions

# no of page(s) to be deleted
delete_page_from_start = 1  # First page is always preserved. second page generally instruction
delete_page_from_end = 2  # if there are extra promotional pages

# opening files
try:
    mark_sheet_image = PIL.Image.open("mark_sheet.png")
except FileNotFoundError:
    print("Error: Mark sheet image not found.")
    exit(1)
old_images = convert_from_path(input_file_name, poppler_path=r'poppler-24.08.0/Library/bin/')

# adding mark sheet to front page
old_images[0].paste(mark_sheet_image, (0, 0), mark_sheet_image)

# final image list with front page, to be converted into pdf
final_image_list = [old_images[0]]

# Eliminate the first  pages/images from old_images
old_images = old_images[delete_page_from_start + 1:- delete_page_from_end]

last_image = None
for index, image in enumerate(old_images):
    print(f"Image Processing: {index + 1}) {image}")
    # for testing purpose, to stop after processing some unit
    # if index == 3:
    #     break

    if not last_image:
        # print("No Previous Image, setting current image.")
        last_image = image  # setting current image to last image
    else:
        print("Previous Image Found, editing and pushing to final image list.")
        width, height = image.size  # width and height of current image

        # top and left/right offset
        top_margin = round(height * 0.0834)
        left_margin = round(width * 0.0514)
        print(top_margin, left_margin)

        if english_on_right:
            # Setting the points for cropped image
            left = (width / 2) * 1.005
            top = top_margin
            right = width - left_margin
            bottom = height

            cropped_image = last_image.crop((left, top, right, bottom))  # cropping the last_image
            image.paste(cropped_image, (left_margin, top_margin))  # overlaying the cropped last_image to current image

            final_image_list.append(image)  # push the edited image to the final image list

        else:
            # Setting the points for cropped image
            left = left_margin
            top = top_margin
            right = width / 2 * 0.995
            bottom = height

            cropped_image = image.crop((left, top, right, bottom))  # cropping the last_image
            # overlaying the cropped last_image to current image
            last_image.paste(cropped_image, (round((width / 2) * 1.005), top_margin))

            final_image_list.append(last_image)  # push the edited image to the final image list
            # last_image.show()

        last_image = None  # empty the last_image variable

# putting the unedited last_image to final list, if any
if last_image:
    print("Unedited Page found(odd page of pdf). putting ,as it is, in final pdf.")
    final_image_list.append(last_image)
    last_image = None

# To see individual images of final list
for index, image in enumerate(final_image_list):
    print(f"Final list :{index+1}) {image}")
    # image.show()

final_image_list[0].save(output_file_name, save_all=True, append_images=final_image_list[1:])
