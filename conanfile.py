from conans import ConanFile, CMake, tools
import os


class CroaringConan(ConanFile):
    name = "CRoaring"
    version = "0.2.63"
    license = "MIT"
    author = "<Put your name here> <And your email here>"
    url = "https://dl.bintray.com/bldrvnlw/conan-repo/CRoaring"
    description = "CRoaring is to provide a high performance low-level implementation of bitmaps that fully take advantage of the latest hardware."
    topics = ("bitsets", "bitmaps", "compressed")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/RoaringBitmap/CRoaring.git")
        os.chdir("./CRoaring")
        self.run("git checkout tags/v{0}".format(self.version))
        os.chdir("..")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CRoaring/CMakeLists.txt", "project(RoaringBitmap)",
                              '''project(RoaringBitmap)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="CRoaring")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        os.chdir("CRoaring/include")
        self.copy("*.h", src="CRoaring/include", dst="include", keep_path=True)
        self.copy("*.hpp", src="CRoaring/include", dst="include", keep_path=True)       
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        os.chdir("../..")
        self.copy("*.h", src="CRoaring/cpp", dst="include", keep_path=False)
        self.copy("*.hpp", src="CRoaring/cpp", dst="include", keep_path=False) 


