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


## Steps to utilize the project
### 1- To run the project locally it's needed to have python 3.x and some other packages installed on your local machine
&ensp;
> Install Python 3.8 or new version
```
sudo apt install python3.8
```
&ensp;
> Install PythonIsPython3
```
sudo apt-get install python-is-python3 -y
```
&ensp;
> Install graphviz
```
sudo apt-get install graphviz
```
<br/>

### 2- Clone the project & the submodule
```
git clone https://github.com/Heydarchi/ClassRelExposer.git
```
Run the command below inside the cloned folder
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