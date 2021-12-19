import torch
import torch.nn as nn


def warp_1(x, flo):
    """
    warp an image/tensor (im2) back to im1, according to the optical flow
    x: [B, C, H, W] (im2)
    flo: [B, 2, H, W] flow
    """
    B, C, H, W = x.size()
    # mesh grid
    xx = torch.arange(0, W).view(1, -1).repeat(H, 1)
    yy = torch.arange(0, H).view(-1, 1).repeat(1, W)
    xx = xx.view(1, 1, H, W).repeat(B, 1, 1, 1)
    yy = yy.view(1, 1, H, W).repeat(B, 1, 1, 1)
    grid = torch.cat((xx, yy), 1).float()

    x = x.cuda()
    grid = grid.cuda()
    vgrid = grid + flo  # B,2,H,W
    # 图二的每个像素坐标加上它的光流即为该像素点对应在图一的坐标

    # scale grid to [-1,1]
    ##2019 code
    vgrid[:, 0, :, :] = 2.0 * vgrid[:, 0, :, :].clone() / max(W - 1, 1) - 1.0
    # 取出光流v这个维度，原来范围是0~W-1，再除以W-1，范围是0~1，再乘以2，范围是0~2，再-1，范围是-1~1
    vgrid[:, 1, :, :] = 2.0 * vgrid[:, 1, :, :].clone() / max(H - 1, 1) - 1.0  # 取出光流u这个维度，同上

    vgrid = vgrid.permute(0, 2, 3, 1)  # from B,2,H,W -> B,H,W,2，为什么要这么变呢？是因为要配合grid_sample这个函数的使用
    output = nn.functional.grid_sample(x, vgrid, align_corners=True)
    mask = torch.autograd.Variable(torch.ones(x.size())).cuda()
    mask = nn.functional.grid_sample(mask, vgrid, align_corners=True)

    ##2019 author
    mask[mask < 0.9999] = 0
    mask[mask > 0] = 1

    ##2019 code
    # mask = torch.floor(torch.clamp(mask, 0 ,1))
    return output * mask