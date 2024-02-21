from mist.models.unet import UNet
from mist.models.nnunet import NNUnet
from mist.models.attn_unet import MONAIAttnUNet
from mist.models.swin_unetr import MONAISwinUNETR

"""
Available models:
    - nnUNet
    - UNet
    - Attention UNet
    - Swin UNETR
"""


def get_model(**kwargs):
    if kwargs["model_name"] == "nnunet":
        model = NNUnet(kwargs["n_classes"],
                       kwargs["n_channels"],
                       kwargs["pocket"],
                       kwargs["deep_supervision"],
                       kwargs["deep_supervision_heads"],
                       kwargs["vae_reg"],
                       kwargs["patch_size"],
                       kwargs["target_spacing"],
                       kwargs["use_res_block"])
    elif kwargs["model_name"] == "unet":
        model = UNet(kwargs["n_classes"],
                     kwargs["n_channels"],
                     kwargs["pocket"],
                     kwargs["deep_supervision"],
                     kwargs["deep_supervision_heads"],
                     kwargs["vae_reg"],
                     kwargs["patch_size"],
                     kwargs["target_spacing"],
                     kwargs["use_res_block"])
    elif kwargs["model_name"] == "attn_unet":
        model = MONAIAttnUNet(kwargs["n_classes"],
                              kwargs["n_channels"],
                              kwargs["pocket"],
                              kwargs["patch_size"])
    elif kwargs["model_name"] == "unetr":
        model = MONAISwinUNETR(kwargs["n_classes"],
                               kwargs["n_channels"],
                               kwargs["patch_size"])
    else:
        raise ValueError("Invalid model name")

    return model
