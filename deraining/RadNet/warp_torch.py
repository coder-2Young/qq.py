import torch
from torchsample.utils import *


def inverse_warp(input, flow):
    size = input.size()  # input=[N C H W]
    N = size[0]
    C = size[1]
    H = size[2]
    W = size[3]

    N_i = torch.arange(0, N)
    H_i = torch.arange(0, H)
    W_i = torch.arange(0, W)

    n, h, w = torch.meshgrid(N_i, H_i, W_i)
    n = torch.unsqueeze(n, dim=1)  # [N,1, H, W]
    w = torch.unsqueeze(w, dim=1)
    h = torch.unsqueeze(h, dim=1)

    n = n.float().cuda()
    h = h.float().cuda()
    w = w.float().cuda()

    v_col, v_row = torch.split(flow, int((flow.size()[1]) / 2), dim=1)
    print('-' * 40)
    print(v_row.size())
    print('-' * 40)
    """ calculate index """
    v_r0 = torch.floor(v_row)
    v_r1 = v_r0 + 1
    v_c0 = torch.floor(v_col)
    v_c1 = v_c0 + 1

    H_ = (H - 1).float().cuda
    W_ = (W - 1).float().cuda

    i_r0 = torch.clamp(h + v_r0, 0., H_)
    i_r1 = torch.clamp(h + v_r1, 0., H_)
    i_c0 = torch.clamp(w + v_c0, 0., W_)
    i_c1 = torch.clamp(w + v_c1, 0., W_)

    i_r0c0 = torch.cat([n, i_r0, i_c0], dim=1).int()
    i_r0c1 = torch.cat([n, i_r0, i_c1], dim=1).int()
    i_r1c0 = torch.cat([n, i_r1, i_c0], dim=1).int()
    i_r1c1 = torch.cat([n, i_r1, i_c1], dim=1).int()

    print('-' * 40)
    print(input.size())
    print(i_r0c0.size())
    print('-' * 40)

    f00 = th_gather_nd(input, i_r0c0)
    f01 = th_gather_nd(input, i_r0c1)
    f10 = th_gather_nd(input, i_r1c0)
    f11 = th_gather_nd(input, i_r1c1)

    w00 = torch.matmul((v_r1 - v_row), (v_c1 - v_col))
    w01 = torch.matmul((v_r1 - v_row), (v_col - v_c0))
    w10 = torch.matmul((v_row - v_r0), (v_c1 - v_col))
    w11 = torch.matmul((v_row - v_r0), (v_col - v_c0))

    out = torch.matmul(w00, f00) + torch.matmul(w01, f01) + torch.matmul(w10, f10) + torch.matmul(w11, f11)

    return out











