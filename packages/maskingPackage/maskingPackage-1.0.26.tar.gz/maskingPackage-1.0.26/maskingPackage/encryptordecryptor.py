import pandas as pd
from cryptography.fernet import Fernet
import json
from pyspark.sql.types import StringType
from pyspark.sql.functions import col, udf
from pyspark.sql import functions as F
import re



class DataEncryptorDecryptor:
    def __init__(self, decryptionkey,data,generated_json):
        self.decryptionkey = decryptionkey
        self.data = data
        self.generated_json = generated_json
#fromat encrypt_data(dataframe,column_to_encrypt = ["col1","col2"])
    def encrypt_data(self,decryption_columns,data):  
        data1 = data 
        if isinstance(data1, pd.DataFrame):  
            data = data1  
        else:  
            data = data1.toPandas()  
  
        key = self.decryptionkey  
        cipher_suite = Fernet(key)  
  
        for column in decryption_columns:  
            original_column_name = column.rsplit('_encrypted', 1)[0]  
            new_column_name = f"{original_column_name}"  
            cipher_suite = Fernet(key)  
            data[new_column_name] = data[original_column_name].apply(  
                lambda x: cipher_suite.encrypt(str(x).encode()).decode() if pd.notnull(x) else x  
            )  
         
        return data
    def decrypt_data(self, sensitive_columns, dataset):
        # dataset = pd.read_csv(masked_encrypted_csv_path, low_memory=False)

        decryption_key = self.decryptionkey
        if decryption_key:
            cipher_suite = Fernet(decryption_key)
            for sensitive_column in sensitive_columns:
                dataset[sensitive_column] = dataset[sensitive_column].apply(
                    lambda x: cipher_suite.decrypt(x.encode()).decode()
                )
        else:
            print("Decryption key not valid")

        return dataset
# masks the data
    def masking_all_column(self, encrypted_dataset):
        init_result= self.generated_json
        def mask_column_with_function(pd_column, function):
            exec(function, globals())
            masked_column = pd_column.apply(maskInfo)
            return masked_column

        # init_result = self.generated_json
        maskeddata = encrypted_dataset.copy()

        for col_info in init_result['content']:
            col_name = col_info['columnName']
            if col_info.get('sensitivity') == 1:
                print(f"Applying masking to sensitive column: {col_name}...")
                maskeddata[col_name] = mask_column_with_function(maskeddata[col_name], col_info['function'])
            else:
                print(f"Skipping non-sensitive column: {col_name}")

        return maskeddata
# This handles both encryption and masking logic together 
    # def encryption_masking(self):
    #     data1 = self.data
    #     if  isinstance(data1, pd.DataFrame):
    #         data = data1
    #     else:
    #         data = data1.toPandas()

    #     def mask_column_with_function(pd_column, function):
    #         exec(function, globals())
    #         # masked_column = pd_column.apply(maskInfo)
    #         masked_column = pd_column.astype(str).apply(maskInfo)
    #         # masked_column = pd_column.apply(lambda x: maskInfo(x))
    #         return masked_column
    #     key = self.decryptionkey
    #     cipher_suite = Fernet(key)
    #     init_result = self.generated_json
    #     sensitive_columns = []
    #     masking_functions = {}

    #     for column_info in init_result["content"]:
    #         if column_info["sensitivity"] == 1:
    #             column_name = column_info["columnName"]
    #             masking_function = column_info["function"]
    #             sensitive_columns.append(column_name)
    #             masking_functions[column_name] = masking_function
            
    #     if sensitive_columns:
    #         key = self.decryptionkey
    #         for column in sensitive_columns:
    #             new_column_name = f"{column}_encrypted"
    #             cipher_suite = Fernet(key)
    #             data[new_column_name] = data[column].apply(lambda x: cipher_suite.encrypt(str(x).encode()).decode() if isinstance(x, (str, int, float)) else x)
    #             duplicate_mask = data[column_name].notna()  
    #             duplicated_rows = data[duplicate_mask]
    #             duplicated_df = pd.concat([data, duplicated_rows], ignore_index=True)
                
    #             result_df = pd.concat([data, duplicated_df], ignore_index=True)
    #             maskeddata = result_df
    #             for col_info in init_result['content']:
    #                 col_name = col_info['columnName']
                    
    #                 if col_info.get('sensitivity') == 1:          
    #                     maskeddata[col_name] = mask_column_with_function(maskeddata[col_name],col_info['function'])          
    #                 else:
    #                     pass
    #         maskeddata.sort_index(axis=1, inplace=True)
    #         # maskeddata = spark.createDataFrame(maskeddata)
    #         return maskeddata

    def encryption_masking(self):  
        data = self.data if isinstance(self.data, pd.DataFrame) else self.data.toPandas()  
  
        def mask_column_with_function(pd_column, function):  
            exec(function, globals())  
            masked_column = pd_column.astype(str).apply(maskInfo)  
            return masked_column  
  
        key = self.decryptionkey  
        cipher_suite = Fernet(key)  
        init_result = self.generated_json  
        sensitive_columns = []  
        masking_functions = {}  
  
        # Collect sensitive columns and their corresponding masking functions  
        for column_info in init_result["content"]:  
            if column_info["sensitivity"] == 1:  
                column_name = column_info["columnName"]  
                masking_function = column_info["function"]  
                sensitive_columns.append(column_name)  
                masking_functions[column_name] = masking_function  
  
        # Encrypt sensitive columns  
        if sensitive_columns:  
            for column in sensitive_columns:  
                new_column_name = f"{column}_encrypted"  
                # Encrypt the data and store in a new column  
                data[new_column_name] = data[column].apply(  
                    lambda x: cipher_suite.encrypt(str(x).encode()).decode()   
                    if pd.notnull(x)   
                    else x  
                )  
  
            # Apply masking to sensitive columns  
            for column, function in masking_functions.items():  
                data[column] = mask_column_with_function(data[column], function)  
                masked_column_name = f"{column}_masking"  
                data.rename(columns={column: masked_column_name}, inplace=True)  
   
        data.sort_index(axis=1, inplace=True)  
  

        # display(data)  
  
        # Remove '_encrypted' from the column names after processing  
        for col in data.columns:  
            if col.endswith('_encrypted'):  
                new_col_name = col.replace('_encrypted', '')  
                data.rename(columns={col: new_col_name}, inplace=True)  
   
  
        return data 

    # def encryption_masking(self):
    #     data1 = self.data
    #     if  isinstance(data1, pd.DataFrame):
    #         data = data1
    #     else:
    #         data = data1.toPandas()

    #     def mask_column_with_function(pd_column, function):
    #         exec(function, globals())
    #         # masked_column = pd_column.apply(maskInfo)
    #         masked_column = pd_column.astype(str).apply(maskInfo)
    #         # masked_column = pd_column.apply(lambda x: maskInfo(x))
    #         return masked_column
    #     key = self.decryptionkey
    #     cipher_suite = Fernet(key)
    #     init_result = self.generated_json
    #     sensitive_columns = []
    #     masking_functions = {}

    #     for column_info in init_result["content"]:
    #         if column_info["sensitivity"] == 1:
    #             column_name = column_info["columnName"]
    #             masking_function = column_info["function"]
    #             sensitive_columns.append(column_name)
    #             masking_functions[column_name] = masking_function
            
    #     if sensitive_columns:
    #         key = self.decryptionkey
    #         for column in sensitive_columns:
    #             new_column_name = f"{column}_encrypted"
    #             cipher_suite = Fernet(key)
    #             data[new_column_name] = data[column].apply(lambda x: cipher_suite.encrypt(str(x).encode()).decode() if isinstance(x, (str, int, float)) else x)
    #             duplicate_mask = data[column_name].notna()  
    #             duplicated_rows = data[duplicate_mask]
    #             duplicated_df = pd.concat([data, duplicated_rows], ignore_index=True)
                
    #             result_df = pd.concat([data, duplicated_df], ignore_index=True)
    #             maskeddata = result_df
    #             for col_info in init_result['content']:
    #                 col_name = col_info['columnName']
                    
    #                 if col_info.get('sensitivity') == 1:          
    #                     maskeddata[col_name] = mask_column_with_function(maskeddata[col_name],col_info['function'])  
    #                     masked_column_name = f"{col_name}_masking" 
    #                     maskeddata.rename(columns={col_name: masked_column_name}, inplace=True)         
    #                 else:
    #                     pass
    #         maskeddata.sort_index(axis=1, inplace=True)  
    #         for col in maskeddata.columns:  
    #             # Check if the column name ends with '_encrypted'  
    #             if col.endswith('_encrypted'):  
    #                 # Remove '_encrypted' from the column name  
    #                 new_col_name = col.replace('_encrypted', '')  
    #                 # Rename the column  
    #                 maskeddata.rename(columns={col: new_col_name}, inplace=True) 
    #         # maskeddata = spark.createDataFrame(maskeddata)
    #         return maskeddata



    def decryption(self,sensitive_columns,dataset):
        for sensitive_column in sensitive_columns:
            decryption_key = self.decryptionkey
            if decryption_key:
                cipher_suite = Fernet(decryption_key)

                # Define a UDF for decryption
                def decrypt_udf(value):
                    if value is not None:
                        return cipher_suite.decrypt(value.encode()).decode()
                    else:
                        return None

                dataset = dataset.withColumn(
                    sensitive_column,
                    F.udf(decrypt_udf, StringType())(dataset[sensitive_column])
                )
            else:
                print("Decryption key not valid")
        for column in dataset.columns:
            if column.endswith('_encrypted') and column in sensitive_columns:
                    new_column_name = column.replace('_encrypted', '_decrypted')
                    dataset = dataset.withColumnRenamed(column,new_column_name)
        return dataset
    
  
    def encrypt_multiple_columns(self, data1, columns_to_encrypt):  
        # data1 = data
        if isinstance(data1, pd.DataFrame):  
            data = data1  
        else:
            data = data1.toPandas()  
        key = self.decryptionkey
        init_result = self.generated_json
        cipher_suite = Fernet(key)  
        sensitive_columns = []  
        masking_functions = {}  
    
        for column_info in init_result["content"]:  
            if column_info["sensitivity"] == 1:  
                column_name = column_info["columnName"]  
                masking_function = column_info["function"]  
                sensitive_columns.append(column_name)  
                masking_functions[column_name] = masking_function  
    
        if columns_to_encrypt is None:  
            columns_to_encrypt = sensitive_columns  
    
        if sensitive_columns:  
            for column in sensitive_columns:  
                if column in columns_to_encrypt:  
                    # Encrypt only the columns specified by the user  
                    data[f"{column}_encrypted"] = data[column].apply(  
                        lambda x: cipher_suite.encrypt(str(x).encode()).decode() if isinstance(x, (str, int, float)) else x  
                    )  
            result_df = data  
        else:  
            result_df = data.copy()  
        decrypted_columns_to_drop = [f"{col}_decrypted" for col in columns_to_encrypt]  
  
        # Drop each decrypted column if it exists  
        for decrypted_column_name in decrypted_columns_to_drop:  
            if decrypted_column_name in data.columns:  
                # print("Dropping column:", decrypted_column_name)  
                data.drop(decrypted_column_name, axis=1, inplace=True)  
      
        return result_df

  
  
    def process_dataframe(self):  
        init_result = self.generated_json
        df = self.data
        decryption_key = self.decryptionkey
        # Nested function to mask a column with the given function  
        def mask_column_with_function(df, column_name, function_str, is_pyspark_df):  
            if is_pyspark_df:  
                # Define a UDF based on the function string  
                exec(f'@udf(returnType=StringType())\ndef mask_udf(value):\n\treturn {function_str}', globals())  
                # Apply the UDF to the column  
                masked_column = df.withColumn(column_name, mask_udf(df[column_name]))  
            else:  
                # Define the masking function  
                exec(function_str, globals())  
                # Apply the masking function to the pandas column  
                masked_column = df[column_name].astype(str).apply(maskInfo)  
                df[column_name] = masked_column  
            return df  
        
        sensitive_columns = []  
        masking_functions = {}  
    
        for column_info in init_result["content"]:  
            if column_info["sensitivity"] == 1:  
                column_name = column_info["columnName"]  
                sensitive_columns.append(column_name)  
                masking_functions[column_name] = column_info["function"]  
        
        is_pyspark_df = isinstance(df, pyspark.sql.dataframe.DataFrame)  
        
        if sensitive_columns:  
            cipher_suite = Fernet(decryption_key)  
            for column in sensitive_columns:  
                new_column_name = f"{column}_encrypted"  
                if is_pyspark_df:  
                    encrypt_udf = udf(lambda x: cipher_suite.encrypt(str(x).encode()).decode() if x is not None else None, StringType())  
                    df = df.withColumn(new_column_name, encrypt_udf(df[column]))  
                else:  
                    df[new_column_name] = df[column].apply(lambda x: cipher_suite.encrypt(str(x).encode()).decode() if isinstance(x, (str, int, float)) else x)  
        
            for column_name, function_str in masking_functions.items():  
                df = mask_column_with_function(df, column_name, function_str, is_pyspark_df)  
        
        if not is_pyspark_df:  
            df.sort_index(axis=1, inplace=True)  
        
        return df  
  
# Usage example:  
# Assume 'data' is either a PySpark DataFrame or a pandas DataFrame  
# Assume 'init_result' is a dictionary containing the necessary configuration  
# Assume 'decryption_key' is the key used for decryption  
# processed_data = process_dataframe(data, init_result, decryption_key)  
 
  
# Usage example:  
# Assume 'data' is either a PySpark DataFrame or a pandas DataFrame  
# Assume 'init_result' is a dictionary containing the necessary configuration  
# Assume 'decryption_key' is the key used for decryption  
# processed_data = process_dataframe(data, init_result, decryption_key)  

            # for sensitive_column in sensitive_columns:
            #     decryption_key = self.decryptionkey
            #     if decryption_key:
            #         cipher_suite = Fernet(decryption_key)

            #         # Define a UDF for decryption
            #         def decrypt_udf(value):
            #             if value is not None:
            #                 return cipher_suite.decrypt(value.encode()).decode()
            #             else:
            #                 return None
            #         dataset = dataset.withColumn(
            #             sensitive_column,
            #             F.udf(decrypt_udf, StringType())(dataset[sensitive_column])
            #         )
            #     else:
            #         print("Decryption key not valid")
            # for columnrename in dataset:
                
            # return dataset

