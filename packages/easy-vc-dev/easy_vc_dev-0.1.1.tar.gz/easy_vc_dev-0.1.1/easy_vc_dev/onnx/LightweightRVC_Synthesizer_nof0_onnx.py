# import json
import torch
from easy_vc_dev.model.LightweightRVC_Synthesizer_nof0 import EasyVC_Synthesizer_nof0_v1
from simple_performance_timer.Timer import Timer


class EasyVC_Synthesizer_nof0_v1_onnx(EasyVC_Synthesizer_nof0_v1):
    def forward(self, phone, phone_lengths, max_len=None, convert_length=None):
        timer_enabled = False
        with Timer("  LRVC Infer", timer_enabled) as t:
            m_p, logs_p, x_mask = self.enc_p(phone, None, phone_lengths)
            t.record("  encp")
            z_p = (m_p + torch.exp(logs_p) * torch.randn_like(m_p) * 0.66666) * x_mask
            z = self.flow(z_p, x_mask, reverse=True)
            t.record("  flow")

            o = self.dec(z)
            t.record("  vocoder")
            return o, x_mask, (z, z_p, m_p, logs_p)
