import dataset
from modules import *
import torch.optim as optim
import matplotlib.pyplot as plt



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#put in training loop
def train(epochs):
    model = ADNI_Transformer(depth=6)
    model.to(device=device)

    dataset = ds.ADNI_Dataset()
    train_loader = dataset.get_train_loader()
    optimizer = optim.Adam(model.parameters(), 1e-5)
    criterion = nn.BCELoss()

    batch_losses = []

    model.train()
    for epoch in range(epochs):
        batch_loss = 0

        for j, (images, labels) in  enumerate(train_loader):
            if images.size(0) == 32:
                optimizer.zero_grad()
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                
                loss = criterion(outputs.squeeze().to(torch.float), labels.to(torch.float))
                loss.backward()
                optimizer.step()
                batch_loss += loss.item()
                
        batch_losses.append(batch_loss)
        print("epoch {} complete".format(epoch + 1))
        
    return model, batch_losses


def visualize_loss(batch_losses):
    
    epochs = range(1, len(batch_losses) + 1)

    
    plt.plot(epochs, batch_losses, marker='o', linestyle='-')
    plt.xlabel('Epoch')
    plt.ylabel('Batch Loss')
    plt.title('Batch Loss Over Epochs')
    plt.grid(True)
    plt.show()


def test_accuracy(model):
    dataset = ds.ADNI_Dataset()
    test_laoder = dataset.get_test_loader()
        
    correct_predictions = 0
    total_samples = 0    
        
    model.eval() 
    for j, (images, labels) in  enumerate(test_laoder):
        if images.size(0) == 32:

            images = images.to(device) 
            labels = labels.to(device)
            
            outputs = model(images)
            predictions = (outputs >= 0.5).squeeze().long()
            correct_predictions += (predictions == labels).sum().item()
            total_samples += labels.size(0)

    accuracy = correct_predictions / total_samples
    return accuracy

if __name__ == "__main__":

    model, losses = train(75)
    torch.save(model.state_dict(), "model/model.pth")
    visualize_loss(losses)
    accuracy = test_accuracy(model)
    
    print("Accuracy of model is {}%".format(accuracy))

    
