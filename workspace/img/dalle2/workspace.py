import torch
from dalle2_pytorch import DiffusionPrior, DiffusionPriorNetwork, OpenAIClipAdapter
from dalle2_pytorch.trainer import DiffusionPriorTrainer


def load_diffusion_model(dprior_path):

    prior_network = DiffusionPriorNetwork(
        dim=768,
        depth=24,
        dim_head=64,
        heads=32,
        normformer=True,
        attn_dropout=5e-2,
        ff_dropout=5e-2,
        num_time_embeds=1,
        num_image_embeds=1,
        num_text_embeds=1,
        num_timesteps=1000,
        ff_mult=4
    )

    diffusion_prior = DiffusionPrior(
        net=prior_network,
        clip=OpenAIClipAdapter("ViT-L/14"),
        image_embed_dim=768,
        timesteps=1000,
        cond_drop_prob=0.1,
        loss_type="l2",
        condition_on_text_encodings=True,

    )

    trainer = DiffusionPriorTrainer(
        diffusion_prior=diffusion_prior,
        lr=1.1e-4,
        wd=6.02e-2,
        max_grad_norm=0.5,
        amp=False,
        group_wd_params=True,
        use_ema=True,
        #device=device,
        accelerator=None,
    )

    trainer.load(dprior_path)

    return trainer

def infer(text: str):
    # tokenize the text
    tokenized_text = clip.tokenize(text)
    # predict an embedding
    predicted_embedding = prior.sample(tokenized_text, n_samples_per_batch=2, cond_scale=1.0)