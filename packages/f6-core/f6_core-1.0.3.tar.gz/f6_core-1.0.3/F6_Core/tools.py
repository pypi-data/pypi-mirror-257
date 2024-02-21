# Copyright 2024 Degtyarev Ivan

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Any

dirname, filename = os.path.split(os.path.abspath(__file__))


class ConfigManager():
    __slots__ = ('parametrs', 'path', 'config_name',)
    VERSION = '1.0.0'
    DEFALTE = {}
    
    TYPE = {
            '-1': lambda x: None,
            None: -1,
            '0': lambda x: str(x),
            str: 0,
            '1': lambda x: int(x),
            int: 1,
            '2': lambda x: float(x),
            float: 2,
        }
    
    def __init__(self, path, config_name='CONFIG', **kwargs) -> None:
        self.path = path
        self.config_name = config_name 
        self.parametrs = {}
        
        kwargs |= self.DEFALTE
        
        for k, v in kwargs.items():
            if str(k).isidentifier():
                self.parametrs[k] = v
                
    def __getattribute__(self, __name: str) -> Any:
        if __name == 'parametrs':
            return object.__getattribute__(self, __name)
        if hasattr(self, 'parametrs'):
            if __name in self.parametrs:
                return self.parametrs.get(__name)
        return object.__getattribute__(self, __name)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'parametrs':
            return object.__setattr__(self, __name, __value)
        if hasattr(self, 'parametrs'):
            self.parametrs[__name] = __value
            return None
        return object.__setattr__(self, __name, __value)
            
    def load_config(self):
        with open(os.path.join(self.path, self.config_name), 'r') as f:
            date = f.readlines()
            for item in range(len(date)):
                if item == 0:
                    # print(date[item])
                    continue
                if date[item].strip():
                    k, v = self.deserializ_item(date[item])
                    if str(k).isidentifier():
                        self.parametrs[k] = v
   
    
    def dump_config(self):
        with open(os.path.join(self.path, self.config_name), 'w') as f:
            f.write(f'--- ConfigManager v{self.VERSION} --- \n')
            for k, v in self.parametrs.items():
                f.write(self.serializ_item(k, v))           
            
    @staticmethod        
    def serializ_item(key: str, value: int|float|str|None) -> str:
        return f'{str(key)}={str(value)}[{str(ConfigManager.TYPE.get(type(value), "-1"))}];\n'
    
    @staticmethod        
    def deserializ_item(item: str) -> tuple:
        key, value = item.strip().split('=')
        return str(key), ConfigManager.TYPE.get(value.split('[')[1].split(']')[0], ConfigManager.TYPE['0'])(value.split('[')[0])
    
    
