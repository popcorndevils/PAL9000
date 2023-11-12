import pandas as pd # noqa
import numpy as np # noqa
from enum import Enum # noqa


class APIPrices:
    class ChatGPT4(Enum):
        # per 1000 tokens
        InputTokens = .03
        OutputTokens = .06

    class ChatGPT4_32k(Enum):
        # per 1000 tokens
        InputTokens = .06
        OutputTokens = .12

    class ChatGPT3_5_Turbo(Enum):
        # per 1000 tokens
        InputTokens = .0010
        OutputTokens = .0020

    class ChatGPT3_5_Turbo_Instruct(Enum):
        # per 1000 tokens
        InputTokens = .0015
        OutputTokens = .0020

    class DallE3:
        # per image
        class Standard(Enum):
            size_1024x1024 = .040
            size_1024x1792 = .080
            size_1792x1024 = .080

        class HD(Enum):
            size_1024x1024 = .080
            size_1024x1792 = .120
            size_1792x1024 = .120

    class DallE2(Enum):
        # per image
        size_1024x1024 = .020
        size_512x512 = .018
        size_256x256 = .016


price_map = {
    "gpt-4": APIPrices.ChatGPT4,
    "gpt-3.5-turbo": APIPrices.ChatGPT3_5_Turbo,
    "dall-e-3_standard_1024x1024": APIPrices.DallE3.Standard.size_1024x1024.value,
    "dall-e-3_standard_1792x1024": APIPrices.DallE3.Standard.size_1792x1024.value,
    "dall-e-3_standard_1024x1792": APIPrices.DallE3.Standard.size_1024x1792.value,
    "dall-e-3_hd_1024x1024": APIPrices.DallE3.HD.size_1024x1024.value,
    "dall-e-3_hd_1792x1024": APIPrices.DallE3.HD.size_1792x1024.value,
    "dall-e-3_hd_1024x1792": APIPrices.DallE3.HD.size_1024x1792.value,
    "dall-e-2_standard_1024x1024": APIPrices.DallE2.size_1024x1024.value,
    "dall-e-2_standard_512x512": APIPrices.DallE2.size_512x512.value,
    "dall-e-2_standard_256x256": APIPrices.DallE2.size_256x256.value,
}


class PandaBear:
    def calc_usage(self, df: pd.DataFrame):
        _df_chats = df[df["api_type"] == "chat_completion"].copy(deep = True)
        _df_images = df[df["api_type"] == "image_generation"].copy(deep = True)
        _df_images["cat"] = _df_images["model"] + "_" + _df_images["quality"] + "_" + _df_images["size"]

        _chat_usage = _df_chats.groupby('model').agg({'input_tokens': 'sum', 'completion_tokens': 'sum'}).to_dict('index')
        _chat_costs = {
            model: {
                "input_tokens": usage['input_tokens'],
                "input_price": price_map[model].InputTokens.value,
                "output_tokens": usage['completion_tokens'],
                "output_price": price_map[model].OutputTokens.value,
                "input_cost": (usage['input_tokens'] / 1000) * price_map[model].InputTokens.value,
                "output_cost": (usage['completion_tokens'] / 1000) * price_map[model].OutputTokens.value
            }
            for model, usage in _chat_usage.items()
        }

        _img_usage = _df_images.groupby('cat').agg({'n': 'sum'}).to_dict('index')
        _img_costs = {
            cat: {
                "images": usage["n"],
                "price": price_map[cat],
                "cost": usage['n'] * price_map[cat]
            }
            for cat, usage in _img_usage.items()
        }
        # return (_chat_costs, _img_costs)
        return self.format_costs_as_dataframe((_chat_costs, _img_costs))

    def format_costs_as_dataframe(self, calc_usage_output):
        chat_costs, img_costs = calc_usage_output

        # Process chat costs
        _chat_data = []

        for model, data in chat_costs.items():
            _chat_data.append({
                "MODEL": model,
                "USAGE": f"{data['input_tokens']} Input",
                "PRICE": f"{data['input_price']}/1000",
                "TOTAL": data['input_cost'],
            })
            _chat_data.append({
                "MODEL": model,
                "USAGE": f"{data['output_tokens']} Output",
                "PRICE": f"{data['output_price']}/1000",
                "TOTAL": data['output_cost'],
            })

        # Process image costs
        _img_data = [{
            "MODEL": model,
            "USAGE": f"{data['images']} images",
            "PRICE": f"{data['price']}/image",
            "TOTAL": data['cost']}
            for model, data in img_costs.items()
        ]

        # Combine chat and image data
        combined_data = _chat_data + _img_data

        # Convert to DataFrame
        df = pd.DataFrame(combined_data)

        # Adding a final row with a total
        _total = f"${df['TOTAL'].sum():,.2f}"
        df["TOTAL"] = df["TOTAL"].apply(lambda x: f"${x:,.2f}")
        df = pd.concat([df, pd.DataFrame([{"MODEL": "", "USAGE": "", "PRICE": "TOTAL COST", "TOTAL": _total}])])

        return df
