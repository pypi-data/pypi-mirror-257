__all__ = [
    'Message',
    'LlamaCppParams',
    'CandleParams',
    'LLMParams',
]

from typing import TypedDict, Optional, Required


class Message(TypedDict):
    role: Required[str]
    content: Required[str]


class LlamaCppParams(TypedDict):
    engine: str                             # 'llama.cpp'
    executable: Optional[str]               # 'main'
    model_id: str                           # creator of model
    creator_model_id: str                   # creator of model
    model: Optional[str]                    # model name
    chatml: Optional[bool]                  # False
    n_predict: Optional[int]                # -2
    ctx_size: Optional[int]                 # 2048
    batch_size: Optional[int]               # 512
    temp: Optional[float]                   # 0.8
    n_gpu_layers: Optional[int]             # 0 (max usually 35)
    top_k: Optional[int]                    # 40
    top_p: Optional[float]                  # 0.9
    stop: Optional[list[str]]               # []
    prompt: Optional[str]                   # | prompt xor messages
    messages: Optional[list[Message]]       # /
    no_display_prompt: Optional[bool]       # True
    split_mode: Optional[str]               # 'none', 'layer' (default), 'row'
    tensor_split: Optional[str]             # None, e.g. '3,1'
    main_gpu: Optional[int]                 # None, e.g. 0 (default)


class CandleParams(TypedDict):
    engine: str                             # 'candle'
    executable: Optional[str]               # 'phi', 'stable-lm', 'llama', 'mistral', 'quantized'
    model_id: str
    creator_model_id: str
    model: Optional[str]
    cpu: Optional[bool]                     # False
    temperature: Optional[int]              # 0.8
    top_p: Optional[int]                    # 0.9
    sample_len: Optional[int]               # 100
    quantized: Optional[bool]               # False
    use_flash_attn: Optional[bool]          # False
    stop: Optional[list[str]]               # []
    prompt: Optional[str]                   # | prompt xor messages
    messages: Optional[list[Message]]       # /


LLMParams: type = LlamaCppParams | CandleParams
