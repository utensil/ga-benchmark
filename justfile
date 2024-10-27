pb:
  #!/usr/bin/env bash
  # brew install cairomm pangomm
  # brew link cairomm --force
  # brew link pangomm --force
  # xrepo install benchmark
  xrepo env -b benchmark -b eigen xmake require -v -y -f gabench
  # xrepo env -b benchmark -b gabench xmake -y

pbm:
  xrepo env -y -b benchmark -b eigen bash -c "cmake -DCMAKE_BUILD_TYPE=Release . & cmake --build . --parallel 8"

libs := "libs"

@clone URL DIR BRANCH:
    #!/usr/bin/env bash
    mkdir -p {{libs}}
    if [[ ! -d {{libs / DIR}} ]]; then
        git clone --depth=100 --recurse-submodules {{URL}} {{libs / DIR}}
    fi
    cd {{libs / DIR}}
    git fetch --depth=100 origin {{BRANCH}}
    git checkout {{BRANCH}}

prep-gal: (clone "https://github.com/jeremyong/gal" "GAL" "master")

@find NAME:
    xmake require -v --search {{NAME}} || true
    xmake require -v --search "vcpkg::{{NAME}}" || true
    xmake require -v --search "conan::{{NAME}}" || true
    # xmake require -v --search "conda::{{NAME}}" || true
    xmake require -v --search "cmake::{{NAME}}" || true
    # xmake require --search "clib::{{NAME}}" || true
    xmake require --search "brew::{{NAME}}" || true

@info NAME:
    xmake require --info {{NAME}}

@fetch NAME:
    xmake require --fetch {{NAME}}

@list:
    xmake require --list

clean:
    rm -rf build
    rm -rf .xmake
    xmake clean
