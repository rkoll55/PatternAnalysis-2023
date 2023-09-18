import torch, tqdm
from .utilis_ import Train_Metrice


def fitting(model, loss, optimizer, train_dataset, test_dataset, CLASS_NUM, DEVICE, scaler, show_thing, opt):
    model.train()
    metrice = Train_Metrice(CLASS_NUM)
    for x, y in tqdm.tqdm(train_dataset, desc='{} Train Stage'.format(show_thing)):
        x, y = x.to(DEVICE).float(), y.to(DEVICE).long()

        with torch.cuda.amp.autocast(opt.amp):
            pred = model(x)
            l = loss(pred, y)
                    

        metrice.update_loss(float(l.data))
        metrice.update_y(y, pred)
        
        scaler.scale(l).backward()

        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()



    model_eval = model.eval()
    with torch.inference_mode():
        for x, y in tqdm.tqdm(test_dataset, desc='{} Test Stage'.format(show_thing)):
            x, y = x.to(DEVICE).float(), y.to(DEVICE).long()

            with torch.cuda.amp.autocast(opt.amp):
                if opt.test_tta:
                    bs, ncrops, c, h, w = x.size()
                    pred = model_eval(x.view(-1, c, h, w))
                    pred = pred.view(bs, ncrops, -1).mean(1)
                    l = loss(pred, y)
                else:
                    pred = model_eval(x)
                    l = loss(pred, y)
                
            metrice.update_loss(float(l.data), isTest=True)
            metrice.update_y(y, pred, isTest=True)

    return metrice.get()


