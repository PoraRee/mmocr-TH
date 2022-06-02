dataset_type = 'OCRDataset'

root = './mmocr/data/trdgTH'
img_prefix = f'{root}/imgs'
train_anno_file1 = f'{root}/label.txt'
test_anno_file1 = f'{root}/test_images/0.jpg'

train=dict(
    type=dataset_type,                  # dataset name
    ann_file=f'{root}/train_images/label.txt',  # Path to annotation file
    img_prefix=f'{root}/train_images',  # Path to images
    loader=dict(
        type='AnnFileLoader',
        # repeat=10,
        parser=dict(
            type='LineStrParser',
            keys=['filename', 'text'],
            keys_idx=[0, 1],
            separator=' ')),
    pipeline=None)

test = dict(
    type=dataset_type,
    img_prefix=img_prefix,
    ann_file=test_anno_file1,
    loader=dict(
        type='AnnFileLoader',
        repeat=1,
        file_format='lmdb',
        file_storage_backend='disk',
        parser=dict(type='LineJsonParser', keys=['filename', 'text'])),
    pipeline=None,
    test_mode=True)


train_list = [train]

test_list = [test]
