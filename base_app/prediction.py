import torch
import torchvision
import cv2
import torchvision.transforms as transforms
from PIL import Image

transform = transforms.ToTensor()
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[1, 1, 1])
res_to = 256
number_of_label_points = 9
model_path = ".\checkpoint_202008061041.pth.tar"
image_address = "n.png"
image_name = "test1"
# img = cv2.imread(image_address)
with Image.open("n.png") as n:
    
img_x256 = cv2.resize(img, (res_to, res_to), cv2.INTER_CUBIC)
cv2.imwrite('out/' + image_name + "_" + str(res_to) + ".jpg", img_x256)

model = torchvision.models.resnet18(num_classes=18).cpu()
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model_state_dict'], strict='False')
model.eval()

with Image.open('out/' + image_name + "_" + str(res_to) + ".jpg") as img:
    input_image = img.convert('RGB')

input = transform(input_image)
input = normalize(input)
input = input.unsqueeze(0)
input = input[:, :, 14:241, 14:241]

pred = model(input).detach().numpy()
print(pred)


for i in range(number_of_label_points):
    img_x256 = cv2.circle(img_x256, (int(pred[0, 2 * i + 0].item()) + 14,
                                     int(pred[0, 2 * i + 1].item()) + 14), 4, (0, 1, 0), 2)
    img_x256 = cv2.circle(img_x256, (int(pred[0, 2 * i + 0].item()) + 14,
                                     int(pred[0, 2 * i + 1].item()) + 14), 4, (1, 0, 0), 2)
    cv2.imwrite('out/labeled_' + image_name + "_" + str(res_to) + ".jpg", img_x256)
