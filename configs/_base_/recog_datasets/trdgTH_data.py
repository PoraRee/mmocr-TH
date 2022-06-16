dataset_type = 'OCRDataset'

root = './mmocr/data/trdgTH'
img_prefix = f'{root}/imgs'
train_anno_file1 = f'{root}/train_images'
train_anno_file2 = f'{root}/train_images_2'
train_anno_file3 = f'{root}/google_ocr_train_images'
test_anno_file1 = f'{root}/test_images'
test_anno_file2 = f'{root}/google_ocr_test_images'


train1 = dict(
    type=dataset_type,
    ann_file=f'{train_anno_file1}/label.txt',
    img_prefix=train_anno_file1,
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineJsonParser',
            keys=['filename', 'text'],
        )),
    pipeline=None)
train2 = dict(
    type=dataset_type,
    ann_file=f'{train_anno_file2}/label.txt',
    img_prefix=train_anno_file2,
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineJsonParser',
            keys=['filename', 'text'],
        )),
    pipeline=None)
train3 = dict(
    type=dataset_type,
    ann_file=f'{train_anno_file3}/label.txt',
    img_prefix=train_anno_file3,
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineJsonParser',
            keys=['filename', 'text'],
        )),
    pipeline=None)

test1 = dict(
    type=dataset_type,
    ann_file=f'{test_anno_file1}/label.txt',
    img_prefix=f'{test_anno_file1}',
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineStrParser',
            keys=['filename', 'text'],
            keys_idx=[0, 1],
            separator=' ')),
    pipeline=None,
    test_mode=True)
test2 = dict(
    type=dataset_type,
    ann_file=f'{test_anno_file2}/label.txt',
    img_prefix=f'{test_anno_file2}',
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineJsonParser',
            keys=['filename', 'text'],
        )),
    pipeline=None,
    test_mode=True)


train_list = [train1, train2, train3]

test_list = [test1, test2]
