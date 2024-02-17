import re
import random
import pandas as pd
import json


class BaseCoder:

    def __init__(self):
        self.number_mapping = {}
        self.encoding = None

    def encode_number(self, number):
        try:
            if number not in self.number_mapping:
                random_value = ''.join(random.choice('0123456789') for _ in range(12))
                self.number_mapping[number] = random_value

            return self.number_mapping[number]
        except Exception as e:
            print(f"Error in encode_number: {e}")
            return number

    def encode_str(self, text):
        try:
            encoded_text = re.sub(r'\b\d+\b', lambda x: self.encode_number(x.group()), text)
            self.encodings = self.number_mapping
            return encoded_text, self.number_mapping
        except Exception as e:
            print(f"Error in encode_str: {e}")
            return text, self.number_mapping

    def decode_str(self, text, number_mapping):
        for original_number, random_value in number_mapping.items():
            text = re.sub(r'\b' + re.escape(random_value) + r'\b', original_number, text)
        return text

    def encode_df(self, dataframe):
        try:
            def encode_cell(cell):
                try:
                    if isinstance(cell, (int, float)):
                        return self.encode_number(str(cell))
                    elif isinstance(cell, str):
                        return re.sub(r'\b\d+\b', lambda x: self.encode_number(x.group()), cell)
                    else:
                        return cell
                except Exception as e:
                    print(f"Error in encode_cell: {e}")
                    return cell

            encoded_df = dataframe.map(encode_cell)
            self.encodings = self.number_mapping
            return encoded_df, self.number_mapping

        except Exception as e:
            print(f"Error in encode_df: {e}")
            self.encodings = self.number_mapping
            return dataframe, self.number_mapping


    def decode_df(self, encoded_df, number_mapping):
        def decode_cell(cell):
            try:
                if isinstance(cell, str) and cell in number_mapping.values():
                    for key, value in number_mapping.items():
                        if value == cell:
                            return key
                else:
                    return cell
            except Exception as e:
                print(f"Error in decode_cell: {e}")
                return cell

        try:
            decoded_df = encoded_df.map(decode_cell)
            return decoded_df
        except Exception as e:
            print(f"Error in decode_df: {e}")
            return encoded_df

    def encode_in_ratio(self, data, ratio):
        try:
            if ratio == 0 or ratio == 1:
                raise ValueError("Ratio should not be 0 and 1")

            if isinstance(data, str):
                def encode_number(match):
                    try:
                        original_number = int(match.group())
                        encoded_number = original_number * ratio
                        return str(encoded_number)
                    except Exception as e:
                        print(f"Error in encode_number: {e}")
                        return match.group()

                encoded_text = re.sub(r'\b\d+\b', encode_number, data)
                return encoded_text

            elif isinstance(data, pd.DataFrame):
                def encode_in_ratio_cell(cell):
                    try:
                        if isinstance(cell, (int, float)):
                            return cell * ratio
                        else:
                            return cell
                    except Exception as e:
                        print(f"Error in encode_in_ratio_cell: {e}")
                        return cell

                encoded_df = data.map(encode_in_ratio_cell)
                return encoded_df

            elif isinstance(data, dict):
                def encode_in_ratio_dict(obj):
                    try:
                        if isinstance(obj, (int, float)):
                            return obj * ratio
                        elif isinstance(obj, list):
                            return [encode_in_ratio_dict(element) for element in obj]
                        elif isinstance(obj, dict):
                            return {key: encode_in_ratio_dict(value) for key, value in obj.items()}
                        else:
                            return obj
                    except Exception as e:
                        print(f"Error in encode_in_ratio_dict: {e}")
                        return obj

                encoded_dict = encode_in_ratio_dict(data)
                return encoded_dict

            else:
                raise ValueError("Unsupported data type. Only string, DataFrame, or Json is allowed.")
        except Exception as e:
            print(f"Error in encode_in_ratio: {e}")
            return data

    
    def decode_in_ratio(self, data, ratio):
        try:
            if ratio == 0 or ratio == 1:
                raise ValueError("Ratio should not be 0 and 1")
            
            if isinstance(data, str):
                def decode_number(match):
                    try:
                        original_number = int(match.group())
                        decoded_number = original_number / ratio
                        return str(int(decoded_number)) if decoded_number.is_integer() else str(decoded_number)
                    except Exception as e:
                        print(f"Error in decode_number: {e}")
                        return match.group()

                decoded_text = re.sub(r'\b\d+(\.\d+)?\b', decode_number, data)
                return decoded_text

            elif isinstance(data, pd.DataFrame):
                def decode_in_ratio_cell(cell):
                    try:
                        if isinstance(cell, (int, float)):
                            decoded_number = cell / ratio
                            # Remove decimal part if it's zero
                            return int(decoded_number) if decoded_number.is_integer() else decoded_number
                        else:
                            return cell
                    except Exception as e:
                        print(f"Error in decode_in_ratio_cell: {e}")
                        return cell

                decoded_df = data.map(decode_in_ratio_cell)
                return decoded_df
            
            elif isinstance(data, dict):
                def decode_in_ratio_dict(obj):
                    try:
                        if isinstance(obj, (int, float)):
                            return obj / ratio
                        elif isinstance(obj, list):
                            return [decode_in_ratio_dict(element) for element in obj]
                        elif isinstance(obj, dict):
                            return {key: decode_in_ratio_dict(value) for key, value in obj.items()}
                        else:
                            return obj
                    except Exception as e:
                        print(f"Error in decode_in_ratio_dict: {e}")
                        return obj

                encoded_dict = decode_in_ratio_dict(data)
                return encoded_dict

            else:
                raise ValueError("Unsupported data type. Only string, JSON or DataFrame is allowed.")
        except Exception as e:
            print(f"Error in decode_in_ratio: {e}")
            return data


    


    

    
    
    