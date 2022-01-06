with open('/home/daftvm/workspace/mast1_ai/deep_learning/yolo/training/data/train.txt', 'r') as train:
    ids = train.readlines()

print('Total ids:', len(ids))

threshold = round(len(ids) * 0.7)
train_ids = ids[:threshold]
val_ids = ids[threshold:]

with open('/home/daftvm/workspace/mast1_ai/deep_learning/yolo/training/data/train.txt', 'w') as train:
    for l in train_ids:
        train.write('/darknet/data/obj/' + l[:-1] + '.jpg\n')

with open('/home/daftvm/workspace/mast1_ai/deep_learning/yolo/training/data/val.txt', 'w') as val:
    for l in val_ids:
        val.write('/darknet/data/obj/' + l[:1] + '.jpg\n')

print('Train ids:', len(train_ids))
print('Val ids:', len(val_ids))