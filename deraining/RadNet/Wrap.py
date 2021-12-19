import tensorflow as tf

def inverse_warp(input, flow):
    shape = tf.shape(input)
    N = shape[0]
    H = shape[1]
    W = shape[2]
    C = shape[3]

    N_i = tf.range(0, N)  # 0 .. N-1
    W_i = tf.range(0, W)
    H_i = tf.range(0, H)

    n, h, w = tf.meshgrid(N_i, H_i, W_i, indexing='ij')
    n = tf.expand_dims(n, axis=3)  # [N, W, H, 1]
    h = tf.expand_dims(h, axis=3)
    w = tf.expand_dims(w, axis=3)

    n = tf.cast(n, tf.float32)
    h = tf.cast(h, tf.float32)
    w = tf.cast(w, tf.float32)

    v_col, v_row = tf.split(flow, 2, axis=-1)  # split flow into v_row & v_col
    """ calculate index """
    v_r0 = tf.floor(v_row)
    v_r1 = v_r0 + 1
    v_c0 = tf.floor(v_col)
    v_c1 = v_c0 + 1

    H_ = tf.cast(H - 1, tf.float32)
    W_ = tf.cast(W - 1, tf.float32)
    i_r0 = tf.clip_by_value(h + v_r0, 0., H_)
    i_r1 = tf.clip_by_value(h + v_r1, 0., H_)
    i_c0 = tf.clip_by_value(w + v_c0, 0., W_)
    i_c1 = tf.clip_by_value(w + v_c1, 0., W_)

    i_r0c0 = tf.cast(tf.concat([n, i_r0, i_c0], axis=-1), tf.int32)
    i_r0c1 = tf.cast(tf.concat([n, i_r0, i_c1], axis=-1), tf.int32)
    i_r1c0 = tf.cast(tf.concat([n, i_r1, i_c0], axis=-1), tf.int32)
    i_r1c1 = tf.cast(tf.concat([n, i_r1, i_c1], axis=-1), tf.int32)

    """ take value from index """
    f00 = tf.gather_nd(input, i_r0c0)  # 图像像素值
    f01 = tf.gather_nd(input, i_r0c1)
    f10 = tf.gather_nd(input, i_r1c0)
    f11 = tf.gather_nd(input, i_r1c1)

    """ calculate coeff """
    w00 = (v_r1 - v_row) * (v_c1 - v_col)  # 像素的位移
    w01 = (v_r1 - v_row) * (v_col - v_c0)
    w10 = (v_row - v_r0) * (v_c1 - v_col)
    w11 = (v_row - v_r0) * (v_col - v_c0)

    out = w00 * f00 + w01 * f01 + w10 * f10 + w11 * f11
    return out