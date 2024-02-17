![logo](https://github.com/Distructor2404/fastapi_methods/blob/main/BC.gif?raw=true)

# **BC-EnDeCoder**

BC-EnDeCoder is a Python library that provides a secure way to encode and decode data for use with Large Language Models (LLM). The library allows you to protect sensitive information by passing a fake dummy value, which is then encoded and decoded to and from its original form after receiving a response from the LLM.

## Features

- **Secure Encoding and Decoding:** Protect your sensitive data by encoding it with a fake dummy value and decoding it back to the original form after interacting with an LLM.

- **Easy Integration:** Simple and easy-to-use functions for encoding and decoding data, making it convenient to integrate into your projects.

- **Customizable Encoding Parameters:** Fine-tune the encoding process with customizable parameters to suit your specific use case.

## Installation

To install BC-EnDeCoder, you can use the following pip command:

```bash 
pip install bc-en-de-coder 
```


## How it Works

BC-EnDeCoder facilitates a secure interaction with LLMs through a three-step process:

- **Encoding with a Dummy Value:** Sensitive data is encoded using a fake value, providing an added layer of security during transmission to an LLM.

- **Interaction with LLM:** The encoded data is then passed to the LLM for analysis or processing.

- **Decoding the Response:** Upon receiving the LLM's response, BC-EnDeCoder decodes it, revealing the original information without compromising its security.




### Encoding and Decoding values in string

Encode and decode values in string using the `encode_str()` and `decode_str()` methods. 

```python
from bc_endecoder.replace import BaseCoder

bc = BaseCoder()

text = '''
        This is a dummy text with value 200,100,150,250.
        We need to protect these values.
        '''

encoded_text,encodings = bc.encode_str(text)  #encode_str takes 1 paramter which is the text and returns the encoded text and encoding
print("Encoded Text : \n",encoded_text)

## encoded_text can be passed to GPT and after getting back the response it will be decoded using decode_str() method

original_text = bc.decode_str(encoded_text,encodings)  #decode_str takes 2 parameters which are the encoded_text and encoding and returns the original text
print("\nOriginal Text : \n",original_text)
```

Output
```python
Encoded Text : 
 
        This is a dummy text with value 4858416350,7636580946,0858875814,8301435677.
        We need to protect these values.
        

Original Text : 
 
        This is a dummy text with value 200,100,150,250.
        We need to protect these values.
```




### Encoding and Decoding values in Dataframe

Encode and decode values in Dataframe using the `encode_df()` and `decode_df()` methods.

```python
from bc_endecoder.replace import BaseCoder
import pandas as pd
import numpy as np

bc = BaseCoder()

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [25, 30, 22, 35, 28],
    'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami'],
    'Salary': [60000, 80000, 55000, 90000, 70000]
}
df = pd.DataFrame(data)


encoded_df,encoding = bc.encode_df(df)  #encode_df takes 1 paramter which is Dataframe and returns the encoded dataframe and encodings
print("Encoded_df : \n",encoded_df)

## encoded_df can be passed to GPT and after getting back the response it will be decoded using decode_df() method

original_df = bc.decode_df(encoded_df,encoding)  #decode_str takes 2 parameters which are the encoded_df and encoding and returns the original df
print("\nOriginal_df : \n",original_df)
```
Output
```python
Encoded_df :    
              Name  Age                  City  Salary
        0    Alice  8623770624       New York  0197705789
        1      Bob  5223314994  San Francisco  9743912420
        2  Charlie  1795473060    Los Angeles  8982145407
        3    David  6439787181        Chicago  6618233087
        4      Eva  4699492207          Miami  6680877680

Original_df : 
             Name   Age          City  Salary
        0    Alice  25       New York  60000
        1      Bob  30  San Francisco  80000
        2  Charlie  22    Los Angeles  55000
        3    David  35        Chicago  90000
        4      Eva  28          Miami  70000
```




### Encoding and Decoding values with a ratio in Dataframe, Json or String

Encode and decode values with a ratio in Dataframe, Json or String using the `encode_df_ratio()` and `decode_df_ratio()` methods.

```python
from bc_endecoder.replace import BaseCoder
import pandas as pd
import numpy as np

bc = BaseCoder()

json_data = {
  "key1": 10,
  "key2": 20,
  "key3": "Hello",
  "key4": 3.14,
  "key5": [1, 2, 3],
  "key6": {"nested_key": "nested_value"},
  "key8": "2022-01-01",
  "key9": None,
  "key10": {"sub_key1": 5, "sub_key2": "world"},
  "key11": [4.5, 6.7, 8.9],
  "key12": False,
  "key13": "42",
  "key14": ["apple", "banana", "cherry"],
  "key15": {"nested_key2": [1, 2, 3]},
  "key16": 7.77,
  "key17": "test",
  "key18": {"sub_key3": "value3", "sub_key4": 10},
  "key19": [True, False],
  "key20": 12345
}

ratio = 56 #this is the ratio for which we want to encode the data, it can be any number except 0 and 1

encoded_data = bc.encode_in_ratio(json_data,ratio)  #encode_in_ratio takes 2 paramter which is Data and the ratio number, and returns the encoded data
print("Encoded data : \n", encoded_data)

## encoded_data can be passed to GPT and after getting back the response it will be decoded using decode_df() method

original_data = bc.decode_in_ratio(encoded_data,ratio)  #decode_str takes 2 parameters which are the encoded_data and encoding and returns the original json
print("Original data : \n",original_data)
```

Output
```python
Encoded data : 
 {'key1': 560, 'key2': 1120, 'key3': 'Hello', 'key4': 175.84, 'key5': [56, 112, 168], 'key6': {'nested_key': 'nested_value'}, 'key8': '2022-01-01', 'key9': None, 'key10': {'sub_key1': 280, 'sub_key2': 'world'}, 'key11': [252.0, 375.2, 498.40000000000003], 'key12': 0, 'key13': '42', 'key14': ['apple', 'banana', 'cherry'], 'key15': {'nested_key2': [56, 112, 168]}, 'key16': 435.12, 'key17': 'test', 'key18': {'sub_key3': 'value3', 'sub_key4': 560}, 'key19': [56, 0], 'key20': 691320}

Original data : 
 {'key1': 10.0, 'key2': 20.0, 'key3': 'Hello', 'key4': 3.14, 'key5': [1.0, 2.0, 3.0], 'key6': {'nested_key': 'nested_value'}, 'key8': '2022-01-01', 'key9': None, 'key10': {'sub_key1': 5.0, 'sub_key2': 'world'}, 'key11': [4.5, 6.7, 8.9], 'key12': 0.0, 'key13': '42', 'key14': ['apple', 'banana', 'cherry'], 'key15': {'nested_key2': [1.0, 2.0, 3.0]}, 'key16': 7.7700000000000005, 'key17': 'test', 'key18': {'sub_key3': 'value3', 'sub_key4': 10.0}, 'key19': [1.0, 0.0], 'key20': 12345.0}
```




### Encoding and Decoding values and passing it to OPENAI 

Pass your data to OPENAI without leaking your sensitive data.

```python
from bc_endecoder.replace import BaseCoder
from bc_endecoder.extract import extract_pdf
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def gpt_call(data):
    client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))   
    response1 = client.chat.completions.create(
            messages=[{"role": "system", "content": f"""You are a Convert the given {data} to csv format"""},
                    {"role": "user", "content": '''Just convert the given text into csv format, and return the output'''}],
            model="gpt-4",
            temperature=0
        )
    output=response1.choices[0].message.content
    return output

bc = BaseCoder()

data = extract_pdf("Dummy.pdf") # Extracting PDF data using the function from bc_endecoder package
print('PDF data : \n',data)

encoded_data, encodings = bc.encode_str(data) # Encoding the data and get the encoded data with their encodings
print('\nEncoded Data from Package : \n',encoded_data)

gpt_response = gpt_call(encoded_data) # Calling GPT-4 API to get the response from the encoded data
print('\nGPT Response :\n'+gpt_response)

decoded_data = bc.decode_str(gpt_response, encodings) # Decoding the encoded data and get your original data
print('\nDecoding the Encoded Values : \n',decoded_data)

```
Download the [Dummy.pdf](https://github.com/Distructor2404/BC-en-de-coder/blob/4452b436b3bf21bee1847236c357c317825077da/Dummy.pdf?raw=true) file used in the above code


Output
```python
PDF data : 
 Blenheim Chalcot Mumbai Andheri 87656 Phone number - 9878787878 Date : 23-02-2024  Invoice Statement  HSBC bank Mumbai Andheri 787656  Account Holder: Abhishek Kumar Singh Account Number: 438743894378 Statement Period: 23-01-2024 to 15-01-2024  ----------------------------------------------------------------------------------------------------------  |    Date    |   Description   |   Withdrawals   |   Deposits   |   Balance   | |------------|------------------|------------------|--------------|-------------| | 2023-01-01 | Opening Balance  |        -         |    $10,000    |   $10,000   | | 2023-01-05 | Payment received |        -         |    $5,000     |   $15,000   | | 2023-01-10 | Grocery Shopping |      $200        |       -       |   $14,800   | | 2023-01-15 | Salary Deposit   |        -         |   $8,000     |   $22,800   | | 2023-01-25 | Utility Bill     |      $100        |       -       |   $22,700   | | 2023-01-31 | Monthly Fee      |      $10         |       -       |   $22,690   |  ----------------------------------------------------------------------------------------------------------  Ending Balance: $22,690  Thank you for choosing HSBC Bank. If you have any questions, please contact our customer support at 8927348737. 

Encoded Data from Package : 
 Blenheim Chalcot Mumbai Andheri 401363147298 Phone number - 906449033591 Date : 338480365517-280971266531-390031187131  Invoice Statement  HSBC bank Mumbai Andheri 466271837735  Account Holder: Abhishek Kumar Singh Account Number: 300534140052 Statement Period: 338480365517-170754211816-390031187131 to 939324337053-170754211816-390031187131  ----------------------------------------------------------------------------------------------------------  |    Date    |   Description   |   Withdrawals   |   Deposits   |   Balance   | |------------|------------------|------------------|--------------|-------------| | 120522004913-170754211816-170754211816 | Opening Balance  |        -         |    $237668946781,294663348315    |   $237668946781,294663348315   | | 120522004913-170754211816-027682990558 | Payment received |        -         |    $877646736189,294663348315     |   $939324337053,294663348315   | | 120522004913-170754211816-237668946781 | Grocery Shopping |      $905935621694        |       -       |   $255360822746,100094946280   | | 120522004913-170754211816-939324337053 | Salary Deposit   |        -         |   $511972984598,294663348315     |   $804636746266,100094946280   | | 120522004913-170754211816-755648715445 | Utility Bill     |      $068679160933        |       -       |   $804636746266,517699474565   | | 120522004913-170754211816-243591450716 | Monthly Fee      |      $237668946781         |       -       |   $804636746266,559182488649   |  ----------------------------------------------------------------------------------------------------------  Ending Balance: $804636746266,559182488649  Thank you for choosing HSBC Bank. If you have any questions, please contact our customer support at 550092238315. 

GPT Response :
"Date","Description","Withdrawals","Deposits","Balance"
"120522004913-170754211816-170754211816","Opening Balance","-","$237668946781,294663348315","$237668946781,294663348315"
"120522004913-170754211816-027682990558","Payment received","-","$877646736189,294663348315","$939324337053,294663348315"
"120522004913-170754211816-237668946781","Grocery Shopping","$905935621694","-","$255360822746,100094946280"
"120522004913-170754211816-939324337053","Salary Deposit","-","$511972984598,294663348315","$804636746266,100094946280"
"120522004913-170754211816-755648715445","Utility Bill","$068679160933","-","$804636746266,517699474565"
"120522004913-170754211816-243591450716","Monthly Fee","$237668946781","-","$804636746266,559182488649"

Decoding the Encoded Values : 
 "Date","Description","Withdrawals","Deposits","Balance"
"2023-01-01","Opening Balance","-","$10,000","$10,000"
"2023-01-05","Payment received","-","$5,000","$15,000"
"2023-01-10","Grocery Shopping","$200","-","$14,800"
"2023-01-15","Salary Deposit","-","$8,000","$22,800"
"2023-01-25","Utility Bill","$100","-","$22,700"
"2023-01-31","Monthly Fee","$10","-","$22,690"
```
Download the above response by clicking [here](https://github.com/Distructor2404/BC-en-de-coder/blob/4452b436b3bf21bee1847236c357c317825077da/Response.txt?raw=true) 



