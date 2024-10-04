import os
import time
import json
import inspect

#SHARETYPES = [bool, int, float, str, dict, list]

class DevPrototype:

    # Prototype 
    def introspect_class(self, cls):
        print(f"Introspecting class: {cls.__name__}\n")

        # Print the docstring of the class
        print(f"Docstring: {inspect.getdoc(cls)}\n")

        # Print the methods of the class
        print("Methods:")
        for name, method in \
                inspect.getmembers(cls, predicate=inspect.isfunction):
            print(f" - {name}: {inspect.getdoc(method)}")

        # Print the inheritance hierarchy
        print("\nInheritance Hierarchy:")
        for base_class in inspect.getmro(cls):
            print(f" - {base_class.__name__}")
    # Upgraded
    def classinfo(self, cls0=None):
        #"""
        #if cls0== None: 
        #    cls0 = self.__class__
        #        
        #if type(cls0) == type:
        #    cls = cls0
        #else:
        #    cls = cls0.__class__
        #    if type(cls) == type:
        #        cls = cls0
        #    else:
        #        return f" {cls} is not class or instance: {type(cls)}"
        #"""

        if cls0== None: 
            cls = self.__class__
        elif type(cls0) == type:
            cls = cls0
        else:
            cls = cls0.__class__
            
        assert type(cls) == type, \
           f" {cls} is not class or instance: {type(cls)}"
        
        #print(f"{dir(cls)}")
        message = f"Class inspection: {cls.__name__}\n\n"
        message += f"Docstring: {inspect.getdoc(cls)}\n\n"
        
        message += "Variables:\n"
        class_vars = {name: attr for name, attr in cls.__dict__.items() if not (name.startswith('__') and name.endswith('__')) and not inspect.isfunction(attr)}
        for name, value in class_vars.items():
            message += f" - {name}: {value}\n"
            
        message += "Methods:\n"
        for name, method in \
                inspect.getmembers(cls, predicate=inspect.isfunction):
            message += f" - {name}: {inspect.getdoc(method)}\n"

        # Print the inheritance hierarchy
        message += "Inheritance Hierarchy:\n"
        for base_class in inspect.getmro(cls):
            message += f" - {base_class.__name__}\n"          
            
        return message

    def info(self):
        return self.classinfo(self.__class__)

    def share(self):

        #print("----for share--:")
        class_vars = {}
        class_vars["timestamp"] = time.time()
        class_vars["dev_name"] = self.__class__.__name__
  

        cls = self.__class__
        instance_vars = {name: attr for name, attr in cls.__dict__.items() if not (name.startswith('__') and name.endswith('__')) and not inspect.isfunction(attr)}
        for name, value in instance_vars.items():
            try:
                json.dumps(value)
                class_vars[name] = value
            except:
                #print(f"Skipped {value} for {name}: Not a valid JSON file.")
                continue

        
        instance_vars = vars(self)
        for name, value in instance_vars.items():
            try:
                json.dumps(value)
                class_vars[name] = value
            except:
                #print(f"Skipped {value} for {name}: Not a valid JSON file.")
                if name in class_vars.keys(): class_vars.pop(name, None)
                continue
                
            class_vars[name] = value
        """        
        class_vars = {name: value \
            for name, value in vars(self) \
               if type(value) in [int, float, str]}
        """
        try:
            sharepath = "/dev/shm/station/"
            if not os.path.exists(sharepath):
                os.makedirs(sharepath)
            filepath = os.path.join(sharepath, str(self.__class__.__name__))
            max_attempts = 10
            for attempt in range(max_attempts):
                try:
                    # 'w+' 모드로 파일 열기 시도
                    with open(filepath, "w+") as fp:
                        json.dump(class_vars, fp)
                        break  # 성공시 반복문 종료
                except IOError as e:
                    print(f"Attempt {attempt + 1}: Error opening file {filepath}: {e}")
                    if attempt < max_attempts - 1:  # 마지막 시도가 아니라면
                        time.sleep(0.1)  # 0.1초 대기
                    else:
                        print(f"Failed to open file after {max_attempts} attempts.")
                except PermissionError as e:
                    print(f"Permission denied for file {filepath}: {e}")
                    break  # 권한 문제는 재시도가 의미 없으므로 종료except Exception as e:
        except Exception as e:
            print(f"Error to write status {__name__} {e}")
if __name__ == "__main__":
    cls = DevPrototype()
    print(cls.classinfo(cls.__class__))
    print("------------------")
    cls.introspect_class(cls.__class__)
        
