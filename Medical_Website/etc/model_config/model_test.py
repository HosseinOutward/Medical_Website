import argparse
# import yaml
# import torch
# from albumentations.augmentations import transforms
# from albumentations import pytorch
# from albumentations.core.composition import Compose
# from albumentations.augmentations.geometric.resize import Resize
# import importlib
# import torch.nn as nn
import cv2
import os
import numpy as np
import time

parser = argparse.ArgumentParser()
# device = torch.device("cpu")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default=None, help='model name')
    parser.add_argument('--image_dir', default="4002362_Rashidi_luna_1.png", help='image dirctory')
    args = parser.parse_args()

    return args


def image_loader(image, test_transforms):
    image = test_transforms(image=image)
    image = image['image'].float().unsqueeze(0).to(device) / 255
    return image


def decode_segmap(image, nc=4):
    # 0=background, 1=aurt, 2=cvc, 3=heart,
    # image = copy(image)
    image = np.argmax(image, 0)
    label_colors = np.array([(0, 0, 0), (128, 0, 0), (0, 128, 0), (0, 0, 128)])
    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]
    rgb = np.stack([r, g, b], axis=2)
    return rgb


def createResult(input, prediction):
    # os.makedirs(os.path.join('results/outputs', config['name']), exist_ok=True)

    prediction = prediction.cpu().numpy()

    prediction_ = (prediction * 255).astype('uint8')

    rgb = decode_segmap(prediction_[0])
    input = input * 255
    input = input[0].permute(1, 2, 0).cpu().numpy().astype('uint8')
    result = cv2.addWeighted(input, 1, rgb, 0.35, 0)
    cv2.imwrite(os.path.join('results', "result.jpg"), (result))


def load_or_build(image, config, load=True):
    import pickle

    if load:
        try:
            infile = open("out.pickle", 'rb')
            return pickle.load(infile, encoding='bytes')
        except:
            return load_or_build(image, config, False)

    # create model
    print("=> creating model %s" % config['arch'])
    module = importlib.import_module("." + str(config['arch']), package='models')
    className = getattr(module, config['arch'])

    if config['arch'] == 'NestedUNet':
        model = className(config['num_classes'], config['input_channels'], config['deep_supervision'])
    elif config['arch'] == 'UNet':
        model = className(config['num_classes'], config['input_channels'])
    else:
        model = className(3, config['num_classes'])
    # model = model.to(device)

    model.load_state_dict(torch.load('results/models/%s/model.pth' % config['name'], map_location=device))

    model.eval()
    with torch.no_grad():
        output = model.forward(image)

    filehandler = open("out.pickle", 'wb')
    pickle.dump(output, filehandler)

    return output


def main(image):
    config = vars(parse_args())

    args = parse_args()
    args.name = ""

    with open('config.yml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    print('-' * 20)
    for key in config.keys():
        print('%s: %s' % (key, str(config[key])))
    print('-' * 20)

    # config.update({'dice_loss' : False})

    test_transform = Compose([
        Resize(config['input_h'], config['input_w']),
        pytorch.transforms.ToTensorV2()
    ])
    image = image_loader(image, test_transform)

    # *****************
    output = load_or_build(image, config)

    prediction = torch.argmax(output, 1)
    prediction = torch.nn.functional.one_hot(prediction, config["num_classes"]).permute(0, 3, 1, 2)
    print(image.shape)

    return createResult(image, prediction.cpu().numpy()[0])


if __name__ == '__main__':
    main()
