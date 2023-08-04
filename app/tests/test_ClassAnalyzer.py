from unittest import TestCase
from analyzer.ClassAnalyzer import ClassAnalyzer
from model.AnalyzerEntities import FileTypeEnum
from PythonUtilityClasses.FileReader import FileReader

class TestClassAnalyzer(TestCase):
    def test_init_patterns(self):
        # Check if the variables are initialized properly
        classAnalyzer = ClassAnalyzer()
        self.assertNotEqual(classAnalyzer.pattern, None)

    #def test_analyze(self):
    #    self.fail()

    def test_extract_class_name_java(self):
        # Check if the class name is extracted properly in a Java input string
        classAnalyzer = ClassAnalyzer()
        inputStr = "public class TestClass {"
        className = classAnalyzer.extractClassName(FileTypeEnum.JAVA, inputStr)
        self.assertEqual(className, "TestClass")

    def test_extract_class_name_java_with_inheritance(self):
        # Check if the class name is extracted properly in a Java input string with inheritance
        classAnalyzer = ClassAnalyzer()
        inputStr = "public class TestClass extends AbstractTestClass2 implements SuperTestClass{"
        className = classAnalyzer.extractClassName(FileTypeEnum.JAVA, inputStr)
        self.assertEqual(className, "TestClass")

    def test_extract_class_name_cpp(self):
        # Check if the class name is extracted properly in a C++ input string
        classAnalyzer = ClassAnalyzer()
        inputStr = "class TestClass {"
        className = classAnalyzer.extractClassName(FileTypeEnum.CPP, inputStr)
        self.assertEqual(className, "TestClass")

    def test_extract_class_name_cpp_with_inheritance(self):
        # Check if the class name is extracted properly in a C++ input string with inheritance
        classAnalyzer = ClassAnalyzer()
        inputStr = "class TestClass : public AbstractTestClass2, public SuperTestClass {"
        className = classAnalyzer.extractClassName(FileTypeEnum.CPP, inputStr)
        self.assertEqual(className, "TestClass")

    #def test_extract_class_inheritances(self):
    #    self.fail()

    #def test_extract_class_spec(self):
    #    self.fail()
