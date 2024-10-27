add_rules("mode.release") -- ("mode.debug") -- , "mode.release")
-- https://xmake.io/#/guide/project_examples?id=integrating-the-c-modules-package
set_languages("c++20")

add_requires("benchmark")
--[[ add_requires("yaml-cpp") ]]
-- add_requires("eigen")
--[[ add_requires("scatter master") ]]
-- add_requires("conan::cairomm/1.18.0")
-- add_requires("conan::pangomm/2.54.0")
-- add_requires("brew::cairomm 1.18.0")
-- add_requires("brew::pangomm 2.46.2")
-- , {system = true})
-- , {system = true})
-- add_requires("cairomm", {system = true})
-- add_requires("pangomm", {system = true})

local my_download = function (package, opt)
   import("net.http")
   import("utils.archive")

   local url = opt.url
   local sourcedir = opt.sourcedir
   local packagefile = path.filename(url)
   local sourcehash = package:sourcehash(opt.url_alias)

   local cached = true
   if not os.isfile(packagefile) or sourcehash ~= hash.sha256(packagefile) then
       cached = false

       -- attempt to remove package file first
       os.tryrm(packagefile)
       http.download(url, packagefile)

       -- check hash
       if sourcehash and sourcehash ~= hash.sha256(packagefile) then
           raise("unmatched checksum, current hash(%s) != original hash(%s)", hash.sha256(packagefile), sourcehash:sub(1, 8))
       end
   end

   -- extract package file
   local sourcedir_tmp = sourcedir .. ".tmp"
   os.rm(sourcedir_tmp)
   if archive.extract(packagefile, sourcedir_tmp) then
       os.rm(sourcedir)
       os.mv(sourcedir_tmp, sourcedir)
   else
       -- if it is not archive file, we need only create empty source file and use package:originfile()
       os.tryrm(sourcedir)
       os.mkdir(sourcedir)
   end

   -- save original file path
   package:originfile_set(path.absolute(packagefile))
end

-- package("scatter")
--   set_urls("https://gitlab.com/tloew/scatter/-/archive/$(version)/scatter-$(version).tar.gz")
--   add_versions("master", "329e3b255f762fb694ecc3b83ee3b49ebbbab634ba87579c9eabc0185619b023")
--   add_versions("v0.1.0", "d1738773c3b38653ba143d55d64deeead084d29db933d2bf82c4e22441fad6dc")

--   on_download(my_download)
--   
--   on_install(function (package)
--       local configs = {}
--       -- table.insert(configs, "-DCMAKE_BUILD_TYPE=" .. (package:debug() and "Debug" or "Release"))
--       -- table.insert(configs, "-DBUILD_SHARED_LIBS=" .. (package:config("shared") and "ON" or "OFF"))
--       import("package.tools.cmake").install(package, configs)
--   end)
--   -- on_test(function (package)
--   --     assert(package:has_cfuncs("add", {includes = "foo.h"}))
--   -- end)
-- package_end()

package("gabench")
  set_sourcedir(os.scriptdir())

  add_deps("benchmark")

  on_install(function (package)
    local configs = {}
    table.insert(configs, "-DCMAKE_BUILD_TYPE=" .. "Release")
    -- table.insert(configs, "-DBUILD_SHARED_LIBS=" .. (package:config("shared") and "ON" or "OFF"))
    import("package.tools.cmake").install(package,configs)
  end)
package_end()

add_requires("gabench")

target("bench")
  set_kind("phony")
  add_deps("gabench")
  -- add_deps("cmake")

  on_run(function (target)
    -- Package:addenv("benchmark_DIR", "")
-- mkdir build
-- cd build
-- cmake -DCMAKE_BUILD_TYPE=Release ..
-- cmake --build . --parallel 8
    -- os.run("mkdir -p build")
    -- os.cd("build")
    -- os.run("cmake -DCMAKE_BUILD_TYPE=Release ..")
    -- os.run("cmake --build . --parallel 8")
  end)

