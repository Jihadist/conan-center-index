from conans import ConanFile, CMake, tools
import os

class ZintConan(ConanFile):
    name = "libzint"
    description = "Zint Barcode Generator"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/VarLog/zint"
    license = "GPL-3.0"
    topics = ("conan", "barcode", "qt")
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = "cmake", "cmake_find_package"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False, 
        "fPIC": True,
        "qt:qttools": True
    }
    _cmake = None
   
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        self.requires("libpng/1.6.37")
        self.requires("zlib/1.2.11")
        self.requires("qt/5.15.2")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version 
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["DESIRED_QT_VERSION"] = "5"
        self._cmake.configure()
        return self._cmake

    def build(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs=[os.path.join('include', 'libzint-{}'.format(self.version))]
        if not self.options.shared:
            self._cmake.definitions["ZINT_STATIC"] = "ON"

        self.cpp_info.filenames["cmake_find_package"] = "libzint"
        self.cpp_info.filenames["cmake_find_package_multi"] = "libzint"
        self.cpp_info.names["cmake_find_package"] = "libzint"
        self.cpp_info.names["cmake_find_package_multi"] = "libzint"
