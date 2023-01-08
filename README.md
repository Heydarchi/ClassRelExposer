# AOSP-Internal-Relationship
AOSP internal from packages/classes relationship perspective



### To run the project locally it's needed to have python 3.x and some other packages installed on your local machine
&ensp;
>To install Python 3.8 or new version
```
sudo apt install python3.8
```
&ensp;
> To install PythonIsPython3
```
sudo apt-get install python-is-python3 -y
```
&ensp;
> To install graphviz
```
sudo apt-get install graphviz
```
<br/>

### **How to run**
After the packages above are installed go to the Analyzer folder and run the command below
    ```
    python FileAnalyzer.py [folder/file path]
    ```
#### **To run sample**
```
python FileAnalyzer.py ../sample
```
>The result can be found in the **out** folder
&ensp;

<br/>

### TODO:
#### - Separate the variables  of Class & Method
#### - Detect the cascade classes
#### - Make a list of primitive variable types