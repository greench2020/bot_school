from PIL import Image, ImageDraw, ImageFont
import os

def generating_head_report(list_reports, user_id):
    list_numeric = []
    mark_pos = (983, 350)
    im = Image.open('BotData\Pics\head_half_year.png')
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype("arialbd.ttf", 30)
    subject = list_reports[1]['subject']

    if len(subject) > 57:
        point = subject[:58].rfind(' ')
        subject = subject[:58][:point] + '\n' + subject[point + 1:]
        pos = (12, 330)
    else:
        pos = (15, 350)

    draw_text.text(pos, subject, fill='black', font=font)
    for keys in list_reports[1].keys():
        if keys.isnumeric() or keys.isalnum():
            list_numeric.append(f'{keys}, {list_reports[1][keys]}')
            draw_text.text(mark_pos, list_reports[1][keys], fill='black', font=font)
            mark_pos = (mark_pos[0] + 66, mark_pos[1])
    return generating_body_report(im, user_id, list_reports)


def generating_body_report(im, user_id, list_reports):
    for i in range(len(list_reports[1:])):

        # Base Data
        mark_pos = (917, 38)
        im2 = Image.open('BotData\Pics\pattern.png')
        draw_text = ImageDraw.Draw(im2)
        font = ImageFont.truetype("arialbd.ttf", 30)
        subject = list_reports[i]['subject']

        # Detection len subject and getting position
        if len(subject) > 54:
            point = subject[:55].rfind(' ')
            subject = subject[:55][:point] + '\n' + subject[point + 1:]
            pos = (15, 24)
        else:
            pos = (15, 35)

        # Drawing subject and detecting and drwwing marks
        draw_text.text(pos, subject, fill='black', font=font)
        for keys in list_reports[i].keys():
            if keys.isnumeric() or keys.isalnum():
                if len(list_reports[i][keys]) == 1:
                    mark_pos = (mark_pos[0] + 66, mark_pos[1])
                else:
                    mark_pos = (mark_pos[0] + 57, mark_pos[1])
                draw_text.text(mark_pos, list_reports[i][keys], fill='black', font=font)

        # Creating new image
        w_1, h_1 = im.size
        w_2, h_2 = im2.size
        new_im = Image.new('RGB', (w_1, h_1 + h_2), 'white')
        new_im.paste(im, (0, 0))
        new_im.paste(im2, (0, h_1))
        im = new_im

    # Saving final image as .png
    new_im.save(f'{os.getcwd()}\BotData\Pics\{user_id}.png')

    # Return path to image
    return f'{os.getcwd()}\BotData\Pics\{user_id}.png'


def create_report(report, user_id):
    list_pre_report = []
    for subject in report['subjects'].keys():
        each_lesson = {'5': report['subjects'][subject]['5'], '4': report['subjects'][subject]['4'],
                       '3': report['subjects'][subject]['3'], '2': report['subjects'][subject]['2'],
                       'average': report['subjects'][subject]['average'], 'term': report['subjects'][subject]['term'],
                       'subject': subject}
        list_pre_report.append(each_lesson)
    return generating_head_report(list_pre_report, user_id)
