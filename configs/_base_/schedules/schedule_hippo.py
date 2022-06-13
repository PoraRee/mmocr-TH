# optimizer
optimizer = dict(type='Adam', lr=0.001 / 8)
optimizer_config = dict(grad_clip=None)
# learning policy
lr_config = dict(
    policy='step',
    warmup=None,
    step=[11])
runner = dict(type='EpochBasedRunner', max_epochs=12)
checkpoint_config = dict(interval=1)
