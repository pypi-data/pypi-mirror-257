import torch

def get_loss(out_encoder, out_decoder, prior_coder, out_predictor, m, y, dim_m, dim_z, is_obs=True, use_prior=True, lbd=1.0):

    mu_encoder, sigma_encoder = out_encoder[:, :dim_z], torch.exp(out_encoder[:, dim_z:])
    mu_decoder, sigma_decoder = out_decoder[:, :dim_m], torch.exp(out_decoder[:, dim_m:])
    mu_prior, sigma_prior = prior_coder[:, :dim_z], torch.exp(prior_coder[:, dim_z:])
    mu_predictor, sigma_predictor= out_predictor[:, :1], torch.exp(out_predictor[:, 1:])
    
    if use_prior:
        kl = - out_encoder[:, dim_z:].sum(dim=1) + prior_coder[:, dim_z:].sum(dim=1) + (((mu_encoder - mu_prior) ** 2 + sigma_encoder * sigma_encoder) / (2 * sigma_prior * sigma_prior)).sum(dim=1)
    else:
        kl = - out_encoder[:, dim_z:].sum(dim=1) + ((mu_encoder ** 2 + sigma_encoder * sigma_encoder) / 2).sum(dim=1)
    ll = - out_decoder[:, dim_m:].sum(dim=1) - ((mu_decoder - m) ** 2 / 2 / (sigma_decoder ** 2)).sum(dim=1)
    # ELBO = - kl.sum() + ll.sum()
    if is_obs: # 如果是观测数据，那么应该回传y的损失，否则y观测不到，仅作为预测数据处理
        ll_y = - out_predictor[:, 1:].sum(dim=1) - ((mu_predictor - y) ** 2 / 2 / (sigma_predictor ** 2)).sum(dim=1)
        all_loss = -(ll.sum() - kl.sum() + lbd * ll_y.sum())
        return all_loss #-ll.sum(), - kl.sum(), + lbd * ll_y.sum(), all_loss
    else:
        all_loss = -(ll.sum() - kl.sum())
        return all_loss    #-ll.sum(), - kl.sum(), all_loss   