from unittest import TestCase
from analyzer.ClassAnalyzer import ClassAnalyzer
from model.AnalyzerEntities import FileTypeEnum
from PythonUtilityClasses.FileReader import FileReader
import re


class TestClassAnalyzer(TestCase):
    def test_init_patterns(self):
        # Check if the variables are initialized properly
        classAnalyzer = ClassAnalyzer()
        self.assertNotEqual(classAnalyzer.pattern, None)

    def test_find_class_pattern_java(self):
        # Check if the class pattern is found correctly in a Java input string
        classAnalyzer = ClassAnalyzer()
        inputStr = "public class TestClass {"

        for pattern in classAnalyzer.pattern[FileTypeEnum.JAVA]:
            match = classAnalyzer.find_class_pattern(pattern, inputStr)
            self.assertEqual(
                inputStr[match.start() : match.end()], "public class TestClass {"
            )

    def test_find_class_pattern_java_with_inheritance(self):
        # Check if the class pattern is found correctly in a Java input string with inheritance
        classAnalyzer = ClassAnalyzer()
        inputStr = "public class TestClass extends AbstractTestClass2 implements SuperTestClass{"
        for pattern in classAnalyzer.pattern[FileTypeEnum.JAVA]:
            match = classAnalyzer.find_class_pattern(pattern, inputStr)
            self.assertEqual(
                inputStr[match.start() : match.end()],
                "public class TestClass extends AbstractTestClass2 implements SuperTestClass{",
            )

    def test_find_class_pattern_java_with_inheritance_and_comments(self):
        # Check if the class pattern is found correctly in a Java input string with inheritance and comments
        classAnalyzer = ClassAnalyzer()
        inputStr = "/* This is a comment */ public class TestClass extends AbstractTestClass2 implements SuperTestClass{"
        for pattern in classAnalyzer.pattern[FileTypeEnum.JAVA]:
            match = classAnalyzer.find_class_pattern(pattern, inputStr)
            self.assertEqual(
                inputStr[match.start() : match.end()],
                " This is a comment */ public class TestClass extends AbstractTestClass2 implements SuperTestClass{",
            )

    """    
    def test_find_class_pattern_cpp(self):
        # Check if the class pattern is found correctly in a C++ input string
        classAnalyzer = ClassAnalyzer()
        inputStr = "class TestClass {"
        match = classAnalyzer.findClassPattern(classAnalyzer.pattern[FileTypeEnum.CPP], inputStr)
        self.assertEqual(inputStr[match.start():match.end()], "class TestClass {")

    def test_find_class_pattern_cpp_with_inheritance(self):
        # Check if the class pattern is found correctly in a C++ input string with inheritance
        classAnalyzer = ClassAnalyzer()
        inputStr = "class TestClass : public AbstractTestClass2, public SuperTestClass{"
        match = classAnalyzer.findClassPattern(classAnalyzer.pattern[FileTypeEnum.CPP], inputStr)
        self.assertEqual(inputStr[match.start():match.end()], "class TestClass : public AbstractTestClass2, public SuperTestClass{")

    def test_find_class_pattern_cpp_with_inheritance_and_comments(self):
        # Check if the class pattern is found correctly in a C++ input string with inheritance and comments
        classAnalyzer = ClassAnalyzer()
        inputStr = "/* This is a comment */ class TestClass : public AbstractTestClass2, public SuperTestClass{"
        match = classAnalyzer.findClassPattern(classAnalyzer.pattern[FileTypeEnum.CPP], inputStr)
        self.assertEqual(inputStr[match.start():match.end()], "class TestClass : public AbstractTestClass2, public SuperTestClass{")
    """
    # def test_analyze(self):
    #    self.fail()

    def test_extract_class_name_java(self):
        # Check if the class name is extracted properly in a Java input string
        classAnalyzer = ClassAnalyzer()
        inputStr = "public class TestClass {"
        className = classAnalyzer.extract_class_name(FileTypeEnum.JAVA, inputStr)
        self.assertEqual(className, "TestClass")

    def test_extract_class_name_java_with_inheritance(self):
        # Check if the class name is extracted properly in a Java input string with inheritance
        classAnalyzer = ClassAnalyzer()
        inputStr = "public class TestClass extends AbstractTestClass2 implements SuperTestClass{"
        className = classAnalyzer.extract_class_name(FileTypeEnum.JAVA, inputStr)
        self.assertEqual(className, "TestClass")

    def test_extract_class_name_cpp(self):
        # Check if the class name is extracted properly in a C++ input string
        classAnalyzer = ClassAnalyzer()
        inputStr = "class TestClass {"
        className = classAnalyzer.extract_class_name(FileTypeEnum.CPP, inputStr)
        self.assertEqual(className, "TestClass")

    def test_extract_class_name_cpp_with_inheritance(self):
        # Check if the class name is extracted properly in a C++ input string with inheritance
        classAnalyzer = ClassAnalyzer()
        inputStr = (
            "class TestClass : public AbstractTestClass2, public SuperTestClass {"
        )
        className = classAnalyzer.extract_class_name(FileTypeEnum.CPP, inputStr)
        self.assertEqual(className, "TestClass")

    # def test_extract_class_inheritances(self):
    #    self.fail()

    # def test_extract_class_spec(self):
    #    self.fail()
