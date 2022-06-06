dataset_type = 'OCRDataset'

root = './mmocr/data/trdgTH'
img_prefix = f'{root}/imgs'
train_anno_file1 = f'{root}/label.txt'
test_anno_file1 = f'{root}/test_images/0.jpg'

train = dict(
    type=dataset_type,
    ann_file=f'{root}/train_images/label.txt',
    img_prefix=f'{root}/train_images',
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineStrParser',
            keys=['filename', 'text'],
            keys_idx=[0, 1],
            separator=' ')),
    pipeline=None)

test = dict(
    type=dataset_type,
    ann_file=f'{root}/test_images/label.txt',
    img_prefix=f'{root}/test_images',
    loader=dict(
        type='AnnFileLoader',
        parser=dict(
            type='LineStrParser',
            keys=['filename', 'text'],
            keys_idx=[0, 1],
            separator=' ')),
    pipeline=None,
    test_mode=True)


train_list = [train]

test_list = [test]
