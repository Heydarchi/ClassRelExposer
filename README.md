# ClassRelExposer
The aim of this python project is to find and exposing the class relationship

### The supported languages are:
- C++
- Java 
- CSharp (C#)

<br/>

The code is tested for Java but not that much for C++ and C-Sharp. Of course, it is not completed yet and has some flaws and issues in processing. Very welcome to report or any kind of contribution.

Feel free to create a ticket or send me a message/report.

<br/>

### PlantUml

Generating the PNG files is based on [PlantUml](http://www.plantuml.com) that I put a jar version in this project.


## Installation
#### Note : The 1st & 2nd steps can be skipped by running the `setup.sh` script.
```
./setup.sh
```
&ensp;
1. Install Python 3.8 or a newer version, PythonIsPython3, Graphviz, and PyQt5:

```
sudo apt install python3.8 python-is-python3 graphviz -y
```
&ensp;

2. Install python packages

```
pip install -r requirements.txt
```
&ensp;

3. Clone the project and its submodule:

```
git clone https://github.com/Heydarchi/ClassRelExposer.git
```
&ensp;

4. Inside the cloned folder, run the following command to update the submodule:

```
git submodule update --init --recursive
```
<br/>

## **How to run**
After the packages above are installed go to the Analyzer folder and run the command below
```
python FileAnalyzer.py [folder/file path]
```
#### **To run sample** 

```
python FileAnalyzer.py ../sample
```

>The result can be found in the **out** folder

<br/>

### TODO:
- [ ] Separate the variables  of Class & Method
- [ ] Detect the cascade classes
- [ ] Make a list of primitive variable types
- [ ] Put the project architecture diagram
- [ ] CSharp is semi tested 
- [ ] Need to have recursive analysis 