ARGUMENT_IS_MANDATORY = "IS MANDATORY" 
MODEL_NAME_TO_URL_PATH_MAPPING = {
    "llama-2-13b-chat": "project/{namespace}/v1/llama-2-13b-chat/infer",
    "stable-diffusion-2-1": "project/{namespace}/v1/stable-diffusion-2-1/infer",
    "mixtral-8x7b-instruct": "project/{namespace}/v1/mixtral-8x7b-instruct/infer",
    "codellama-13b-instruct": "project/{namespace}/v1/codellama-13b-instruct/infer",
}
MODEL_API_DEFAULT_DATA = {"inputs": []}
MODELS_API_DATA_FORMATS = {
    "llama-2-13b-chat": {
        "prompt": {
            "name": "prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "system_prompt": {
            "name": "system_prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "max_new_tokens": {
            "name": "max_new_tokens",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "top_k": {
            "name": "top_k",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "top_p": {
            "name": "top_p",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
        "temperature": {
            "name": "temperature",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
        "num_return_sequences": {
            "name": "num_return_sequences",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "repetition_penalty": {
            "name": "repetition_penalty",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
    },
    "mixtral-8x7b-instruct": {
        "prompt": {
            "name": "prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "system_prompt": {
            "name": "system_prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "max_new_tokens": {
            "name": "max_new_tokens",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "top_k": {
            "name": "top_k",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "top_p": {
            "name": "top_p",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
        "temperature": {
            "name": "temperature",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
        "num_return_sequences": {
            "name": "num_return_sequences",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "repetition_penalty": {
            "name": "repetition_penalty",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
    },
    "codellama-13b-instruct": {
        "prompt": {
            "name": "prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "system_prompt": {
            "name": "system_prompt",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "max_new_tokens": {
            "name": "max_new_tokens",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "top_k": {
            "name": "top_k",
            "shape": [1],
            "datatype": "INT32",
            "data": [],
        },
        "top_p": {
            "name": "top_p",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
        "temperature": {
            "name": "temperature",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
        "action": {
            "name": "action",
            "shape": [1],
            "datatype": "BYTES",
            "data": [],
        },
        "repetition_penalty": {
            "name": "repetition_penalty",
            "shape": [1],
            "datatype": "FP32",
            "data": [],
        },
    },
    "stable-diffusion-2-1": {
        "prompt": {
            "name": "prompt",
            "shape": [1, 1],
            "datatype": "BYTES",
            "data": [],
        },
        "negative_prompt": {
            "name": "negative_prompt",
            "shape": [1, 1],
            "datatype": "BYTES",
            "data": [],
        },
        "height": {
            "name": "height",
            "shape": [1, 1],
            "datatype": "UINT16",
            "data": [],
        },
        "width": {
            "name": "width",
            "shape": [1, 1],
            "datatype": "UINT16",
            "data": [],
        },
        "generator": {
            "name": "generator",
            "shape": [1, 1],
            "datatype": "UINT16",
            "data": [],
        },
        "num_inference_steps": {
            "name": "num_inference_steps",
            "shape": [1, 1],
            "datatype": "UINT16",
            "data": [],
        },
        "guidance_scale": {
            "name": "guidance_scale",
            "shape": [1, 1],
            "datatype": "FP32",
            "data": [],
        },
        "guidance_rescale": {
            "name": "guidance_rescale",
            "shape": [1, 1],
            "datatype": "FP32",
            "data": [],
        },
    },
}
