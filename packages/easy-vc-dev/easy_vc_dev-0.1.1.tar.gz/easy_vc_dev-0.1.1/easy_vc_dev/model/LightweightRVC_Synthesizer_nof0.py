# import json
import torch
from torch import nn
from easy_vc_dev import commons
from easy_vc_dev.model.components.TextEncoder768 import TextEncoder768
from easy_vc_dev.model.components.PosteriorEncoder import PosteriorEncoder
from easy_vc_dev.model.components.ResidualCouplingBlock import ResidualCouplingBlock

from collections import OrderedDict

from easy_vc_dev.model.components.hifigan.HifiganDecoder import HifiganDecoder
from simple_performance_timer.Timer import Timer


class EasyVC_Synthesizer_nof0_v1(nn.Module):
    def __init__(
        self,
        spec_channels: int = 1024 // 2 + 1,
        segment_size: int = 6400 // 160,
        inter_channels: int = 80,
        hidden_channels: int = 192,
        filter_channels: int = 768,
        n_heads: int = 2,
        n_layers: int = 6,
        kernel_size: int = 3,
        p_dropout: int = 0,
        upsample_initial_channel: int = 128,
        gin_channels: int = 256,
    ):
        super().__init__()
        self.version = 1
        self.spec_channels = spec_channels
        self.inter_channels = inter_channels
        self.hidden_channels = hidden_channels
        self.filter_channels = filter_channels
        self.n_heads = n_heads
        self.n_layers = n_layers
        self.kernel_size = kernel_size
        self.p_dropout = p_dropout
        self.upsample_initial_channel = upsample_initial_channel
        self.segment_size = segment_size
        self.gin_channels = gin_channels
        self.enc_p = TextEncoder768(
            inter_channels,
            hidden_channels,
            filter_channels,
            n_heads,
            n_layers,
            kernel_size,
            p_dropout,
            f0=False,
        )
        self.enc_q = PosteriorEncoder(
            spec_channels,
            inter_channels,
            hidden_channels,
            5,
            1,
            16,
            gin_channels=gin_channels,
        )
        self.flow = ResidualCouplingBlock(inter_channels, hidden_channels, 5, 1, 3, gin_channels=gin_channels)

        # # Hifigan向け
        # # ckpt = torch.load("models/vocoder/hifigan_custom/model-635000-gen.pt")
        # # ckpt = torch.load("model-best-gen.pt")
        # ckpt = torch.load("models/vocoder/hifigan/model-635000-gen_80.pt")
        # # ckpt = torch.load("model-695000-gen_192.pt")

        # # inter_channels = ckpt["n_mels"]
        # # upsample_initial_channel = ckpt["upsample_initial_channel"]

        self.dec = HifiganDecoder(in_channels=inter_channels, upsample_initial_channel=upsample_initial_channel)
        self.infer_channels = inter_channels
        self.upsample_initial_channel = upsample_initial_channel

        # new_state_dict = OrderedDict()
        # for k, v in ckpt["model"].items():
        #     name = k[7:] if k.startswith("module.") else k  # 「module.」があれば削除
        #     new_state_dict[name] = v
        # self.dec.load_state_dict(new_state_dict)

        # APNet2向け
        # config_file = "configs/apnet2/config.json"
        # with open(config_file) as f:
        #     data = f.read()
        # json_config = json.loads(data)
        # h = AttrDict(json_config)

        # self.vocoder = Generator(h)
        # new_state_dict = OrderedDict()
        # ckpt = torch.load("models/vocoder/APNet2/g_00010000_16k.pt")
        # for k, v in ckpt["generator"].items():
        #     name = k[7:] if k.startswith("module.") else k  # 「module.」があれば削除
        #     new_state_dict[name] = v

        # self.vocoder.load_state_dict(new_state_dict)

    def remove_weight_norm(self):
        self.dec.remove_weight_norm()
        self.flow.remove_weight_norm()
        self.enc_q.remove_weight_norm()

    def forward(self, phone, phone_lengths, y, y_lengths):
        # g = self.emb_g(ds).unsqueeze(-1)
        m_p, logs_p, x_mask = self.enc_p(phone, None, phone_lengths)
        z, m_q, logs_q, y_mask = self.enc_q(y, y_lengths)
        z_p = self.flow(z, y_mask)
        z_slice, ids_slice = commons.rand_slice_segments(z, y_lengths, self.segment_size)
        o = self.dec(z_slice)
        return o, ids_slice, x_mask, y_mask, (z, z_p, m_p, logs_p, m_q, logs_q)

        # APNet2向け
        # logamp_g, pha_g, _, _, y_g = self.dec(z_slice)
        # return y_g, ids_slice, x_mask, y_mask, (z, z_p, m_p, logs_p, m_q, logs_q)

    def infer(self, phone, phone_lengths, max_len=None, convert_length=None):
        timer_enabled = False
        with Timer("  LRVC Infer", timer_enabled) as t:
            m_p, logs_p, x_mask = self.enc_p(phone, None, phone_lengths)
            t.record("  encp")
            z_p = (m_p + torch.exp(logs_p) * torch.randn_like(m_p) * 0.66666) * x_mask
            z = self.flow(z_p, x_mask, reverse=True)
            t.record("  flow")
            # print(f"z shape:{z.shape}, z_p shape:{z_p.shape}, m_p shape:{m_p.shape}, logs_p shape:{logs_p.shape}")

            o = self.dec(z)
            t.record("  vocoder")
            return o, x_mask, (z, z_p, m_p, logs_p)

            # APNet2向け
            # logamp_g, pha_g, _, _, y_g = self.dec(z)
            # t.record("  vocoder")
            # return y_g, x_mask, (z, z_p, m_p, logs_p)

    def load_vocoder(self, path: str):
        ckpt = torch.load(path, map_location="cpu")
        new_state_dict = OrderedDict()
        for k, v in ckpt["model"].items():
            name = k[7:] if k.startswith("module.") else k  # 「module.」があれば削除
            new_state_dict[name] = v
        self.dec.load_state_dict(new_state_dict)

    def freeze_vocoder_weights(self):
        for param in self.dec.parameters():
            param.requires_grad = False
