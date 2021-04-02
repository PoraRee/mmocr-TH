import math
import warnings

import cv2
import mmcv
import numpy as np
from matplotlib import pyplot as plt

import mmocr.utils as utils


def overlay_mask_img(img, mask):
    """Draw mask boundaries on image for visualization.

    Args:
        img (ndarray): The input image.
        mask (ndarray): The instance mask.

    Returns:
        img (ndarray): The output image with instance boundaries on it.
    """
    assert isinstance(img, np.ndarray)
    assert isinstance(mask, np.ndarray)

    contours, _ = cv2.findContours(
        mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

    return img


def show_feature(features, names, to_uint8, out_file=None):
    """Visualize a list of feature maps.

    Args:
        features (list(ndarray)): The feature map list.
        names (list(str)): The visualized title list.
        to_uint8 (list(1|0)): The list indicating whether to convent
            feature maps to uint8.
        out_file (str): The output file name. If set to None,
            the output image will be shown without saving.
    """
    assert utils.is_ndarray_list(features)
    assert utils.is_type_list(names, str)
    assert utils.is_type_list(to_uint8, int)
    assert utils.is_none_or_type(out_file, str)
    assert utils.equal_len(features, names, to_uint8)

    num = len(features)
    row = col = math.ceil(math.sqrt(num))

    for i, (f, n) in enumerate(zip(features, names)):
        plt.subplot(row, col, i + 1)
        plt.title(n)
        if to_uint8[i]:
            f = f.astype(np.uint8)
        plt.imshow(f)
    if out_file is None:
        plt.show()
    else:
        plt.savefig(out_file)


def show_img_boundary(img, boundary):
    """Show image and instance boundaires.

    Args:
        img (ndarray): The input image.
        boundary (list[float or int]): The input boundary.
    """
    assert isinstance(img, np.ndarray)
    assert utils.is_type_list(boundary, int) or utils.is_type_list(
        boundary, float)

    cv2.polylines(
        img, [np.array(boundary).astype(np.int32).reshape(-1, 1, 2)],
        True,
        color=(0, 255, 0),
        thickness=1)
    plt.imshow(img)
    plt.show()


def show_pred_gt(preds,
                 gts,
                 show=False,
                 win_name='',
                 wait_time=0,
                 out_file=None):
    """Show detection and ground truth for one image.

    Args:
        preds (list[list[float]]): The detection boundary list.
        gts (list[list[float]]): The ground truth boundary list.
        show (bool): Whether to show the image.
        win_name (str): The window name.
        wait_time (int): The value of waitKey param.
        out_file (str): The filename of the output.
    """
    assert utils.is_2dlist(preds)
    assert utils.is_2dlist(gts)
    assert isinstance(show, bool)
    assert isinstance(win_name, str)
    assert isinstance(wait_time, int)
    assert utils.is_none_or_type(out_file, str)

    p_xy = [p for boundary in preds for p in boundary]
    gt_xy = [g for gt in gts for g in gt]

    max_xy = np.max(np.array(p_xy + gt_xy).reshape(-1, 2), axis=0)

    width = int(max_xy[0]) + 100
    height = int(max_xy[1]) + 100

    img = np.ones((height, width, 3), np.int8) * 255
    pred_color = mmcv.color_val('red')
    gt_color = mmcv.color_val('blue')
    thickness = 1

    for boundary in preds:
        cv2.polylines(
            img, [np.array(boundary).astype(np.int32).reshape(-1, 1, 2)],
            True,
            color=pred_color,
            thickness=thickness)
    for gt in gts:
        cv2.polylines(
            img, [np.array(gt).astype(np.int32).reshape(-1, 1, 2)],
            True,
            color=gt_color,
            thickness=thickness)
    if show:
        mmcv.imshow(img, win_name, wait_time)
    if out_file is not None:
        mmcv.imwrite(img, out_file)

    return img


def imshow_pred_boundary(img,
                         boundaries_with_scores,
                         labels,
                         score_thr=0,
                         boundary_color='blue',
                         text_color='blue',
                         thickness=1,
                         font_scale=0.5,
                         show=True,
                         win_name='',
                         wait_time=0,
                         out_file=None,
                         show_score=False):
    """Draw boundaries and class labels (with scores) on an image.

    Args:
        img (str or ndarray): The image to be displayed.
        boundaries_with_scores (list[list[float]]): Boundaries with scores.
        labels (list[int]): Labels of boundaries.
        score_thr (float): Minimum score of boundaries to be shown.
        boundary_color (str or tuple or :obj:`Color`): Color of boundaries.
        text_color (str or tuple or :obj:`Color`): Color of texts.
        thickness (int): Thickness of lines.
        font_scale (float): Font scales of texts.
        show (bool): Whether to show the image.
        win_name (str): The window name.
        wait_time (int): Value of waitKey param.
        out_file (str or None): The filename of the output.
        show_score (bool): Whether to show text instance score.
    """
    assert isinstance(img, (str, np.ndarray))
    assert utils.is_2dlist(boundaries_with_scores)
    assert utils.is_type_list(labels, int)
    assert utils.equal_len(boundaries_with_scores, labels)
    if len(boundaries_with_scores) == 0:
        warnings.warn('0 text found in ' + out_file)
        return

    utils.valid_boundary(boundaries_with_scores[0])
    img = mmcv.imread(img)

    scores = np.array([b[-1] for b in boundaries_with_scores])
    inds = scores > score_thr
    boundaries = [boundaries_with_scores[i][:-1] for i in np.where(inds)[0]]
    scores = [scores[i] for i in np.where(inds)[0]]
    labels = [labels[i] for i in np.where(inds)[0]]

    boundary_color = mmcv.color_val(boundary_color)
    text_color = mmcv.color_val(text_color)
    font_scale = 0.5

    for boundary, score, label in zip(boundaries, scores, labels):
        boundary_int = np.array(boundary).astype(np.int32)

        cv2.polylines(
            img, [boundary_int.reshape(-1, 1, 2)],
            True,
            color=boundary_color,
            thickness=thickness)

        if show_score:
            label_text = f'{score:.02f}'
            cv2.putText(img, label_text,
                        (boundary_int[0], boundary_int[1] - 2),
                        cv2.FONT_HERSHEY_COMPLEX, font_scale, text_color)
    if show:
        mmcv.imshow(img, win_name, wait_time)
    if out_file is not None:
        mmcv.imwrite(img, out_file)

    return img


def imshow_text_char_boundary(img,
                              text_quads,
                              boundaries,
                              char_quads,
                              chars,
                              show=False,
                              thickness=1,
                              font_scale=0.5,
                              win_name='',
                              wait_time=-1,
                              out_file=None):
    """Draw text boxes and char boxes on img.

    Args:
        img (str or ndarray): The img to be displayed.
        text_quads (list[list[int|float]]): The text boxes.
        boundaries (list[list[int|float]]): The boundary list.
        char_quads (list[list[list[int|float]]]): A 2d list of char boxes.
            char_quads[i] is for the ith text, and char_quads[i][j] is the jth
            char of the ith text.
        chars (list[list[char]]). The string for each text box.
        thickness (int): Thickness of lines.
        font_scale (float): Font scales of texts.
        show (bool): Whether to show the image.
        win_name (str): The window name.
        wait_time (int): Value of waitKey param.
        out_file (str or None): The filename of the output.
    """
    assert isinstance(img, (np.ndarray, str))
    assert utils.is_2dlist(text_quads)
    assert utils.is_2dlist(boundaries)
    assert utils.is_3dlist(char_quads)
    assert utils.is_2dlist(chars)
    assert utils.equal_len(text_quads, char_quads, boundaries)

    img = mmcv.imread(img)
    char_color = [mmcv.color_val('blue'), mmcv.color_val('green')]
    text_color = mmcv.color_val('red')
    text_inx = 0
    for text_box, boundary, char_box, txt in zip(text_quads, boundaries,
                                                 char_quads, chars):
        text_box = np.array(text_box)
        boundary = np.array(boundary)

        text_box = text_box.reshape(-1, 2).astype(np.int32)
        cv2.polylines(
            img, [text_box.reshape(-1, 1, 2)],
            True,
            color=text_color,
            thickness=thickness)
        if boundary.shape[0] > 0:
            cv2.polylines(
                img, [boundary.reshape(-1, 1, 2)],
                True,
                color=text_color,
                thickness=thickness)

        for b in char_box:
            b = np.array(b)
            c = char_color[text_inx % 2]
            b = b.astype(np.int32)
            cv2.polylines(
                img, [b.reshape(-1, 1, 2)], True, color=c, thickness=thickness)

        label_text = ''.join(txt)
        cv2.putText(img, label_text, (text_box[0, 0], text_box[0, 1] - 2),
                    cv2.FONT_HERSHEY_COMPLEX, font_scale, text_color)
        text_inx = text_inx + 1

    if show:
        mmcv.imshow(img, win_name, wait_time)
    if out_file is not None:
        mmcv.imwrite(img, out_file)

    return img


def tile_image(images):
    """Combined multiple images to one vertically.

    Args:
        images (list[np.ndarray]): Images to be combined.
    """
    assert isinstance(images, list)
    assert len(images) > 0

    for i, _ in enumerate(images):
        if len(images[i].shape) == 2:
            images[i] = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)

    widths = [img.shape[1] for img in images]
    heights = [img.shape[0] for img in images]
    h, w = sum(heights), max(widths)
    vis_img = np.zeros((h, w, 3), dtype=np.uint8)

    offset_y = 0
    for image in images:
        img_h, img_w = image.shape[:2]
        vis_img[offset_y:(offset_y + img_h), 0:img_w, :] = image
        offset_y += img_h

    return vis_img


def imshow_text_label(img,
                      pred_label,
                      gt_label,
                      show=False,
                      win_name='',
                      wait_time=-1,
                      out_file=None):
    """Draw predicted texts and ground truth texts on images.

    Args:
        img (str or np.ndarray): Image filename or loaded image.
        pred_label (str): Predicted texts.
        gt_label (str): Ground truth texts.
        show (bool): Whether to show the image.
        win_name (str): The window name.
        wait_time (int): Value of waitKey param.
        out_file (str): The filename of the output.
    """
    assert isinstance(img, (np.ndarray, str))
    assert isinstance(pred_label, str)
    assert isinstance(gt_label, str)
    assert isinstance(show, bool)
    assert isinstance(win_name, str)
    assert isinstance(wait_time, int)

    img = mmcv.imread(img)

    src_h, src_w = img.shape[:2]
    resize_height = 64
    resize_width = int(1.0 * src_w / src_h * resize_height)
    img = cv2.resize(img, (resize_width, resize_height))
    h, w = img.shape[:2]
    pred_img = np.ones((h, w, 3), dtype=np.uint8) * 255
    gt_img = np.ones((h, w, 3), dtype=np.uint8) * 255

    cv2.putText(pred_img, pred_label, (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (0, 0, 255), 2)
    images = [pred_img, img]

    if gt_label != '':
        cv2.putText(gt_img, gt_label, (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 0, 0), 2)
        images.append(gt_img)

    img = tile_image(images)

    if show:
        mmcv.imshow(img, win_name, wait_time)
    if out_file is not None:
        mmcv.imwrite(img, out_file)

    return img
