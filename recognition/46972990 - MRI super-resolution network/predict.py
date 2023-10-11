import torch
import matplotlib.pyplot as plt
from modules import ESPCN
from dataset import get_test_loader
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = ESPCN(upscale_factor=4, channels=1)
model.load_state_dict(torch.load('final_model.pth'))
model = model.to(device).eval()

test_loader = get_test_loader()
test_data_list = list(test_loader)

selected_downscaled_images = []
selected_original_images = []

# Randomly select 5 batches and then one image set from each of these batches
for _ in range(5):
    downscaled_batch, original_batch = random.choice(test_data_list)
    
    # Randomly select an image set from the chosen batch
    index = random.randint(0, len(downscaled_batch) - 1)
    selected_downscaled_images.append(downscaled_batch[index])
    selected_original_images.append(original_batch[index])

# Convert the lists to tensors
sample_downscaled_images = torch.stack(selected_downscaled_images).to(device)
sample_original_images = torch.stack(selected_original_images).to(device)

def visualize_progress(model, downscaled, original, num_images=5):
    # Set model to evaluation mode for inference
    model.eval()
    with torch.no_grad():
        upscaled = model(downscaled)
    
    # Loop through the desired number of images
    for i in range(min(num_images, downscaled.shape[0])):
        # Convert tensors to numpy arrays for visualization
        downscaled_img = downscaled[i].cpu().squeeze().numpy()
        upscaled_img = upscaled[i].cpu().squeeze().numpy()
        original_img = original[i].cpu().squeeze().numpy()
        
        # Plotting
        plt.figure(figsize=(15,5))
        plt.subplot(1, 3, 1)
        plt.imshow(downscaled_img, cmap='gray')
        plt.title("Downscaled")
        plt.subplot(1, 3, 2)
        plt.imshow(upscaled_img, cmap='gray')
        plt.title("Upscaled by Model")
        plt.subplot(1, 3, 3)
        plt.imshow(original_img, cmap='gray')
        plt.title("Original")
        plt.show()

# Visualize the results
visualize_progress(model, sample_downscaled_images, sample_original_images)